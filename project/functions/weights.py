import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.utils import resample
import warnings

class ANESWeights:
    """
    Class to handle ANES survey weights for density estimation
    Implements survey design adjustment using strata and PSU information
    """
    
    def __init__(self, df, weight_col='post_full', strata_col='full_var_stratum', psu_col='full_var_psu', random_state=None):
        """
        Initialize with ANES dataframe and weight columns
        
        Parameters:
        -----------
        df : pandas.DataFrame
            ANES dataframe
        weight_col : str
            Column name for survey weights (default: 'post_full')
        strata_col : str
            Column name for strata variable (default: 'full_var_stratum')
        psu_col : str
            Column name for PSU/cluster variable (default: 'full_var_psu')
        random_state : int, optional
            Random seed for reproducibility
        """
        self.df = df.copy()
        self.weight_col = weight_col
        self.strata_col = strata_col
        self.psu_col = psu_col
        self.random_state = random_state
        
        # Set random seed if provided
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        # Clean and prepare the data
        self._prepare_data()
    
    def _prepare_data(self):
        """
        Clean and prepare the survey data for weighted analysis
        """
        # Convert weight columns to numeric
        for col in [self.weight_col, self.strata_col, self.psu_col]:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove rows with missing survey design variables
        self.df = self.df.dropna(subset=[self.weight_col, self.strata_col, self.psu_col])
        
        # Remove invalid weights (negative or zero)
        self.df = self.df[self.df[self.weight_col] > 0]
        
        print(f"Survey data prepared: {len(self.df)} valid observations")
    
    def create_replicate_weights(self, n_replicates=100, method='bootstrap'):
        """
        Create replicate weights for variance estimation
        This is a simplified version - full BRR or jackknife would be more accurate
        
        Parameters:
        -----------
        n_replicates : int
            Number of replicate weight columns to create
        method : str
            Method for creating replicates ('bootstrap' or 'jackknife')
        """
        # Set seed for reproducibility
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        if method == 'bootstrap':
            # Bootstrap resampling within strata and PSUs
            replicate_weights = []
            
            for rep in range(n_replicates):
                rep_weights = []
                
                for stratum in self.df[self.strata_col].unique():
                    strata_df = self.df[self.df[self.strata_col] == stratum]
                    
                    # Resample PSUs within stratum with seed
                    psus = strata_df[self.psu_col].unique()
                    resampled_psus = resample(psus, replace=True, n_samples=len(psus), 
                                            random_state=self.random_state + rep if self.random_state else None)
                    
                    # Create replicate weight for this stratum
                    for _, row in strata_df.iterrows():
                        psu_count = np.sum(resampled_psus == row[self.psu_col])
                        rep_weight = row[self.weight_col] * psu_count
                        rep_weights.append(rep_weight)
                
                replicate_weights.append(rep_weights)
            
            # Add replicate weights to dataframe
            for i, weights in enumerate(replicate_weights):
                self.df[f'rep_weight_{i}'] = weights
        
        return self.df
    
    def get_weighted_sample(self, variable, group_var=None, method='replication'):
        """
        Create weighted sample for density estimation
        
        Parameters:
        -----------
        variable : str
            Variable name for density estimation
        group_var : str, optional
            Grouping variable name
        method : str
            Method for weighting ('replication', 'bootstrap', or 'simple')
        
        Returns:
        --------
        dict : Dictionary with weighted samples by group (if group_var provided)
        """
        # Set seed for reproducibility
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        # Filter valid data
        valid_cols = [variable, self.weight_col, self.strata_col, self.psu_col]
        if group_var:
            valid_cols.append(group_var)
        
        df_clean = self.df.dropna(subset=valid_cols)
        df_clean = df_clean[pd.to_numeric(df_clean[variable], errors='coerce').notna()]
        
        if method == 'replication':
            return self._replicate_method(df_clean, variable, group_var)
        elif method == 'bootstrap':
            return self._bootstrap_method(df_clean, variable, group_var)
        else:  # simple
            return self._simple_method(df_clean, variable, group_var)
    
    def _replicate_method(self, df, variable, group_var=None):
        """
        Replicate observations based on survey weights
        """
        def replicate_group(group_df):
            expanded_data = []
            
            for _, row in group_df.iterrows():
                # Calculate number of replications
                weight = row[self.weight_col]
                n_reps = max(1, int(round(weight / group_df[self.weight_col].min())))
                
                # Add replicated observations
                for _ in range(n_reps):
                    expanded_data.append(row[variable])
            
            return np.array(expanded_data)
        
        if group_var:
            result = {}
            for group in df[group_var].unique():
                group_df = df[df[group_var] == group]
                result[group] = replicate_group(group_df)
            return result
        else:
            return {'all': replicate_group(df)}
    
    def _bootstrap_method(self, df, variable, group_var=None, n_bootstrap=1000):
        """
        Bootstrap sampling with survey weights
        """
        # Set seed for bootstrap sampling
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        def bootstrap_group(group_df):
            values = group_df[variable].values
            weights = group_df[self.weight_col].values
            weights = weights / weights.sum()  # Normalize
            
            # Bootstrap sample
            bootstrap_indices = np.random.choice(
                len(values), 
                size=n_bootstrap, 
                p=weights, 
                replace=True
            )
            
            return values[bootstrap_indices]
        
        if group_var:
            result = {}
            for group in df[group_var].unique():
                group_df = df[df[group_var] == group]
                result[group] = bootstrap_group(group_df)
            return result
        else:
            return {'all': bootstrap_group(df)}
    
    def _simple_method(self, df, variable, group_var=None):
        """
        Simple approach: return original data with weights for external use
        """
        if group_var:
            result = {}
            for group in df[group_var].unique():
                group_df = df[df[group_var] == group]
                result[group] = {
                    'values': group_df[variable].values,
                    'weights': group_df[self.weight_col].values
                }
            return result
        else:
            return {
                'all': {
                    'values': df[variable].values,
                    'weights': df[self.weight_col].values
                }
            }

def weighted_kde(values, weights=None, bandwidth=None, random_state=None):
    """
    Compute weighted kernel density estimation
    
    Parameters:
    -----------
    values : array-like
        Data values
    weights : array-like, optional
        Weights for each value
    bandwidth : float, optional
        KDE bandwidth
    random_state : int, optional
        Random seed for reproducibility
    
    Returns:
    --------
    callable : KDE function
    """
    if weights is None:
        return gaussian_kde(values, bw_method=bandwidth)
    
    # Set seed for weighted KDE sampling
    if random_state is not None:
        np.random.seed(random_state)
    
    # For weighted KDE, we'll use a bootstrap approach
    weights = np.array(weights)
    weights = weights / weights.sum()  # Normalize
    
    # Create weighted sample through resampling
    n_samples = len(values) * 2  # Increase sample size
    indices = np.random.choice(len(values), size=n_samples, p=weights, replace=True)
    weighted_values = values[indices]
    
    return gaussian_kde(weighted_values, bw_method=bandwidth)

def apply_anes_weights_to_density(df, variable, group_var=None, weight_method='replication', random_state=None):
    """
    Main function to apply ANES survey weights to density estimation
    
    Parameters:
    -----------
    df : pandas.DataFrame
        ANES dataframe
    variable : str
        Variable for density estimation
    group_var : str, optional
        Grouping variable
    weight_method : str
        Weighting method ('replication', 'bootstrap', or 'simple')
    random_state : int, optional
        Random seed for reproducibility
    
    Returns:
    --------
    dict : Dictionary with KDE objects for each group
    """
    # Initialize weights handler with seed
    weights_handler = ANESWeights(df, random_state=random_state)
    
    # Get weighted samples
    weighted_samples = weights_handler.get_weighted_sample(
        variable, group_var, method=weight_method
    )
    
    # Compute KDE for each group
    kde_results = {}
    
    for group, data in weighted_samples.items():
        if weight_method == 'simple':
            # Handle simple method with explicit weights
            kde_results[group] = weighted_kde(data['values'], data['weights'], random_state=random_state)
        else:
            # Handle replication and bootstrap methods
            kde_results[group] = gaussian_kde(data)
    
    return kde_results

# Convenience function for direct integration with existing code
def get_anes_weighted_density_data(df, variable, groups, group_var='party', weight_method='replication', random_state=None):
    """
    Get weighted density data ready for plotting
    
    Parameters:
    -----------
    df : pandas.DataFrame
        ANES dataframe with survey weights
    variable : str
        Variable for density estimation
    groups : list
        List of groups to include
    group_var : str
        Grouping variable name
    weight_method : str
        Weighting method
    random_state : int, optional
        Random seed for reproducibility
    
    Returns:
    --------
    dict : Dictionary with x_range and y_values for each group
    """
    # Filter data for specified groups
    df_filtered = df[df[group_var].isin(groups)]
    
    # Apply weights and get KDE with seed
    kde_results = apply_anes_weights_to_density(
        df_filtered, variable, group_var, weight_method, random_state=random_state
    )
    
    # Generate plotting data
    x_range = np.linspace(0, 100, 500)  # Assuming 0-100 scale
    plotting_data = {}
    
    for group in groups:
        if group in kde_results:
            kde = kde_results[group]
            y_values = kde(x_range)
            plotting_data[group] = {
                'x_range': x_range,
                'y_values': y_values
            }
    
    return plotting_data
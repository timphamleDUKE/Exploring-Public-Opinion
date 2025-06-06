import pandas as pd
import numpy as np
import streamlit as st

def ces_calc_weights(df, question, group):
    grouped = (
        df.groupby([group, question])['commonweight']
        .sum()
        .reset_index(name='weighted_count')
    )
    
    totals = grouped.groupby(group)['weighted_count'].transform('sum')
    grouped['proportion'] = grouped['weighted_count'] / totals
    
    grouped = grouped.rename(columns={question: "response", group: "group"})
    
    st.write("CES final data:")
    st.write(grouped)
    
    return grouped

def anes_calc_weights_complex(df, question, group):
    """
    This is your original complex survey weight calculation
    Keep this if you need the survey design adjustments
    """
    weight_col = 'post_full'
    stratum_col = 'full_var_stratum'
    psu_col = 'full_var_psu'
    
    # Drop missing data AND empty strings
    df = df.dropna(subset=[group, question, weight_col, stratum_col, psu_col])
    
    # Additional filtering to remove empty strings
    df = df[
        (df[group] != '') & 
        (df[question] != '') & 
        (df[weight_col] != '') & 
        (df[stratum_col] != '') & 
        (df[psu_col] != '')
    ]
    
    # Convert weight columns to numeric, coercing errors to NaN
    df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
    df[stratum_col] = pd.to_numeric(df[stratum_col], errors='coerce')
    df[psu_col] = pd.to_numeric(df[psu_col], errors='coerce')
    
    # Drop any rows where conversion failed
    df = df.dropna(subset=[weight_col, stratum_col, psu_col])
    
    # One-hot encode responses
    prefix = 'resp'
    response_dummies = pd.get_dummies(df[question], prefix=prefix)
    df = pd.concat([df.reset_index(drop=True), response_dummies.reset_index(drop=True)], axis=1)
    response_cols = [col for col in df.columns if col.startswith(prefix)]
    
    results = []
    
    for response_col in response_cols:
        total_sum = 0
        variance_sum = 0
        
        # Group by strata
        for stratum, stratum_df in df.groupby(stratum_col):
            psu_totals = []
            
            for psu, psu_df in stratum_df.groupby(psu_col):
                # Calculate PSU total with additional safety check
                calculation = psu_df[response_col] * psu_df[weight_col]
                psu_total_raw = calculation.sum()
                
                # Handle case where sum might be empty or invalid
                try:
                    psu_total = float(psu_total_raw) if psu_total_raw != '' else 0.0
                except (ValueError, TypeError):
                    psu_total = 0.0
                
                psu_totals.append(psu_total)
            
            psu_totals = np.array(psu_totals)
            n_psus = len(psu_totals)
            
            if n_psus >= 2:
                stratum_mean = psu_totals.mean()
                stratum_var = ((psu_totals - stratum_mean) ** 2).sum() / (n_psus - 1)
                
                total_sum += psu_totals.sum()
                variance_sum += stratum_var
            else:
                total_sum += psu_totals.sum()
        
        se = np.sqrt(variance_sum)
        
        # Store results for each group (not just overall)
        # Group by group var and response
        for level in df[group].unique():
            subset = df[df[group] == level]
            calculation = subset[response_col] * subset[weight_col]
            count_raw = calculation.sum()
            
            # Handle case where sum might be empty or invalid
            try:
                count = float(count_raw) if count_raw != '' else 0.0
            except (ValueError, TypeError):
                count = 0.0
            
            results.append({
                group: level,
                'response': response_col.replace(prefix + '_', ''),
                'weighted_count': count,
                'se': se
            })
    
    # Convert to DataFrame
    result_df = pd.DataFrame(results)
    
    # Compute proportion within group
    totals = result_df.groupby(group)['weighted_count'].transform('sum')
    result_df['proportion'] = result_df['weighted_count'] / totals
    
    # Ensure consistent column naming - rename the group column to match CES format
    result_df = result_df.rename(columns={group: "group"})
    
    st.write("ANES Final Data:")
    st.write(result_df)
    
    return result_df
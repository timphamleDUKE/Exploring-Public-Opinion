import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.utils import resample
import streamlit as st
from functions.dictionaries import find_weight_col

class SurveyDesign:
    """
    Emulates Stata"s svyset design object: handles weights, strata, and PSUs
    """
    def __init__(self, df, weight, strata=None, psu=None, seed=None):
        self.df = df.copy()
        self.weight_col = weight
        self.strata_col = strata
        self.psu_col = psu
        self.seed = seed

        if self.seed is not None:
            np.random.seed(self.seed)

        self._prepare()

    def _prepare(self):
        cols = [self.weight_col] + ([self.strata_col] if self.strata_col else []) + ([self.psu_col] if self.psu_col else [])
        for col in cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.df = self.df.dropna(subset=[self.weight_col])
        if self.strata_col:
            self.df = self.df.dropna(subset=[self.strata_col])
        if self.psu_col:
            self.df = self.df.dropna(subset=[self.psu_col])

        self.df = self.df[self.df[self.weight_col] > 0]

    def get_weighted_sample(self, variable, group_var=None, method="bootstrap", n_samples=1000):
        df = self.df.dropna(subset=[variable])
        if group_var:
            df = df.dropna(subset=[group_var])

        if method == "bootstrap":
            return self._bootstrap_sampling(df, variable, group_var, n_samples)
        elif method == "replication":
            return self._replication_sampling(df, variable, group_var)
        else:
            return self._simple_sample(df, variable, group_var)

    def _bootstrap_sampling(self, df, variable, group_var, n_samples):
        def sample_group(group_df):
            values = group_df[variable].values
            weights = group_df[self.weight_col].values / group_df[self.weight_col].sum()
            indices = np.random.choice(len(values), size=n_samples, p=weights, replace=True)
            return values[indices]

        if group_var:
            return {g: sample_group(gdf) for g, gdf in df.groupby(group_var)}
        else:
            return {"all": sample_group(df)}

    def _replication_sampling(self, df, variable, group_var):
        def replicate_group(gdf):
            min_weight = gdf[self.weight_col].min()
            expanded = []
            for _, row in gdf.iterrows():
                n_rep = max(1, int(round(row[self.weight_col] / min_weight)))
                expanded.extend([row[variable]] * n_rep)
            return np.array(expanded)

        if group_var:
            return {g: replicate_group(gdf) for g, gdf in df.groupby(group_var)}
        else:
            return {"all": replicate_group(df)}

    def _simple_sample(self, df, variable, group_var):
        if group_var:
            return {
                g: {
                    "values": gdf[variable].values,
                    "weights": gdf[self.weight_col].values
                }
                for g, gdf in df.groupby(group_var)
            }
        else:
            return {
                "all": {
                    "values": df[variable].values,
                    "weights": df[self.weight_col].values
                }
            }

def weighted_kde(values, weights=None, bandwidth=None):
    if weights is None:
        return gaussian_kde(values, bw_method=bandwidth)

    weights = weights / np.sum(weights)
    indices = np.random.choice(len(values), size=len(values)*2, p=weights, replace=True)
    resampled = values[indices]
    return gaussian_kde(resampled, bw_method=bandwidth)



def apply_svy_density(df, variable, weight_col, group_var=None, strata_col="full_var_stratum", psu_col="full_var_psu", method="bootstrap", seed=None):
    design = SurveyDesign(df, weight=weight_col, strata=strata_col, psu=psu_col, seed=seed)
    st.write(weight_col)
    return design.get_weighted_sample(variable, group_var=group_var, method=method)


def get_anes_weighted_density_data(df, variable, groups, group_var="party", weight_method="bootstrap", seed=None):
    df = df[df[group_var].isin(groups)]
    samples = apply_svy_density(df, variable, weight_col = find_weight_col(variable), group_var=group_var, method=weight_method, seed=seed)

    x_range = np.linspace(0, 100, 500)
    result = {}

    for group in groups:
        if weight_method == "simple":
            values = samples[group]["values"]
            weights = samples[group]["weights"]
            kde = weighted_kde(values, weights)
        else:
            kde = gaussian_kde(samples[group])

        result[group] = {
            "x_range": x_range,
            "y_values": kde(x_range)
        }

    return result




import pandas as pd
import numpy as np

def estimate_weighted_totals_with_design(
    df,
    question_col,
    weight_col,
    stratum_col,
    psu_col,
    prefix='resp'
):
    """
    Estimate survey-weighted totals and standard errors for each category
    of a categorical variable, accounting for stratification and clustering.

    Parameters:
        df (DataFrame): The survey data
        question_col (str): Column name of the categorical survey question
        weight_col (str): Survey weight column ('pre_full' or 'post_full')
        stratum_col (str): Stratification variable (e.g., 'full_var_stratum')
        psu_col (str): PSU (cluster) variable (e.g., 'full_var_psu')
        prefix (str): Prefix for one-hot encoded response columns

    Returns:
        DataFrame with columns: response, total, se
    """
    
    # Step 1: One-hot encode the responses
    df = df.dropna(subset=[question_col, weight_col, stratum_col, psu_col])
    response_dummies = pd.get_dummies(df[question_col], prefix=prefix)
    df = pd.concat([df.reset_index(drop=True), response_dummies.reset_index(drop=True)], axis=1)
    
    # Step 2: Initialize result container
    results = []

    response_cols = [col for col in df.columns if col.startswith(prefix)]

    # Step 3: Loop over each response category (dummy column)
    for col in response_cols:
        total_sum = 0
        variance_sum = 0

        # Group by stratum
        for stratum, stratum_df in df.groupby(stratum_col):
            psu_totals = []

            # Group within stratum by PSU
            for psu, psu_df in stratum_df.groupby(psu_col):
                # Compute PSU-level weighted total
                psu_total = (psu_df[col] * psu_df[weight_col]).sum()
                psu_totals.append(psu_total)

            psu_totals = np.array(psu_totals)
            n_psus = len(psu_totals)

            # Only calculate variance if there are 2+ PSUs
            if n_psus >= 2:
                stratum_mean = psu_totals.mean()
                stratum_var = ((psu_totals - stratum_mean) ** 2).sum() / (n_psus - 1)

                total_sum += psu_totals.sum()
                variance_sum += stratum_var
            else:
                # If only 1 PSU in stratum, we skip variance calculation for that stratum
                total_sum += psu_totals.sum()
                # No contribution to variance

        # Final standard error
        se = np.sqrt(variance_sum)

        # Append results
        results.append({
            'response': col.replace(prefix + '_', ''),
            'total': total_sum,
            'se': se
        })

    return pd.DataFrame(results)









results_df = estimate_weighted_totals_with_design(
    df=df,
    question_col='q1',           # your survey question
    weight_col='post_full',      # or 'pre_full' depending on timing
    stratum_col='full_var_stratum',
    psu_col='full_var_psu'
)

# Optional: plot
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(results_df['response'], results_df['total'], yerr=1.96 * results_df['se'], capsize=5)
plt.title("Survey-Weighted Totals with 95% CI")
plt.xlabel("Response")
plt.ylabel("Estimated Total")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()





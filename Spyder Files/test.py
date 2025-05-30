#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 10:27:13 2025

@author: alexafahrer
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../Data/ANES_2024.csv")

df = df[["V242064", "V241302", "V240107b"]]  # Party, Abortion opinion, Weight

valid_opinions = [1, 2, 3, 4, 5]
df = df[df["V241302"].isin(valid_opinions)]

valid_parties = [1,2]
df = df[df["V242064"].isin(valid_opinions)]

# Map response codes to readable labels
opinion_labels = {
    1: "Never permitted",
    2: "Only after rape/incest",
    3: "Only after need clearly established",
    4: "Always permitted",
    5: "Other"
}
df["response_label"] = df["V241302"].map(opinion_labels)

# Map party codes to labels
party_labels = {
    1: "Democrat",
    2: "Republican"
}
df["party_label"] = df["V242064"].map(party_labels)

# Group by response and party
grouped = df.groupby(["party_label", "response_label"], as_index=False)["V240107b"].sum()
grouped.rename(columns={"V240107b": "weighted_count"}, inplace=True)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped, x="response_label", y="weighted_count", hue="party_label")

plt.title("Weighted Abortion Opinions by Political Party")
plt.xlabel("Opinion on Abortion")
plt.ylabel("Weighted Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(grouped["weighted_count"].describe())
print(grouped["weighted_count"].min())




import os
import pandas as pd

# Confirm location
print("✅ Current working directory:", os.getcwd())

# Load the ANES 2024 dataset
df = pd.read_csv("../Data/ANES_2024.csv")
print("✅ Original dataset shape:", df.shape)

# Variables across 8 major topics
selected_cols = [
    "V241302", "V241303", "V241304", "V241305",  # Abortion
    "V241245", "V241246", "V241247",             # Healthcare
    "V242235", "V242236", "V242234x",            # Immigration
    "V242326", "V242328x", "V242329",            # Guns
    "V242321", "V242322", "V242324x",            # Environment
    "V241252", "V241253", "V241254",             # Economy
    "V241306", "V241308x",                       # Policing
    "V242064", "V242065", "V242104x"             # Voting
]

# Trim to selected variables (only keep columns that exist)
existing_cols = [col for col in selected_cols if col in df.columns]
df_filtered = df[existing_cols]

# Remove invalid responses
# invalid_vals = [-9, -8, -7, -6, -5, -4, -3, -2, -1]
# for col in df_filtered.columns:
    # df_filtered = df_filtered[~df_filtered[col].isin(invalid_vals)]

# Save cleaned data
df_filtered.to_csv("../Data/CLEANED_ANES_2024.csv", index=False)
print("✅ Cleaned subset saved as 'cleaned_anes_2024_subset.csv'")




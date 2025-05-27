#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 11:11:30 2025

@author: jj
"""

import os
import pandas as pd

# Confirm location
print("✅ Current working directory:", os.getcwd())

# Load the ANES 2024 dataset
df = pd.read_csv("anes2024.csv")
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
invalid_vals = [-9, -8, -7, -6, -5, -4, -3, -2, -1]
for col in df_filtered.columns:
    df_filtered = df_filtered[~df_filtered[col].isin(invalid_vals)]

# Save cleaned data
df_filtered.to_csv("cleaned_anes_2024_subset.csv", index=False)
print("✅ Cleaned subset saved as 'cleaned_anes_2024_subset.csv'")




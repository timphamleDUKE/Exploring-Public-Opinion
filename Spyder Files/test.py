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

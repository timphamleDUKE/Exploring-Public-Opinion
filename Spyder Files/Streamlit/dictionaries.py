# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 12:39:46 2025

@author: heyti
"""

import pandas as pd

codebook = pd.read_csv("data/codebook.csv")

# Lists

list_of_group_bys = [
        "Political Party", 
        "Education", 
        "Employment Status", 
        "Marriage", 
        "Income", 
        "Religion", 
        "Gender",
        "Race",
        "State",
        "Urban/Rural Status"
        ]

list_of_topics = codebook["topic"].dropna().unique().tolist()

# Dictionaries

group_by_dic = {
        "Political Party": "poli_party_reg", 
        "Education": "educ", 
        "Employment Status": "employ", 
        "Marriage": "marstat", 
        "Income": "faminc_new", 
        "Religion": "religion", 
        "Gender": "gender",
        "Race": "race",
        "State": "input_state",
        "Urban/Rural Status": "urban_rural"
    }

study_dic = {
    "Cooperative Election Study": "CES",
    "American National Election Studies": "ANES"
}

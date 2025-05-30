# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:23:25 2025

@author: heyti
"""

import streamlit as st

st.write("### Public Opinion Explorer")

st.markdown("--description of page--")


# inputs

col1, col2, col3 = st.columns(3)

study = col1.selectbox(
    "Study",
    ("Cooperative Election Study", "American National Election Studies"),
)

topic = col2.selectbox(
    "Topic",
    ("Abortion", "Gun Control"),
)

group_by = col3.multiselect(
    "Group By:",
    ["Political Party", 
     "Education", 
     "Employment Status", 
     "Marriage", 
     "Income", 
     "Religion", 
     "Gender",
     "Race",
     "State",
     "Urban/Rural Status"
     ],
    default=["Political Party"],
)

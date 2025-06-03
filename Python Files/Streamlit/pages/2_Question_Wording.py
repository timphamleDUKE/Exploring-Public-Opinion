# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:23:25 2025

@author: heyti
"""

import streamlit as st
import pandas as pd

st.write("### Question Wording")

study_df = pd.read_csv("data/CES_2024_clean.csv")

st.write(study_df["race"])
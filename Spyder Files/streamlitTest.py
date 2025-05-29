# -*- coding: utf-8 -*-
"""
Created on Thu May 29 10:03:44 2025

@author: heyti
"""

import streamlit as st
import pandas as pd
import os

st.write("Hello World")
st.text_input("What is you favorite color?")

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "..", "Data", "ANES_2024.csv")

ANES_2024 = pd.read_csv(csv_path)
st.write(ANES_2024)
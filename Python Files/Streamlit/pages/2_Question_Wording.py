import streamlit as st
import pandas as pd
from Home import set_logo

set_logo()

st.write("### Question Wording")

study_df = pd.read_csv("data/CES_2024_clean.csv")

st.write(study_df["race"])
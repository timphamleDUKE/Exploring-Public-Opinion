import streamlit as st
import pandas as pd
from functions.dictionaries import set_logo

set_logo()

# Create two columns for title and image
col1, col2 = st.columns([3, 1])

with col1:
    st.title("About the Data")

with col2:
    st.image("images/Anes Logo.png")

st.divider()

# Description
st.markdown("""
**American National Election Survey (ANES) 2024**  
5,521 observations and 124 variables  
High quality public opinion data
""")

st.markdown(
    "This project: "
    "[**American National Election Studies**](https://electionstudies.org/)."
)

# Show the dataframe
df = pd.read_csv("../data/anes_2024_clean.csv")
st.write(df)
import streamlit as st
import base64
import os
from functions.dictionaries import set_logo, df

set_logo()

# Create two columns for title and image
col1, col2 = st.columns([3, 1])

with col1:
    st.title("About the Data")

with col2:
    st.image("images/Anes Logo.png", use_container_width=True)

st.divider()

# Show the dataframe
st.write(df)

# Add metadata description
st.markdown("""
**American National Election Survey (ANES) 2024**  
5,521 observations and 124 variables  
High quality public opinion data
""")

# ---------- Footer ----------
st.divider()
st.markdown(
    "This project: "
    "[**American National Election Studies**](https://electionstudies.org/)."
)
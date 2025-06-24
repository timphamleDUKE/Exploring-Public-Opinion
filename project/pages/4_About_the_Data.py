import streamlit as st
import base64
import os
from functions.dictionaries import set_logo, df

set_logo()
st.title("About the Data")
st.divider()

st.write(df)
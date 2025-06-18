import streamlit as st
from functions.dictionaries import set_logo

set_logo()
st.title("Home")
st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)


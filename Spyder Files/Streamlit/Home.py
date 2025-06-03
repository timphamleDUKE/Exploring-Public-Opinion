# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:23:25 2025

@author: heyti
"""

import streamlit as st

st.set_page_config(
    page_title="Survey Navigator",
    layout="wide"
)

LOGO_WIDE = "images/logo.png"
LOGO_ICON = "images/logo.png"

# Display the logo
st.logo(
    image=LOGO_WIDE,
    size="large",
    link="https://your-company-website.com", 
    icon_image=LOGO_ICON
)

LOGO_PATH = "images/logo.png"

# Display a large logo at the top of the page
st.image(LOGO_PATH, width=300)

# Add a large logo to the sidebar
with st.sidebar:
    st.image(LOGO_PATH, width=300)


st.title("The Survey Navigator")
st.divider()

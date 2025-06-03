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

def set_logo():
    logo = "images/logo.png"
    data_plus_logo = "images/data+.png"

    st.logo(
        image=logo,
        link="https://your-company-website.com", 
        icon_image=logo,
        size = "large"
    )


    with st.sidebar:
        st.image(data_plus_logo, use_container_width=True)

set_logo()


st.title("The Survey Navigator")
st.divider()

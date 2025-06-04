import streamlit as st

st.set_page_config(
    page_title="Survey Navigator",
    layout="wide"
)

def set_logo():
    logo = "images/logo-black.PNG"
    data_plus_logo = "images/data+.png"

    st.logo(
        image=logo,
        link="https://your-company-website.com", 
        icon_image=logo,
        size = "large"
    )

set_logo()


st.title("The Survey Navigator")
st.divider()

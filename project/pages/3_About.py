import streamlit as st
import os

st.set_page_config(page_title="About the Authors", layout="wide")

st.markdown(
    "<h1 style='font-size: 40px; margin-bottom: 0;'>About the Authors</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
<p style='font-size:18px; line-height:1.6;'>
This tool was created as part of a research collaboration with the <strong>Duke University Polarization Lab</strong>,
focusing on how survey wording affects perceived political polarization.
</p>
<hr style='margin-top:0;'>
""",
    unsafe_allow_html=True
)

# Create 3 horizontal columns
col1, col2, col3 = st.columns(3)

def author_card(image_path, name, link):
    if os.path.exists(image_path):
        st.image(image_path, width=180)
    st.markdown(
        f"<p style='font-size:16px; text-align: center;'><a href='{link}' target='_blank'><strong>{name}</strong></a></p>",
        unsafe_allow_html=True
    )

with col1:
    author_card("images/AF.jpg", "Alexa Fahrer", "https://www.linkedin.com/in/alexa-fahrer-138456133/")

with col2:
    author_card("images/TL.jpg", "Tim Le", "https://www.linkedin.com/in/tim-le-836296283/")

with col3:
    author_card("images/JJ.jpeg", "Joie Jacobs", "https://www.linkedin.com/in/joie-jacobs-09801b332/")


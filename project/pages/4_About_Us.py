import streamlit as st
import base64
import os
from functions.dictionaries import set_logo

set_logo()
st.title("About Us")
st.divider()

# ---------- Helper to embed images as base64 ----------
def base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------- Author Card Function ----------
def author_card(image_path, name, class_year, major, school, linkedin_url):
    if not os.path.exists(image_path):
        return
    encoded_image = base64_image(image_path)
    html = f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;">
            <img src="data:image/png;base64,{encoded_image}"
                 style="width: 240px; height: 240px; object-fit: cover;
                        border: 2px solid #31333F; border-radius: 0;">
            <div style="margin-top: 1rem;">
                <strong style="font-size: 18px;">{name}</strong><br>
                <span style="font-size: 16px;">{class_year}</span><br>
                <span style="font-size: 16px;">{major}</span><br>
                <span style="font-size: 16px;">{school}</span>
            </div>
        </a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------- Authors Data ----------
authors = [
    {
        "image_path": "images/AF_cropped.png",
        "name": "Alexa Fahrer",
        "class_year": "Class of 2026",
        "major": "Statistical Science & Public Policy",
        "school": "Duke University",
        "linkedin_url": "https://www.linkedin.com/in/alexa-fahrer-138456133/"
    },
    {
        "image_path": "images/TL_cropped.png",
        "name": "Tim Le",
        "class_year": "Class of 2028",
        "major": "Computer Science & Statistical Science",
        "school": "Duke University",
        "linkedin_url": "https://www.linkedin.com/in/tim-le-836296283/"
    },
    {
        "image_path": "images/JJ_cropped.png",
        "name": "Joie Jacobs",
        "class_year": "Class of 2028",
        "major": "Accounting & Math",
        "school": "North Carolina Central University",
        "linkedin_url": "https://www.linkedin.com/in/joie-jacobs-09801b332/"
    }
]

# ---------- Display Author Cards ----------
cols = st.columns(len(authors))
for col, author in zip(cols, authors):
    with col:
        author_card(**author)

# ---------- Footer ----------
st.divider()
st.markdown(
    "This project was created as part of a research collaboration with the "
    "[**Duke University Polarization Lab**](https://www.polarizationlab.com/)."
)
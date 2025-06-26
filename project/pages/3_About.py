import streamlit as st
import pandas as pd
import base64
import os
from functions.dictionaries import set_logo
from functions.css import load_custom_css

# Load custom styling
load_custom_css()

set_logo()

# Enhanced hero section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">About</h1>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["The Data", "The Team"])

# Tab 1: The Data
df = pd.read_csv("../data/anes_2024_clean.csv")

with tab1:
    st.markdown("""
    <div class="content-container">
        <div class="data-description">
            The data used in this project come from the <strong>American National Election Survey (ANES) 2024</strong>, 
            one of the most respected sources of public opinion data in the United States, a collaborative project between Stanford 
            University and the University of Michigan.
            <br><br>
            The dataset includes detailed information on political attitudes, voting behavior, 
            demographic characteristics, ideological self-placement, partisanship, and much more.
        </div>
        
        <div class="data-stats">
            <div class="stat-item">
                <span class="stat-number">5,521</span>
                <div class="stat-label">Respondents</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">124</span>
                <div class="stat-label">Variables</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display dataframe with enhanced styling
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="logo-container">
            <img src="images/logos/anes-logo.png" style="max-width: 100%; height: auto;">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-text">
        This project was created as part of a research collaboration with the 
        <a href="https://www.polarizationlab.com/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600;">Duke University Polarization Lab</a> 
        using data from the <a href="https://electionstudies.org/" target="_blank" style="color: #764ba2; text-decoration: none; font-weight: 600;">American National Election Studies</a>.
    </div>
    """, unsafe_allow_html=True)

# Tab 2: The Team
with tab2:
    def base64_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def author_card(image_path, name, class_year, major, school, linkedin_url):
        if not os.path.exists(image_path):
            return
        encoded_image = base64_image(image_path)
        html = f"""
        <div class="author-card">
            <a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="author-img-wrapper">
                    <img class="author-card-img" src="data:image/png;base64,{encoded_image}">
                </div>
                <div class="author-card-description">
                    <div class="author-name">{name}</div>
                    <div class="author-info">
                        {class_year}<br>
                        {major}<br>
                        {school}
                    </div>
                </div>
            </a>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    # Team introduction
    st.markdown("""
    <div class="content-container">
        <div style="text-align: center;">
            <h2 style="color: #3b4cb8; margin-bottom: 1.5rem;">Meet Our Research Team</h2>
            <p style="font-size: 1.2rem; color: #5a6c7d; line-height: 1.6;">
                Our interdisciplinary team combines expertise in statistics, computer science, public policy, 
                and business to provide comprehensive insights into American political opinion.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    authors = [
        {
            "image_path": "images/pfp/AF_cropped.png",
            "name": "Alexa Fahrer",
            "class_year": "Class of 2026",
            "major": "Statistical Science & Public Policy",
            "school": "Duke University",
            "linkedin_url": "https://www.linkedin.com/in/alexa-fahrer-138456133/"
        },
        {
            "image_path": "images/pfp/TL_cropped.png",
            "name": "Tim Le",
            "class_year": "Class of 2028",
            "major": "Computer Science & Statistical Science",
            "school": "Duke University",
            "linkedin_url": "https://www.linkedin.com/in/tim-le-836296283/"
        },
        {
            "image_path": "images/pfp/JJ_cropped.png",
            "name": "Joie Jacobs",
            "class_year": "Class of 2028",
            "major": "Accounting & Math",
            "school": "North Carolina Central University",
            "linkedin_url": "https://www.linkedin.com/in/joie-jacobs-09801b332/"
        },
        {
            "image_path": "images/pfp/DM_Lol.png",
            "name": "Dario Moscatello",
            "class_year": "Class of 2026",
            "major": "Business Administration",
            "school": "Bocconi University",
            "linkedin_url": "https://www.linkedin.com/in/dario-moscatello-/"
        }
    ]
    
    cols = st.columns(len(authors))
    for col, author in zip(cols, authors):
        with col:
            author_card(**author)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer-text">
        This project was created as part of a research collaboration with the 
        <a href="https://www.polarizationlab.com/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600;">Duke University Polarization Lab</a> 
        using data from <a href="https://electionstudies.org/" target="_blank" style="color: #764ba2; text-decoration: none; font-weight: 600;">American National Election Studies</a>.
    </div>
    """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import base64
import os
from functions.dictionaries import set_logo
from functions.css import load_custom_css

set_logo()
load_custom_css()
st.title("About")

# Tabs
tab1, tab2 = st.tabs(["The Data", "The Team"])

script_dir = os.path.dirname(os.path.abspath(__file__))
df_path = os.path.join(script_dir, '..', '..', 'data', 'anes_2024_clean.csv')
df = pd.read_csv(df_path)

# Tab 1: The Data
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Add metadata description
        st.markdown("""  
        The data used in this project come from the **American National Election Survey (ANES) 2024**, 
        one of the most respected sources of public opinion data in the United States. ANES is a 
        collaboration of Duke University, University of Michigan, The University of Texas at Austin, 
        and Stanford University, with funding by the National Science Foundation.
        
        **Observations:** 5,521 respondents    &    **Variables:** 124
        
        The dataset includes detailed information on political attitudes, voting behavior, 
        demographic characteristics, ideological self-placement, partisanship, and more.
        """)
        
    with col2:

        script_dir = os.path.dirname(os.path.abspath(__file__))
        anes_logo_path = os.path.join(script_dir, '..', 'images', 'logos', 'anes-logo.png')

        st.image(anes_logo_path, use_container_width=True)
    
    # Add space between text and dataframe
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display dataframe at full width
    st.dataframe(df)
    
    st.markdown(
        "This project was created as part of a research collaboration with the "
        "[**Duke University Polarization Lab**](https://www.polarizationlab.com/) "
        "using data from the [**American National Election Studies**](https://electionstudies.org/)."
    )

# Tab 2: Us
with tab2:

    def base64_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def author_card(image_path, name, class_year, major, school, linkedin_url):
        if not os.path.exists(image_path):
            return
        encoded_image = base64_image(image_path)
        html = f"""
        <div class="author-container" style="text-align: center; margin-bottom: 2rem;">
            <a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;">
                <img src="data:image/png;base64,{encoded_image}"
                     style="width: 240px; height: 240px; object-fit: cover;
                            border: 2px solid #31333F; border-radius: 0;">
            </a>
                <div style="margin-top: 1rem;">
                    <strong style="font-size: 18px;">{name}</strong><br>
                    <span style="font-size: 16px;">{class_year}</span><br>
                    <span style="font-size: 16px;">{major}</span><br>
                    <span style="font-size: 16px;">{school}</span>
                </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    alexa_pic_path = os.path.join(script_dir, '..', 'images', 'pfp', 'AF.png')
    tim_pic_path = os.path.join(script_dir, '..', 'images', 'pfp', 'TL.png')
    joie_pic_path = os.path.join(script_dir, '..', 'images', 'pfp', 'JJ.png')
    dario_pic_path = os.path.join(script_dir, '..', 'images', 'pfp', 'DM.png')

    authors = [
        {
            "image_path": alexa_pic_path,
            "name": "Alexa Fahrer",
            "class_year": "Class of 2026",
            "major": "Statistical Science & Public Policy",
            "school": "Duke University",
            "linkedin_url": "https://www.linkedin.com/in/alexa-fahrer-138456133/"
        },
        {
            "image_path": tim_pic_path,
            "name": "Tim Le",
            "class_year": "Class of 2028",
            "major": "Computer Science & Statistical Science",
            "school": "Duke University",
            "linkedin_url": "https://www.linkedin.com/in/tim-le-836296283/"
        },
        {
            "image_path": joie_pic_path,
            "name": "Joie Jacobs",
            "class_year": "Class of 2028",
            "major": "Accounting & Math",
            "school": "North Carolina Central University",
            "linkedin_url": "https://www.linkedin.com/in/joie-jacobs-09801b332/"
        },
        {
            "image_path": dario_pic_path,
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
    
    st.divider()
    st.markdown(
        "This project was created as part of a research collaboration with the "
        "[**Duke University Polarization Lab**](https://www.polarizationlab.com/) "
        "using data from [**American National Election Studies**](https://electionstudies.org/)."
    )
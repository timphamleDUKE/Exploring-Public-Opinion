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
tab1, tab2, tab3 = st.tabs(["The Data", "The Team", "How to Use"])

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

with tab3:

    PAGES = [
    {
        "title": "Affective Polarization",
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 18 Q6 4 10 8 Q14 12 18 18" stroke="#764ba2" stroke-width="2" fill="none"/>
                <path d="M2 18 Q6 4 10 8 Q14 12 18 18 L18 20 L2 20 Z" fill="#764ba2" opacity="0.25"/>
                <path d="M6 18 Q10 14 14 10 Q18 6 22 18" stroke="#667eea" stroke-width="2" fill="none"/>
                <path d="M6 18 Q10 14 14 10 Q18 6 22 18 L22 20 L6 20 Z" fill="#667eea" opacity="0.25"/>
                <line x1="2" y1="20" x2="22" y2="20" stroke="#999" stroke-width="1"/>
               </svg>""",
        "description": """
        Defined as how much warmer partisans feel about their own party versus the opposing party, measured using feeling thermometer ratings on a 0-100 degree scale.

        The Featured tab contains density graphs depicting thermometer ratings showing how different parties rate each other,
        how people of different ideologies rate each other,
        and how different parties rate each presidential candidate from the 2024 Election (both pre- and post-election).
        
        The Explore tab allows users to filter through various ANES 2024 survey questions related to feeling thermometer ratings
        and see how different ideological and political groups rated each other. Users can also facet these graphs to view more detailed findings.

        """,
        "button_text": "Explore Affective Polarization",
        "page": "pages/1_Affective_Polarization.py",
        "key": "ap_button"
    },
    {
        "title": "Issue Position", 
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="1" y="4" width="2" height="4" rx="1" fill="#764ba2"/>
                <rect x="1" y="10" width="2" height="6" rx="1" fill="#764ba2"/>
                <rect x="1" y="18" width="2" height="2" rx="1" fill="#764ba2"/>
                <rect x="21" y="6" width="2" height="3" rx="1" fill="#667eea"/>
                <rect x="21" y="11" width="2" height="8" rx="1" fill="#667eea"/>
                <rect x="21" y="20" width="2" height="2" rx="1" fill="#667eea"/>
                <path d="M3 6 C8 6 16 7 21 7.5 L21 9 C16 8.5 8 7.5 3 8 Z" fill="#764ba2" opacity="0.4"/>
                <path d="M3 8 C8 9 16 12 21 15 L21 17 C16 14 8 10 3 8.5 Z" fill="#764ba2" opacity="0.5"/>
                <path d="M3 13 C8 14 16 16 21 17 L21 19 C16 18 8 15 3 15 Z" fill="#764ba2" opacity="0.6"/>
                <path d="M3 19 C8 19.5 16 20.5 21 21 L21 22 C16 21.5 8 20 3 19.5 Z" fill="#764ba2" opacity="0.3"/>
               </svg>""",
        "description": """
        Defined as the widening gap in policy opinions between ideological groups, with people taking increasingly opposing stances on key political issues.

        This page allows users to filter through various issue-based questions from the ANES 2024 survey and see how different ideological and political groups
        responded to these policy questions. Users can view these responses through sankey flow diagrams, displaying either direct response flows or simplified binary flows 
        to better understand how political preferences align across different topics.

        """,
        "button_text": "Analyze Issue Positions",
        "page": "pages/2_Issue_Position.py",
        "key": "ip_button"
    },
    {
        "title": "Rate and Compare", 
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="#764ba2" stroke-width="2" fill="none"/>
                <path d="M9 12 L11 14 L15 10" stroke="#667eea" stroke-width="2" fill="none"/>
                <path d="M6 8 L6 16 M18 8 L18 16" stroke="#764ba2" stroke-width="1.5" opacity="0.6"/>
                <circle cx="6" cy="8" r="2" fill="#764ba2" opacity="0.3"/>
                <circle cx="18" cy="16" r="2" fill="#667eea" opacity="0.3"/>
               </svg>""",
        "description": """
        Users can answer the same feeling thermometer questions from the ANES 2024 survey to see how their ratings compare to the general US public. 
        
        After providing your ratings, density plots are generated and faceted by different demographic and political inputs, showing your personal rating 
        positioned relative to the broader population's responses. This allows you to see where you fall on the spectrum of American political attitudes.
        """,
        "button_text": "Compare Yourself to the US",
        "page": "pages/3_Rate_and_Compare.py",
        "key": "rc_button"
    }
    ]

    for page in PAGES:
        st.markdown(f"""
            <h2>{page['title']}</h2>
            <p>{page['description']}</p>
        """, unsafe_allow_html=True)

st.divider()
st.markdown(
    "This project was created as part of a research collaboration with the "
    "[**Duke University Polarization Lab**](https://www.polarizationlab.com/) "
    "using data from [**American National Election Studies**](https://electionstudies.org/)."
)
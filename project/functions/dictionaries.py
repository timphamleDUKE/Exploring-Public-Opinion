import pandas as pd
import streamlit as st
import os

# Setting logo
def set_logo():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, '..', 'images', 'logos', 'polarization-logo.png')

    st.set_page_config(layout="wide")

    st.logo(
        image=logo_path,
        icon_image=logo_path,
        link = "https://www.polarizationlab.com/",
        size = "large"
    )

    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 600px;
        }
        img[data-testid="stLogo"],
        div[data-testid="stSidebarHeader"] > img,
        div[data-testid="collapsedControl"] > img {
            height: 50px !important;
            width: auto;
        }
    </style>
    """, unsafe_allow_html=True)


# Dataframe
script_dir = os.path.dirname(os.path.abspath(__file__))

df_path = os.path.join(script_dir, '..', '..', 'data', 'anes_2024_clean.csv')
df = pd.read_csv(df_path)

codebook_path = os.path.join(script_dir, '..', '..', 'data', 'codebook.csv')
codebook = pd.read_csv(codebook_path)


# List of thermometer questions
thermometer_codebook = codebook[(codebook["Category"] == "Feeling Thermometer")]
list_of_thermometer = thermometer_codebook["Renamed"]
list_of_thermometer_topics = thermometer_codebook["Topic"].dropna().unique().tolist()
list_of_thermometer_topics = sorted([t for t in list_of_thermometer_topics if t != "Other"]) + ["Other"]

topic_to_list_of_thermometer_map = (
    thermometer_codebook.groupby("Topic")["Dropdown Text"]
    .apply(lambda x: x.dropna().tolist())
    .to_dict()
)


# List of issue questions
issue_codebook = codebook[(codebook["Category"] == "Issue Position")]
list_of_issues = issue_codebook["Renamed"]

list_of_issue_topics = issue_codebook["Topic"].dropna().unique().tolist()
list_of_issue_topics = sorted([t for t in list_of_issue_topics if t != "Other"])

topic_to_list_of_issue_map = (
    issue_codebook.groupby("Topic")["Description"]
    .apply(lambda x: x.dropna().tolist())
    .to_dict()
)


# List of colors based on group by
political_colors = {
    "Democrat": "blue",
    "Republican": "red",
    "Independent": "green",
    "N/A": "rgb(141, 142, 147)"
}

political_fill_colors = {
    "Democrat": "rgba(0, 0, 255, 0.3)",     # Blue
    "Republican": "rgba(255, 0, 0, 0.3)",     # Red
    "Independent": "rgba(0, 128, 0, 0.3)",  # Green
    "N/A": "rgba(141, 142, 147, 0.3)"
}

ideological_colors = {
    "Liberal": "blue",
    "Conservative": "red",
    "Moderate": "rgb(141, 142, 147)",
    "Other": "green"
}

ideological_fill_colors = {
    "Liberal": "rgba(0, 0, 255, 0.3)",     # Blue
    "Conservative": "rgba(255, 0, 0, 0.3)",     # Red
    "Moderate": "rgba(141, 142, 147, 0.3)",  # Green
    "Other": "rgba(0, 128, 0, 0.3)"
}

target_label_map = {
    -9: "Refused",
    -8: "Don’t know",
    -1: "Inapplicable",
    1: "Extremely willing",
    2: "Very willing",
    3: "Moderately willing",
    4: "A little willing",
    5: "Not at all willing"
}


# Density plot mapping
def map_group_info(df, group):
    if group == "Ideological Groups":
        df["party"] = df["lib_con_7pt"].map({
            1: "Liberal", 2: "Liberal", 3: "Liberal",
            4: "Moderate",
            5: "Conservative", 6: "Conservative", 7: "Conservative",
            99: "Other", -4: "Other", -9: "Other"
        }).fillna("N/A")
        colors = ideological_colors
        fill_colors = ideological_fill_colors

    elif group == "Political Groups":
        df["party"] = df["poli_party_self_7pt"].map({
            1: "Democrat", 2: "Democrat",
            3: "Independent", 4: "Independent", 5: "Independent",
            6: "Republican", 7: "Republican",
            -9: "N/A", -4: "N/A", -1: "N/A"
        }).fillna("N/A")
        colors = political_colors
        fill_colors = political_fill_colors

    else:
        raise ValueError("Invalid group type.")

    return df, colors, fill_colors



# Descriptions
description_map = dict(zip(codebook["Renamed"], codebook["Description"]))
full_description_map = dict(zip(codebook["Renamed"], codebook["Original Question"]))
description_to_renamed = dict(zip(codebook["Description"], codebook["Renamed"]))
dropdown_to_renamed = dict(zip(codebook["Dropdown Text"], codebook["Renamed"]))


# Sankey Color Mapping
sankey_colors = {
    1: "rgba(0,0,255,0.3)", # Blue
    2: "rgba(255,0,0,0.3)", # Red
    3: "rgba(160,160,160,0.3)" # Grey
}

lib_con_map_3pt = {
    1: "Liberal",
    2: "Conservative",
    3: "Moderate"
}

political_map_3pt = {
    1: "Democrat",
    2: "Republican",
    3: "Independent"
}

def find_weight_col(question):
    prepost = codebook.loc[codebook["Renamed"] == question, "Pre/Post"].iloc[0]
    return "pre_full" if prepost == "Pre" else "post_full"

def find_answer_choices(question):
    df = codebook[codebook["Renamed"] == question]["Answer Choices"]

    df_text = df.iloc[0]

    # Split into lines and parse each line
    answer_map = {}
    for line in df_text.strip().split("\n"):
        if "." in line:
            key, value = line.strip().split(".", 1)
            try:
                answer_map[int(key.strip())] = value.strip()
            except ValueError:
                continue  # Skip if the key isn't an int
    return answer_map

def wrap_title(title, max_length=85):
    if len(title) <= max_length:
        return title
    
    words = title.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

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
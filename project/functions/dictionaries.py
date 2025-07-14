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
    "Independent": "rgb(141, 142, 147)",
    "N/A": "green"
}

political_fill_colors = {
    "Democrat": "rgba(0, 0, 255, 0.3)",     # Blue
    "Republican": "rgba(255, 0, 0, 0.3)",     # Red
    "Independent": "rgba(141, 142, 147, 0.3)",  # grey
    "N/A": "rgba(0, 128, 0, 0.3)" # green
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
    "Moderate": "rgba(141, 142, 147, 0.3)",  # Grey
    "Other": "rgba(0, 128, 0, 0.3)" # Green
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
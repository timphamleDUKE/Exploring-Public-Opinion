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


# Demographics Mapping
demographics_codebook = codebook[(codebook["Category"] == "Social Characteristics")]
list_of_demographics = demographics_codebook["Renamed"].dropna().unique().tolist()

def build_age_facet_map(df):
    def map_age_to_group(age):
        if pd.isna(age):
            return None
        elif age < 30:
            return "18-29"
        elif age < 45:
            return "30-44"
        elif age < 60:
            return "45-59"
        else:
            return "60+"

    return df["age_election_day"].apply(map_age_to_group)
age_valid_facet_values = ["18-29", "30-44", "45-59", "60+"]

educ_facet_map = {
    -9: None,
    -8: None,
    -4: None,
    -2: None,
    1: "Non-college",
    2: "Non-college",
    3: "Non-college",
    4: "College grad+",
    5: "College grad+"
}
educ_valid_facet_values = ["Non-college", "College grad+"]

marriage_facet_map = {
    -2: None,
    1: "Married",
    2: "Widowed", 
    3: "Divorced", 
    4: "Separated", 
    5: "Never Married"
}
marriage_valid_facet_values = ["Married", "Widowed", "Divorced", "Separated", "Never Married"]

income_facet_map = {
    -9: None, 
    -5: None,
    -4: None,
    1: "Under $9,999",
    2: "$10,000 to $29,999",
    3: "$30,000 to $59,999",
    4: "$60,000 to $99,999",
    5: "$100,000 to $249,999",
    6: "$250,000 or more"
}
income_valid_facet_values = ["Under $9,999", "$10,000 to $29,999", "$30,000 to $59,999", "$60,000 to $99,999", "$100,000 to $249,999", "$250,000 or more"]

religion_facet_map = {
    -9: None,
    -8: None,
    -1: None,
    1: "Religious",
    2: "Religious",
    3: "Religious",
    4: "Religious",
    5: "Religious",
    6: "Religious",
    7: "Religious",
    8: "Religious",
    9: "Non-Religious",
    10: "Non-Religious",
    11: "Religious",
    12: "Non-Religious"
}
religion_valid_facet_values = ["Religious", "Non-Religious"]

gender_facet_map = {
    -9: None,
    -1: None,
    1: "Man",
    2: "Woman",
    3: "Other",
    4: "Other"
}
gender_valid_facet_values = ["Man", "Woman", "Other"]

race_ethnicity_facet_map_plot = {
    -9: None,
    -8: None,
    -4: None,
    1: "White, non-Hispanic",
    2: "Black, non-Hispanic",
    3: "Hispanic",
    4: "Asian or Native Hawaiian/other Pacific Islander, <br> non-Hispanic",
    5: "Native American/Alaska Native or other race, <br> non-Hispanic",
    6: "Multiple races, non-Hispanic"
}
race_ethnicity_valid_facet_values_plot = ["White, non-Hispanic", "Black, non-Hispanic", "Hispanic", "Asian or Native Hawaiian/other Pacific Islander, <br> non-Hispanic", "Native American/Alaska Native or other race, <br> non-Hispanic", "Multiple races, non-Hispanic"]

race_ethnicity_facet_map = {
    -9: None,
    -8: None,
    -4: None,
    1: "White, non-Hispanic",
    2: "Black, non-Hispanic",
    3: "Hispanic",
    4: "Asian or Native Hawaiian/other Pacific Islander, non-Hispanic",
    5: "Native American/Alaska Native or other race, non-Hispanic",
    6: "Multiple races, non-Hispanic"
}
race_ethnicity_valid_facet_values = ["White, non-Hispanic", "Black, non-Hispanic", "Hispanic", "Asian or Native Hawaiian/other Pacific Islander, non-Hispanic", "Native American/Alaska Native or other race, non-Hispanic", "Multiple races, non-Hispanic"]

# Facet configuration map
facet_config = {
    "age_election_day": {
        "map_func": build_age_facet_map,
        "valid_values": age_valid_facet_values
    },
    "educ": {
        "map": educ_facet_map,
        "valid_values": educ_valid_facet_values
    },
    "marriage": {
        "map": marriage_facet_map,
        "valid_values": marriage_valid_facet_values
    },
    "income": {
        "map": income_facet_map,
        "valid_values": income_valid_facet_values
    },
    "religion": {
        "map": religion_facet_map,
        "valid_values": religion_valid_facet_values
    },
    "gender": {
        "map": gender_facet_map,
        "valid_values": gender_valid_facet_values
    },
    "race_ethnicity": {
        "map": race_ethnicity_facet_map,
        "valid_values": race_ethnicity_valid_facet_values,
        "map_plot": race_ethnicity_facet_map_plot,
        "valid_values_plot": race_ethnicity_valid_facet_values_plot,
    }
}

facet_display_map = {
    "age_election_day": "Age",
    "educ": "Education",
    "marriage": "Marital Status",
    "income": "Income",
    "religion": "Religion",
    "gender": "Gender",
    "race_ethnicity": "Race/Ethnicity"
}

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
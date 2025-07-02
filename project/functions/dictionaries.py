import pandas as pd
import streamlit as st

# Setting logo
def set_logo():
    logo = "images/logos/polarization-logo.PNG"

    st.set_page_config(layout="wide")

    st.logo(
        image=logo,
        icon_image=logo,
        link = "https://www.polarizationlab.com/",
        size = "large"
    )

    # Size of sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                width: 600px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Size of logo
    st.markdown(
    """
    <style>
      img[data-testid="stLogo"] {
          height: 50px !important;
          width: auto;
      }
      div[data-testid="stSidebarHeader"] > img,
      div[data-testid="collapsedControl"] > img {
          height: 50px !important;
          width: auto;
      }
    </style>
    """,
    unsafe_allow_html=True
    )


# Dataframe
df = pd.read_csv("../data/anes_2024_clean.csv")
codebook = pd.read_csv("../data/codebook.csv")


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
    "Democratic Party": "blue",
    "Republican Party": "red",
    "Independent": "green",
    "N/A": "rgb(141, 142, 147)"
}

political_fill_colors = {
    "Democratic Party": "rgba(0, 0, 255, 0.3)",     # Blue
    "Republican Party": "rgba(255, 0, 0, 0.3)",     # Red
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
    if codebook[codebook["Renamed"] == question]["Pre/Post"].iloc[0] == "Pre":
        weight_col = "pre_full"
    else:
        weight_col = "post_full"
    return weight_col

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
marriage_valid_facet_values = ["Under $9,999", "$10,000 to $29,999", "$30,000 to $59,999", "$60,000 to $99,999", "$100,000 to $249,999", "$250,000 or more"]

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

race_ethnicity_facet_map = {
    -9: None,
    -8: None,
    -4: None,
    1: "White, non-Hispanic",
    2: "Black, non-Hispanic",
    3: "Hispanic",
    4: "Other/Multiple races, non-Hispanic",
    5: "Other/Multiple races, non-Hispanic",
    6: "Other/Multiple races, non-Hispanic"
}
race_ethnicity_valid_facet_values = ["White, non-Hispanic", "Black, non-Hispanic", "Hispanic", "Other/Multiple races, non-Hispanic"]
import pandas as pd
import streamlit as st

# Setting logo
def set_logo():
    logo = "images/logo-black.PNG"

    st.logo(
        image=logo,
        icon_image=logo,
        link = "https://www.polarizationlab.com/",
        size = "large"
    )

    st.set_page_config(
        layout = "wide"
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
    thermometer_codebook.groupby("Topic")["Description"]
    .apply(lambda x: x.dropna().tolist())
    .to_dict()
)


# List of issue questions
issue_codebook = codebook[(codebook["Category"] == "Issue Position")]
list_of_issues = issue_codebook["Renamed"]

list_of_issue_topics = issue_codebook["Topic"].dropna().unique().tolist()
list_of_issue_topics = sorted([t for t in list_of_issue_topics if t != "Other"]) + ["Other"]

topic_to_list_of_issue_map = (
    issue_codebook.groupby("Topic")["Description"]
    .apply(lambda x: x.dropna().tolist())
    .to_dict()
)

# List of colors based on group by
colors = {
    "Democratic Party": "blue",
    "Republican Party": "red",
    "Other": "green",
    "N/A": "rgb(141, 142, 147)"
}

fill_colors = {
    "Democratic Party": "rgba(0, 0, 255, 0.3)",     # Blue
    "Republican Party": "rgba(255, 0, 0, 0.3)",     # Red
    "Other": "rgba(0, 128, 0, 0.3)",  # Green
    "N/A": "rgba(141, 142, 147, 0.3)"

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

# Ideology color mappin
lib_con_2pt = {
    1: "rgba(0,0,255,0.3)",
    2: "rgba(255,0,0,0.3)"
}

lib_con_7pt = {
    1: "rgba(0,0,255,0.3)",
    2: "rgba(64,96,255,0.3)",
    3: "rgba(128,160,255,0.3)",
    4: "rgba(160,160,160,0.3)",
    5: "rgba(255,160,128,0.3)",
    6: "rgba(255,96,64,0.3)",
    7: "rgba(255,0,0,0.3)",
}

lib_con_map_2pt = {
    1: "Liberal",
    2: "Conservative"
}

lib_con_map_7pt = {
    1: "Extremely liberal",
    2: "Liberal",
    3: "Slightly Liberal",
    4: "Moderate",
    5: "Slightly Conservative",
    6: "Conservative",
    7: "Extremely Conservative"
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
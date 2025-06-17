import pandas as pd
import streamlit as st

# Setting logo
def set_logo():
    logo = "images/logo-black.PNG"
    data_plus_logo = "images/data+.png"

    st.logo(
        image=logo,
        icon_image=logo,
        size = "large"
    )

# Dataframe
df = pd.read_csv("../data/anes_2024_clean.csv")
codebook = pd.read_csv("../data/codebook.csv")

# List of thermometer questions
list_of_thermometer = codebook[(codebook["Category"] == "Feeling Thermometer")]
list_of_thermometer = list_of_thermometer["Renamed"]

# List of issue questions
list_of_issues = codebook[(codebook["Category"] == "Issue Position")]
list_of_issues = list_of_issues["Renamed"]

# List of colors based on group by
colors = {
    "Democratic Party": "blue",
    "Republican Party": "red",
    "None/Independent Party": "green"
}

fill_colors = {
    "Democratic Party": "rgba(0, 0, 255, 0.3)",     # Blue
    "Republican Party": "rgba(255, 0, 0, 0.3)",     # Red
    "None/Independent Party": "rgba(0, 128, 0, 0.3)"  # Green
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
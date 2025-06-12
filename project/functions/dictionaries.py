import pandas as pd
import streamlit as st

# Setting logo
def set_logo():
    logo = "images/logo-black.PNG"
    data_plus_logo = "images/data+.png"

    st.logo(
        image=logo,
        link="https://your-company-website.com", 
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

lib_con_map = {
    1: "Extremely liberal",
    2: "Liberal",
    3: "Slightly Liberal",
    4: "Moderate",
    5: "Slightly Conservative",
    6: "Conservative",
    7: "Extremely Conservative"
}

# Descriptions
description_map = dict(zip(codebook['Renamed'], codebook['Description']))

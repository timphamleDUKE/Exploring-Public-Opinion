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

# List of thermometer questions
list_of_thermometer = (
    "harris_thermometer_pre",
    "trump_thermometer_pre",
    "biden_thermometer_pre",
    "vance_thermometer_pre",
    "democrat_thermometer_pre",
    "republican_thermometer_pre",
    "harris_thermometer_post",
    "trump_thermometer_post",
    "walz_thermometer_post",
    "vance_thermometer_post",
    "biden_thermometer_post",
    "christian_fundamentalists_thermometer",
    "feminists_thermometer",
    "liberals_thermometer",
    "labor_unions_thermometer",
    "big_business_thermometer",
    "conservatives_thermometer",
    "supreme_court_thermometer",
    "lgbt_thermometer",
    "congress_thermometer",
    "muslims_thermometer",
    "christians_thermometer",
    "maga_thermometer",
    "jews_thermometer",
    "police_thermometer",
    "transgender_thermometer",
    "blm_thermometer",
    "nra_thermometer",
    "fbi_thermometer",
    "rural_thermometer",
    "planned_parenthood_thermometer",
    "asian_thermometer",
    "hispanic_thermometer",
    "black_thermometer",
    "illegal_immigrant_thermometer",
    "white_thermometer",
)

list_of_issues = (
    "abortion",
    "death_penalty",
    "us_world_involvement",
    "international_force",
    "voting_id",
    "voting_felons",
    "journalists",
    "climate_inc_temps",
    "paid_leave",
    "transgender_bathrooms",
    "transgender_sports",
    "birthright_citizenship",
    "lgbt_discrimination",
    "lgbt_adoption",
    "gay_marriage",
    "children_immigrants",
    "mexico_wall",
    "ukraine_russia",
    "israel",
    "palestine_aid",
    "israel_palestine",
    "gaza_protests",
    "political_violence",
    "import_limits",
    "immigration_levels",
    "immigration_jobs",
    "immigration_crime",
    "immigration_citizenship",
    "immigration_economy",
    "immigration_customs",
    "hiring_black",
    "affirmative_action",
    "gov_involvement",
    "gov_regulation",
    "income_inequality",
    "equal_opportunity",
    "gender_roles",
    "budget_deficit",
    "tax_millionaires",
    "vaccines_schools",
    "obamacare",
    "climate_temps",
    "climate_regulate_emissions",
    "gun_difficulty",
    "gun_background_checks",
    "gun_ban_assault_rifles",
    "opioid_epidemic",
    "police_force",
    "free_trade",
    "diversity",
    "federal_min_wage",
    "budget_healthcare",
    "vaccines",
    "sexual_harassment",
    "transgender_military",
    "china_threat",
    "russia_threat",
    "mexico_threat",
    "iran_threat",
    "japan_threat",
    "israel_threat"
)

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
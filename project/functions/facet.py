from functions.dictionaries import codebook
import pandas as pd

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
    1: "Less than high school credential",
    2: "High school credential",
    3: "Some post-high school, no bachelor’s degree",
    4: "Bachelor’s degree",
    5: "Graduate degree"
}
educ_valid_facet_values = ["Less than high school credential", "High school credential", "Some post-high school, no bachelor’s degree", "Bachelor’s degree", "Graduate degree"]

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
    "gender": {
        "map": gender_facet_map,
        "valid_values": gender_valid_facet_values
    },
    "race_ethnicity": {
        "map": race_ethnicity_facet_map,
        "valid_values": race_ethnicity_valid_facet_values,
        "map_plot": race_ethnicity_facet_map_plot,
        "valid_values_plot": race_ethnicity_valid_facet_values_plot,
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
    }
}

facet_display_map = {
    "age_election_day": "Age",
    "gender": "Gender",
    "race_ethnicity": "Race/Ethnicity",
    "educ": "Education",
    "marriage": "Marital Status",
    "income": "Income",
    "religion": "Religion"
}
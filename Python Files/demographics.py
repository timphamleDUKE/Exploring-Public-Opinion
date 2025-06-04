import pandas as pd

study = "CES"
year = 2024

study_file_path = f"Streamlit/data/{study}_{year}.csv"
study_df = pd.read_csv(study_file_path, low_memory=False)

rename_dicts = {
    ("ANES", 2024): {
        "V240107a": "pre_full",
        "V240107b": "post_full",
        "V240107c": "full_var_psu",
        "V240107d": "full_var_stratum",

        "V241458x": "birth",
        "V241025": "poli_party_reg",
        "V241221": "poli_party_self3",
        "V241226": "poli_party_self7",
        "V241463": "educ",
        "V241483": "employ",
        "V241459": "marstat",
        "V241567x": "faminc_new",
        "V241422": "religion",
        "V241551": "gender",
        "V241501x": "race",
        "V241017": "input_state",
        "V242341": "urban_rural"
    },
    "CES": {
        "pid3": "poli_party_self3",
        "pid7": "poli_party_self7",
        "religpew": "religion",
        "inputstate": "input_state",
        "urbancity": "urban_rural",
        "gender4": "gender"
    },
    ("CES", 2024): {
        "CC24_361b": "poli_party_reg"
    }
}

if study in rename_dicts:
    study_df = study_df.rename(columns=rename_dicts[(study)])

if (study, year) in rename_dicts:
    study_df = study_df.rename(columns=rename_dicts[(study, year)])

select_cols = [
    "commonweight",
    "commonpostweight",
    
    "birthyr",
    "poli_party_reg",
    "poli_party_self3",
    "poli_party_self7",
    "educ",
    "employ",
    "marstat",
    "faminc_new",
    "religion",
    "gender",
    "race",
    "input_state",
    "urban_rural"
]

other_cols = [col for col in study_df.columns if col not in select_cols]

study_df = study_df[select_cols + other_cols]

study_df.to_csv("Streamlit/data/CES_2024_clean.csv", index=False)


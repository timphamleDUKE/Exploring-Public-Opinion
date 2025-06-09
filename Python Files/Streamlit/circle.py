import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Survey Navigator",
    layout="wide"
)

def set_logo():
    logo = "images/logo-black.PNG"
    data_plus_logo = "images/data+.png"

    st.logo(
        image=logo,
        link="https://your-company-website.com", 
        icon_image=logo,
        size = "large"
    )

set_logo()

# Load + clean data
df = pd.read_csv("../../data/anes_2024_clean.csv")
df.columns = df.columns.str.strip()

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

thermometer_question = st.selectbox("Question", list_of_thermometer)

df_filtered = df[['poli_party_reg', thermometer_question]].dropna()
party_map = {1: 'Democrat', 2: 'Republican', 4: 'None/Independent'}
df_filtered = df_filtered[df_filtered['poli_party_reg'].isin(party_map)]
df_filtered['party'] = df_filtered['poli_party_reg'].map(party_map)
df_filtered['rating'] = df_filtered[thermometer_question]

st.write(df_filtered)
st.write(df[df['poli_party_reg'] == 1].shape[0])
st.write(df[df['poli_party_reg'] == 2].shape[0])
st.write(df[df['poli_party_reg'] == 4].shape[0])

# Sort and assign angles

repub_df = df_filtered[df_filtered['rating'] > 0].reset_index(drop=True)
dem_df = df_filtered[df_filtered['rating'] > 0].reset_index(drop=True)
ind_df = df_filtered[df_filtered['rating'] > 0].reset_index(drop=True)

repub_df = df_filtered[df_filtered['party'] == 'Republican'].reset_index(drop=True)
dem_df = df_filtered[df_filtered['party'] == 'Democrat'].reset_index(drop=True)
ind_df = df_filtered[df_filtered['party'] == 'None/Independent'].reset_index(drop=True)

repub_df['theta'] = np.linspace(0, 120, len(repub_df), endpoint=False)
dem_df['theta'] = np.linspace(120, 240, len(dem_df), endpoint=False)
ind_df['theta'] = np.linspace(240, 360, len(ind_df), endpoint=False)

st.write(df_filtered)
st.write(df_filtered[df_filtered['poli_party_reg'] == 1].shape[0])
st.write(df_filtered[df_filtered['poli_party_reg'] == 2].shape[0])
st.write(df_filtered[df_filtered['poli_party_reg'] == 4].shape[0])


# Radius: higher rating = closer to center
repub_df['r'] = 1 - (repub_df['rating'] / 100)
dem_df['r'] = 1 - (dem_df['rating'] / 100)
ind_df['r'] = 1 - (ind_df['rating'] / 100)
df_polar = pd.concat([repub_df, dem_df, ind_df])

# Build figure
fig = go.Figure()

# Inner rating dots
fig.add_trace(go.Scatterpolar(
    r=df_polar['r'],
    theta=df_polar['theta'],
    mode='markers',
    marker=dict(
        size=4, 
        opacity = 0.5,
        color=df_polar['party'].map(
            {'Republican': 'red',
            'Democrat': 'blue',
            'None/Independent': 'green'}
             )),
    hoverinfo='text'
))

# Create concentric rings and optional sector guides using tick marks
fig.update_layout(
    title=f"Target-Style Polar Chart: Thermometer Ratings by Party on {thermometer_question}",
    polar=dict(
        bgcolor="white",
        angularaxis=dict(
            tickmode="array",
            tickvals=[0,120,240],
            visible=True,
            showline=False,
            showticklabels=False,
            ticks='',
            rotation=90,
            direction="clockwise"
        ),
        radialaxis=dict(
            visible=True,
            showline=False,
            showticklabels=True,
            ticks='',
            range=[0, 1],
            tickmode = "array",
            tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
            ticktext=['80', '60', '40', '20', '0'],  # reversed
            tickcolor = "black",
            tickfont = dict(
                color = "black",
                size = 15
            ),
            showgrid=True,
            gridcolor="black",
            gridwidth = 1
        ),
    ),
    width=800,
    height=800,
    showlegend=False
)

fig.add_annotation(
    x=0.5, y=1.1, xref='paper', yref='paper',
    text="Republicans", showarrow=False, font=dict(size=14, color='red')
)
fig.add_annotation(
    x=0.1, y=0.1, xref='paper', yref='paper',
    text="Democrats", showarrow=False, font=dict(size=14, color='blue')
)
fig.add_annotation(
    x=0.9, y=0.1, xref='paper', yref='paper',
    text="Independents", showarrow=False, font=dict(size=14, color='green')
)


st.write(fig)
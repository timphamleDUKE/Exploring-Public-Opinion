import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# Streamlit setup
st.title("MAGA Thermometer Distribution by Party (Interactive)")
st.write("Interactive density plot of MAGA thermometer ratings for Democrats, Republicans, and Independents.")

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

question = st.selectbox("Question", list_of_thermometer)

anes_2024_sunshine = pd.read_csv("../../data/anes_2024_clean.csv")

# Create party labels
anes_2024_sunshine["party"] = anes_2024_sunshine["poli_party_reg"].map({
    1: "Democratic",
    2: "Republican",
    4: "None/Independent"
})

# Filter valid data
df = anes_2024_sunshine[
    (anes_2024_sunshine["party"].isin(["Democratic", "Republican", "None/Independent"])) &
    (anes_2024_sunshine[question] >= 0) &
    (anes_2024_sunshine[question] <= 100)
]

# Colors for each party
colors = {
    "Democratic": "blue",
    "Republican": "red",
    "None/Independent": "green"
}

# Create figure
fig = go.Figure()

fill_colors = {
    'Democratic': 'rgba(0, 0, 255, 0.3)',     # Blue
    'Republican': 'rgba(255, 0, 0, 0.3)',     # Red
    'None/Independent': 'rgba(0, 128, 0, 0.3)'  # Green
}

# Add KDE traces for each party
for party in ["Democratic", "Republican", "None/Independent"]:
    values = df[df["party"] == party][question].dropna().values

    # Compute KDE
    kde = gaussian_kde(values)
    x_range = np.linspace(0, 100, 500)
    y_values = kde(x_range)

    # Add filled trace
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_values,
        mode="lines",
        name=party,
        line=dict(color=colors[party], width=2),
        fill="tozeroy",
        fillcolor=fill_colors.get(party, 'rgba(128, 128, 128, 0.3)')
    ))

# Layout settings
fig.update_layout(
    title=f"Overlayed Density of {question} Thermometer Ratings by Party",
    xaxis_title="Thermometer Rating (0–100)",
    yaxis_title="Density",
    xaxis=dict(tickmode="linear", tick0=0, dtick=20),
    hovermode="x unified",
    template="simple_white"
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
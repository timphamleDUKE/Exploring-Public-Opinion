import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from functions.dictionaries import *

def densityGraph(df, question, groups):
    # Make party labels
    df["party"] = df["poli_party_reg"].map({
        1: "Democratic Party",
        2: "Republican Party",
        4: "None/Independent Party"
    })

    # Filter the valid data
    df = df[
        (df["party"].isin(groups)) &
        (df[question] >= 0) &
        (df[question] <= 100)
    ]

    fig = go.Figure()

    # Add KDE traces for each party
    for party in groups:
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

    list_groups_joined = ", ".join(groups)

    # Layout settings
    fig.update_layout(
        title=f"Overlayed Density of {question} Thermometer Ratings by {list_groups_joined}",
        xaxis_title="Thermometer Rating (0–100)",
        yaxis_title="Density",
        xaxis=dict(tickmode="linear", tick0=0, dtick=20),
        hovermode="x unified",
        template="simple_white"
    )

    return fig

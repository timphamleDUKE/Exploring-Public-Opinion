import streamlit as st
import plotly.graph_objects as go
from functions.dictionaries import *
from functions.weights import get_anes_weighted_density_data

def densityGraph(df, question, groups, group, title=None, yaxis_range=None):

    # Map group values
    if group == "Ideological Groups":
        df["party"] = df["lib_con_7pt"].map({
            1: "Liberal", 2: "Liberal", 3: "Liberal",
            4: "Moderate",
            5: "Conservative", 6: "Conservative", 7: "Conservative",
            99: "Other", -4: "Other", -9: "Other"
        }).fillna("N/A")
        colors = ideological_colors
        fill_colors = ideological_fill_colors

    elif group == "Political Groups":
        df["party"] = df["poli_party_reg"].map({
            1: "Democratic Party", 2: "Republican Party",
            4: "Other", 5: "Other", -8: "Other", -9: "N/A"
        }).fillna("N/A")
        colors = political_colors
        fill_colors = political_fill_colors

    # Filter the data
    df = df[
        (df["party"].isin(groups)) &
        (df[question] >= 0) &
        (df[question] <= 100)
    ]

    # Create plot
    fig = go.Figure()

    try:
        plotting_data = get_anes_weighted_density_data(
            df, question, groups, group_var="party", seed=12345
        )

        for party in groups:
            if party in plotting_data:
                x_range = plotting_data[party]["x_range"]
                y_values = plotting_data[party]["y_values"]

                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=y_values,
                    mode="lines",
                    name=party,
                    line=dict(color=colors[party], width=2),
                    fill="tozeroy",
                    fillcolor=fill_colors.get(party, "rgba(128,128,128,0.3)")
                ))

    except Exception as e:
        st.error(f"Error generating weighted density plot: {e}")
        return go.Figure()  # return an empty figure on error

    # Layout settings
    fig.update_layout(
        title=dict(
            text = title if title else "",
            font = dict(size = 24)
        ),
        xaxis_title=dict(text="Thermometer Rating (0–100)", font=dict(size=24)),
        yaxis_title=dict(text="Density", font=dict(size=24)),
        xaxis=dict(tickmode="linear", tick0=0, dtick=20, tickfont=dict(size=20)),
        yaxis=dict(
            tickfont=dict(size=20), 
            range=yaxis_range
            ),
        legend=dict(font=dict(size=20)),
        hovermode="x unified",
        template="simple_white",
        font=dict(size=20)
    )

    return fig


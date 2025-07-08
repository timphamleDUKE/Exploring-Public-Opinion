import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functions.dictionaries import *
from functions.weights import get_anes_weighted_density_data
import math

def densityGraph(df, question, groups, group, title=None, yaxis_range=None):

    df, colors, fill_colors = map_group_info(df, group)
    df = df[df[question].between(0, 100)]

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
            text=title or "",
            font=dict(size=24, weight=100)
        ),
        xaxis=dict(
            title=dict(text="Thermometer Rating (0–100)", font=dict(size=20)),
            tickmode="linear",
            tick0=0,
            dtick=20,
            tickfont=dict(size=18)
        ),
        yaxis=dict(
            title=dict(text="Density", font=dict(size=20)),
            tickfont=dict(size=18),
            range=yaxis_range
        ),
        legend=dict(font=dict(size=18)),
        hovermode="x unified",
        template="simple_white",
        font=dict(size=18)
    )

    return fig


def densityGraphFaceted(df, question, groups, group, facet_var, facet_map, valid_facet_values=None, title=None):
    # 1. Apply facet mapping
    df["facet_label"] = df[facet_var].map(facet_map)
    df = df[df["facet_label"].notna()]
    if valid_facet_values:
        df = df[df["facet_label"].isin(valid_facet_values)]

    # 2. Apply group mappings and filter
    df, colors, fill_colors = map_group_info(df, group)
    df = df[df["party"].isin(groups) & df[question].between(0, 100)]

    facet_values = [val for val in valid_facet_values if val in df["facet_label"].unique()]
    n_facets = len(facet_values)

    # 3. Determine layout
    rows = 1 if n_facets <= 3 else 2
    cols = n_facets if rows == 1 else math.ceil(n_facets / 2)

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=facet_values,
        shared_yaxes="all",
        vertical_spacing=0.25 if rows > 1 else 0.05
    )

    # 4. Add density traces
    try:
        for i, facet_value in enumerate(facet_values):
            row = (i // cols) + 1
            col = (i % cols) + 1
            df_facet = df[df["facet_label"] == facet_value]

            for party in groups:
                df_party = df_facet[df_facet["party"] == party]
                if df_party[question].dropna().nunique() < 2:
                    st.warning(f"Not enough variation for '{party}' in {facet_var} group '{facet_value}' — skipping.")
                    continue

                plotting_data = get_anes_weighted_density_data(
                    df_party,
                    question,
                    [party],
                    group_var="party",
                    seed=12345
                )

                if party not in plotting_data:
                    st.warning(f"No KDE data for '{party}' in {facet_var} group '{facet_value}'")
                    continue

                fig.add_trace(go.Scatter(
                    x=plotting_data[party]["x_range"],
                    y=plotting_data[party]["y_values"],
                    mode="lines",
                    name=party,
                    legendgroup=party,
                    showlegend=(i == 0),
                    line=dict(color=colors.get(party, "gray"), width=2),
                    fill="tozeroy",
                    fillcolor=fill_colors.get(party, "rgba(128,128,128,0.3)")
                ), row=row, col=col)

    except Exception as e:
        st.error(f"Error generating weighted density plot: {e}")
        return go.Figure()

    # 5. Update layout
    fig.update_layout(
        title=dict(text=title or "", font=dict(size=24)),
        template="simple_white",
        font=dict(size=18),
        yaxis_title = "Density",
        hovermode="x unified",
        legend=dict(font=dict(size=14)),
        height=700 if rows > 1 else 450
    )

    # 6. Axis titles for all subplots
    for i in range(len(facet_values)):
        suffix = "" if i == 0 else str(i + 1)
        fig.layout[f"xaxis{suffix}"].title = "Thermometer Rating (0–100)"

    return fig

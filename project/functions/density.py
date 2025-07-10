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

def densityGraphFaceted(df, question, groups, group, facet_var, facet_map, valid_facet_values=None, title=None, user_rating=None):

    # 1) facet‐map and filter
    df["facet_label"] = df[facet_var].map(facet_map)
    df = df[df["facet_label"].notna()]
    if valid_facet_values:
        df = df[df["facet_label"].isin(valid_facet_values)]

    # 2) group map and filter
    df, colors, fill_colors = map_group_info(df, group)
    df = df[df["party"].isin(groups) & df[question].between(0, 100)]

    # 3) get valid facet values that exist in filtered data
    facet_values = [v for v in (valid_facet_values or []) if v in df["facet_label"].unique()]
    n = len(facet_values)

    # Protect against empty facet_values
    if n == 0:
        st.warning("No data available for the selected facet values.")
        return go.Figure()

    # 4) layout
    rows = 1 if n <= 3 else 2
    cols = max(1, n) if rows == 1 else max(1, math.ceil(n / 2))

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=facet_values,
        shared_yaxes="all",
        vertical_spacing=0.25 if rows > 1 else 0.05
    )

    # 5) draw density traces
    max_y = [0] * n
    for i, val in enumerate(facet_values):
        row = (i // cols) + 1
        col = (i % cols) + 1
        df_f = df[df["facet_label"] == val]

        for party in groups:
            df_p = df_f[df_f["party"] == party]
            if df_p[question].dropna().nunique() < 2:
                continue

            data = get_anes_weighted_density_data(
                df_p, question, [party], group_var="party", seed=12345
            ).get(party)

            if not data:
                continue

            fig.add_trace(
                go.Scatter(
                    x=data["x_range"],
                    y=data["y_values"],
                    mode="lines",
                    name=party,
                    legendgroup=party,
                    showlegend=(i == 0),
                    line=dict(color=colors.get(party, "gray"), width=2),
                    fill="tozeroy",
                    fillcolor=fill_colors.get(party, "rgba(128,128,128,0.3)")
                ),
                row=row, col=col
            )
            max_y[i] = max(max_y[i], max(data["y_values"]))

    # 6) add user-rating line
    if user_rating is not None:
        for i in range(n):
            row = (i // cols) + 1
            col = (i % cols) + 1
            fig.add_trace(
                go.Scatter(
                    x=[user_rating, user_rating],
                    y=[0, max_y[i]],
                    mode="lines",
                    line=dict(color="black", dash="dash"),
                    showlegend=False,
                    hoverinfo="skip"
                ),
                row=row, col=col
            )

    # 7) layout and labels
    fig.update_layout(
        title=dict(text=title or "", font=dict(size=24)),
        template="simple_white",
        font=dict(size=18),
        yaxis_title="Density",
        hovermode="x unified",
        legend=dict(font=dict(size=14)),
        height=700 if rows > 1 else 450
    )

    for i in range(n):
        suf = "" if i == 0 else str(i + 1)
        fig.layout[f"xaxis{suf}"].title = "Thermometer Rating (0–100)"

    return fig

import numpy as np
import plotly.graph_objects as go
from functions.dictionaries import lib_con_map_2pt, lib_con_map_7pt, lib_con_2pt, lib_con_7pt, find_weight_col
from functions.weights import SurveyDesign
import streamlit as st

def sankeyGraph(df, question, group, use_weights = True):
    """
    Create a Sankey diagram with optional survey-weighted flows.
    """

    if group == "Liberal/Conservative 2-Point Scale":
        source_col = "lib_con_2pt"
        lib_con_map = lib_con_map_2pt
        ideology_colors = lib_con_2pt
    else:
        source_col = "lib_con_7pt"
        lib_con_map = lib_con_map_7pt
        ideology_colors = lib_con_7pt

    target_col = question

    # Clean data using SurveyDesign if weights are enabled

    weight_col = find_weight_col(question)


    if use_weights:
        design = SurveyDesign(df, weight = "post_full", strata = "full_var_stratum", psu = "full_var_psu")
        df = design.df
    else:
        df = df.copy()
        df[weight_col] = 1  # treat all weights as 1

    # Filter valid values
    df = df[
        (df[source_col].between(1, 7)) &
        (df[target_col].between(0, 7))
    ]

    # Weighted flow counts
    flow_df = (
        df[[source_col, target_col, weight_col]]
        .dropna()
        .groupby([source_col, target_col], as_index = False)
        .agg(count = (weight_col, "sum"))
    )

    # Label mapping
    present_keys = sorted(flow_df[source_col].unique())
    sources = [lib_con_map[int(k)] for k in present_keys]
    targets = flow_df[target_col].astype(str).unique().tolist()
    labels = sources + targets

    x_coords = [0] * len(sources) + [1] * len(targets)
    y_coords = list(np.linspace(0.05, 0.95, len(sources))) + list(np.linspace(0.05, 0.95, len(targets)))

    label_indices = {label: idx for idx, label in enumerate(labels)}
    source_indices = flow_df[source_col].map(lambda x: label_indices[lib_con_map[int(x)]]).tolist()
    target_indices = flow_df[target_col].astype(str).map(lambda t: label_indices[t] + len(sources)).tolist()
    values = flow_df["count"].tolist()

    link_colors = [ideology_colors[int(k)] for k in flow_df[source_col]]

    sankey = go.Sankey(
        node = dict(
            label = labels,
            x = x_coords,
            y = y_coords,
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            color = "white"
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            color = link_colors,
            customdata = flow_df[["count"]],
            hovertemplate = "%{source.label} → %{target.label}<br>Weighted Count: %{customdata[0]:,.0f}<extra></extra>"
        )
    )

    fig = go.Figure(sankey)
    fig.update_layout(
        font = dict(size = 12, family = "Arial"),
        margin = dict(l = 20, r = 20, t = 100, b = 100),
        width = 1000,   # or more
        height = 600,   # increase if nodes/links overlap
    )

    fig.add_annotation(text = "Ideology (Source)", x = 0.01, y = 1.05, showarrow = False, font = dict(size = 12))

    return fig

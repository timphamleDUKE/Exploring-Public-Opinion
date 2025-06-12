import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors
from functions.dictionaries import lib_con_map, description_map

def sankeyGraph(df, question, groups, title=None):
    """
    Create a Sankey diagram with source nodes labeled descriptively per lib_con_map.
    """
    source_col = "lib_con_7pt"
    target_col = question

    # Filter data to valid ranges
    df = df[
        (df[target_col] >= 0) & (df[target_col] <= 7) &
        (df[source_col] >= 1) & (df[source_col] <= 7)
    ]

    # Compute flow counts
    flow_df = (
        df[[source_col, target_col]]
        .dropna()
        .groupby([source_col, target_col])
        .size()
        .reset_index(name='count')
    )

    # Build ordered/descriptive source labels
    present_keys = sorted(flow_df[source_col].unique())
    sources = [lib_con_map[int(k)] for k in present_keys]
    # Build target labels (strings) in first-seen order
    targets = flow_df[target_col].astype(str).unique().tolist()

    # Combine for all node labels
    labels = sources + targets

    # Node positions: sources on left (x=0), targets on right (x=1)
    x_coords = [0] * len(sources) + [1] * len(targets)
    # Evenly space y coordinates
    y_coords = list(__import__('numpy').linspace(0, 1, len(sources))) + \
               list(__import__('numpy').linspace(0, 1, len(targets)))

    # Map labels to numeric indices for the Sankey
    label_indices = {label: idx for idx, label in enumerate(labels)}
    source_indices = (
        flow_df[source_col]
        .map(lambda x: label_indices[lib_con_map[int(x)]])
        .tolist()
    )
    target_indices = (
        flow_df[target_col]
        .astype(str)
        .map(lambda t: label_indices[t] + len(sources))
        .tolist()
    )
    values = flow_df['count'].tolist()

    # Generate gradient link colors (blue→red) with 0.3 opacity
    rgb_grad = n_colors('rgb(0,0,255)', 'rgb(255,0,0)', 7, colortype='rgb')
    gradient = [c.replace('rgb(', 'rgba(').replace(')', ',0.3)') for c in rgb_grad]
    link_colors = [gradient[int(k)-1] for k in flow_df[source_col]]

    # Build sankey with fixed arrangement
    sankey = go.Sankey(
        node=dict(
            label=labels,
            x=x_coords,
            y=y_coords,
            pad=30,
            thickness=30,
            line=dict(color='darkgrey', width=0.5),
            color='lightgrey'
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors
        )
    )

    fig = go.Figure(sankey)
    fig.update_layout(
        # title_text= f"Sankey Diagram of Liberal-Conservative Meter for {target_col}",
        title_text = "There has been some discussion about abortion during recent years.<br>Which one of the opinions on this page best agrees with your view?<br>You can just tell me the number of the opinion you choose.",
        font_size=10
    )
    return fig

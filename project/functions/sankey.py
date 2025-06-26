import holoviews as hv
from holoviews import opts, dim
import pandas as pd
from functions.dictionaries import lib_con_map_3pt, sankey_colors, find_weight_col, find_answer_choices, political_map_3pt
from functions.sidebar_sankey import lib_con_map_7pt_reverse, political_map_reverse
from functions.weights import SurveyDesign
import streamlit as st

# Enable bokeh backend for HoloViews
hv.extension('bokeh')

def sankeyGraph(df, question, list_of_groups, group):

    if group == "Ideological Groups":
        source_col = "lib_con_7pt"
        label_map = lib_con_map_3pt
        ideology_colors = sankey_colors
    else:
        source_col = "poli_party_self_7pt"
        label_map = political_map_3pt
        ideology_colors = sankey_colors

    target_col = question

    # Clean data using SurveyDesign if weights are enabled
    weight_col = find_weight_col(question)

    design = SurveyDesign(df, weight="post_full", strata="full_var_stratum", psu="full_var_psu")
    df = design.df

    # Filter valid values
    valid_values = []
    if group == "Political Groups":
        for group in list_of_groups:
            for value in political_map_reverse[group]:
                valid_values.append(value)
    else:
        for group in list_of_groups:
            for value in lib_con_map_7pt_reverse[group]:
                valid_values.append(value)
    
    df = df[
        df[source_col].isin(valid_values) &
        df[target_col].between(0, 7)
    ]

    df[source_col] = df[source_col].apply(
        lambda x: 1 if 1 <= x <= 3 else x
    )
    df[source_col] = df[source_col].apply(
        lambda x: 2 if 5 <= x <= 7 else x
    )
    df[source_col] = df[source_col].apply(
        lambda x: 3 if x == 4 else x
    )

    # Weighted flow counts
    flow_df = (
        df[[source_col, target_col, weight_col]]
        .dropna()
        .groupby([source_col, target_col], as_index=False)
        .agg(count=(weight_col, "sum"))
    )

    # Label mapping
    answer_choice_map = find_answer_choices(question)
    target_order = [answer_choice_map[i] for i in sorted(answer_choice_map.keys())]

    # Create the data structure for HoloViews Sankey
    # HoloViews expects (source, target, value) tuples
    sankey_data = []
    
    total = flow_df["count"].sum()
    
    for _, row in flow_df.iterrows():
        source_label = label_map[int(row[source_col])]
        target_label = answer_choice_map[int(row[target_col])]
        value = row["count"]
        percent = (value / total) * 100
        
        # Get color for this flow based on source ideology
        color = ideology_colors[int(row[source_col])]
        
        sankey_data.append((source_label, target_label, value, percent, color))

    # Convert to DataFrame for HoloViews
    sankey_df = pd.DataFrame(sankey_data, columns=['Source', 'Target', 'Value', 'Percent', 'Color'])

    # Create HoloViews Sankey diagram
    sankey = hv.Sankey(sankey_df, kdims=['Source', 'Target'], vdims=['Value', 'Percent', 'Color'])
    
    all_nodes = list(sankey_df['Source'].unique()) + list(sankey_df['Target'].unique())
    unique_nodes = list(set(all_nodes))

    # Apply styling options
    sankey = sankey.opts(
        opts.Sankey(
            width=600,
            height=200,
            edge_color='Color',
            edge_alpha=1,
            node_color=dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
            node_fill_color=dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
            node_alpha=1.0,
            node_fill_alpha=1.0,
            node_line_color='black',
            node_line_width=0.25,
            edge_line_width=1,
            label_text_font_size='12pt',
            node_padding=50,
            tools=['hover'],           # Only keep hover tool
            active_tools=[],           # Disable default active tools like box zoom
            bgcolor='white',
            show_values = False,
            node_sort = False
        )
    )

    # Add custom hover tool information
    sankey = sankey.opts(
        opts.Sankey(
            hover_tooltips=[
                ('Flow', '@Source → @Target'),
                ('Weighted Count', '@Value{0,0}'),
                ('Percent', '@Percent{0.00}%')
            ]
        )
    )

    return sankey
import holoviews as hv
from holoviews import opts, dim
import pandas as pd
from functions.dictionaries import *
from functions.weights import SurveyDesign
import streamlit as st

# Enable bokeh backend for HoloViews
hv.extension('bokeh')

def sankeyGraph(df, question, group):
    """
    Create a Sankey diagram with optional survey-weighted flows using HoloViews.
    """

    if group == "Lib/Con 2-Point Scale":
        source_col = "lib_con_2pt"
        lib_con_map = lib_con_map_2pt
        ideology_colors = lib_con_2pt
    elif group == "Lib/Con 7-Point Scale":
        source_col = "lib_con_7pt"
        lib_con_map = lib_con_map_7pt
        ideology_colors = lib_con_7pt
    else:
        source_col = "poli_party_reg"
        lib_con_map = political_map
        ideology_colors = political_colors_numbered

    target_col = question

    # Clean data using SurveyDesign if weights are enabled
    weight_col = find_weight_col(question)

    design = SurveyDesign(df, weight="post_full", strata="full_var_stratum", psu="full_var_psu")
    df = design.df

    # Filter valid values
    if group == "Political Party":
        df = df[
            (df[source_col].between(1, 2)) &
            (df[target_col].between(0, 7))
        ]
    else:
        df = df[
            (df[source_col].between(1, 7)) &
            (df[target_col].between(0, 7))
        ]

    # Weighted flow counts
    flow_df = (
        df[[source_col, target_col, weight_col]]
        .dropna()
        .groupby([source_col, target_col], as_index=False)
        .agg(count=(weight_col, "sum"))
    )

    # Label mapping
    answer_choice_map = find_answer_choices(question)

    # Create the data structure for HoloViews Sankey
    # HoloViews expects (source, target, value) tuples
    sankey_data = []
    
    total = flow_df["count"].sum()
    
    for _, row in flow_df.iterrows():
        source_label = lib_con_map[int(row[source_col])]
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
            show_values=False
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

# Alternative function that returns the plot in a format suitable for Streamlit
def sankeyGraph_streamlit(df, question, group):
    """
    Create a Sankey diagram for Streamlit display.
    Returns the bokeh plot object.
    """
    sankey = sankeyGraph(df, question, group)
    
    # Convert to bokeh plot for Streamlit
    bokeh_plot = hv.render(sankey)
    
    return bokeh_plot

# Function to display using streamlit-bokeh (correct import)
def display_sankey_streamlit_bokeh(df, question, group):
    """
    Create and display a Sankey diagram using streamlit-bokeh.
    """
    try:
        from streamlit_bokeh import streamlit_bokeh
        
        bokeh_plot = sankeyGraph_streamlit(df, question, group)
        streamlit_bokeh(bokeh_plot, use_container_width=True)
        
    except ImportError:
        st.error("streamlit-bokeh not installed. Please run: pip install streamlit-bokeh")
        return None

# Alternative function for HTML export to Streamlit
def sankeyGraph_html(df, question, group):
    """
    Create a Sankey diagram and return as HTML for Streamlit display.
    """
    sankey = sankeyGraph(df, question, group)
    
    # Export as HTML
    from bokeh.embed import file_html
    from bokeh.resources import CDN
    
    bokeh_plot = hv.render(sankey)
    html = file_html(bokeh_plot, CDN, "Sankey Diagram")
    return html

# Function to display using HTML components
def display_sankey_html(df, question, group):
    """
    Create and display a Sankey diagram using HTML components.
    """
    html_plot = sankeyGraph_html(df, question, group)
    st.components.v1.html(html_plot, height=500, scrolling=True)
import streamlit as st
import pandas as pd
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import *
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_custom_css
hv.extension('bokeh')

set_logo()

# Custom CSS
st.markdown("""
<style>
.stCheckbox { margin-bottom: 0.1rem !important; }
.stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { margin-bottom: 0 !important; padding-bottom: 0 !important; }
.stRadio > div { gap: 0.25rem !important; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Issue Position")
st.divider()

# Sidebar UI
col1, col2, col3, col4, col5 = st.columns([3, 0.3, 1, 0.8, 1])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)

with col3:
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)

with col4:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>', unsafe_allow_html=True)
    checks = ideological_check() if group == "Ideological Groups" else political_check()

with col5:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Visualization Type</div>', unsafe_allow_html=True)
    viz_type = st.radio("", ["Traditional Sankey", "Agree/Disagree Flow"], label_visibility="collapsed")

dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)
df_filtered = df[df[issue_question] >= 1].copy()

# --------------------------
# AGREE/DISAGREE SANKEY
# --------------------------
def create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group_type):
    from holoviews import opts

    group_var = 'lib_con_2pt' if group_type == "Ideological Groups" else 'poli_party_self_7pt'
    df_valid = df[(df[issue_question] >= 1) & (df[group_var] >= 1)].copy()
    if df_valid.empty:
        return None

    max_val = int(df_valid[issue_question].max())

    def get_response_labels(max_value):
        if max_value == 7:
            return {
                1: "Favor a great deal", 2: "Favor moderately", 3: "Favor a little",
                4: "Neither favor nor oppose", 5: "Oppose a little",
                6: "Oppose moderately", 7: "Oppose a great deal"
            }
        elif max_value == 5:
            return {
                1: "Strongly agree", 2: "Somewhat agree", 3: "Neither agree nor disagree",
                4: "Somewhat disagree", 5: "Strongly disagree"
            }
        elif max_value == 4:
            return {
                1: "Strongly favor", 2: "Somewhat favor",
                3: "Somewhat oppose", 4: "Strongly oppose"
            }
        else:
            return {i: f"Response {i}" for i in range(1, max_value + 1)}

    def categorize_response(value, max_value):
        if max_value == 7:
            if value <= 3:
                return "Favor"
            elif value == 4:
                return "Neither"
            else:
                return "Oppose"
        elif max_value == 5:
            if value <= 2:
                return "Agree"
            elif value == 3:
                return "Neither"
            else:
                return "Disagree"
        elif max_value == 4:
            if value <= 2:
                return "Favor"
            else:
                return "Oppose"
        else:
            if value <= max_value // 3:
                return "Favor"
            elif value > (max_value * 2) // 3:
                return "Oppose"
            else:
                return "Neither"

    response_labels = get_response_labels(max_val)
    df_valid['general_position'] = df_valid[issue_question].apply(lambda x: categorize_response(x, max_val))
    df_valid['specific_response'] = df_valid[issue_question].map(response_labels)

    if group_type == "Ideological Groups":
        group_labels = {1: 'Liberal', 2: 'Conservative'}
        df_valid['group_label'] = df_valid['lib_con_2pt'].map(group_labels)
    else:
        party_labels = {
            1: 'Strong Democrat', 2: 'Weak Democrat', 3: 'Independent Democrat',
            4: 'Independent', 5: 'Independent Republican', 6: 'Weak Republican',
            7: 'Strong Republican'
        }
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].map(party_labels)

    df_valid = df_valid[df_valid['group_label'].isin(list_of_groups)]
    df_valid = df_valid.dropna(subset=['group_label', 'general_position', 'specific_response'])
    if df_valid.empty:
        return None

    flows = []
    group_to_general = df_valid.groupby(['group_label', 'general_position']).size().reset_index(name='count')
    for _, row in group_to_general.iterrows():
        flows.append((row['group_label'], row['general_position'], row['count']))

    general_to_specific = df_valid.groupby(['general_position', 'specific_response']).size().reset_index(name='count')
    for _, row in general_to_specific.iterrows():
        flows.append((row['general_position'], row['specific_response'], row['count']))

    edge_color_map = {
        'Liberal': '#547DD3',        # Blue
        'Conservative': '#D75D5D'    # Red
    }

    all_nodes = set()
    for src, tgt, _ in flows:
        all_nodes.update([src, tgt])

    node_colors = {label: '#f0f0f0' for label in all_nodes}  # Light grey nodes

    sankey = hv.Sankey(flows).opts(
        opts.Sankey(
            width=900,
            height=600,
            edge_color=hv.dim('source').categorize(edge_color_map, default='lightgray'),
            edge_line_color='black',
            edge_line_alpha=0.4,
            edge_line_width=0.5,
            node_color=hv.dim('label').categorize(node_colors, default='#f0f0f0'),
            node_line_color='white',
            node_line_width=0.5,
            label_text_font_size='11pt',
            show_values=False,
            tools=['hover']
        )
    )

    return sankey

# --------------------------
# RENDER VISUALIZATION
# --------------------------
if viz_type == "Agree/Disagree Flow":
    list_of_groups = list_of_groups_check(group, checks)
    st.markdown(f"### {description_map.get(issue_question)}")

    try:
        sankey_graph = create_agree_disagree_sankey_holoviews(df_filtered, issue_question, list_of_groups, group)
        if sankey_graph:
            bokeh_plot = hv.render(sankey_graph)
            streamlit_bokeh(bokeh_plot, use_container_width=True)
        else:
            st.warning("No data available for this combination.")
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        st.warning("Please try the Traditional Sankey view.")
else:
    list_of_groups = list_of_groups_check(group, checks)
    st.markdown(f"### {description_map.get(issue_question)}")
    sankey_graph = sankeyGraph(df_filtered, issue_question, list_of_groups, group)
    bokeh_plot = hv.render(sankey_graph)
    streamlit_bokeh(bokeh_plot, use_container_width=True)

# --------------------------
# EXPANDER + CAPTION
# --------------------------
expander(df_filtered, issue_question, page="Issue Position")

st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")

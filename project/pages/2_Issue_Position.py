import streamlit as st
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import set_logo, description_map, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df, wrap_title
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_save_list_css
from functions.ad_sankey import create_binary_flow_sankey_holoviews, check_needs_binary_sankey
from functions.saved import star_button, show_saved_button

hv.extension('bokeh')

set_logo()
load_save_list_css()

# Custom CSS
st.markdown("""
    <style>
    .stCheckbox { 
        margin-bottom: 0.1rem !important; 
        line-height: 1.2 !important;
    }
    .stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { 
        margin-bottom: 0 !important; 
        padding-bottom: 0 !important; 
        line-height: 1.2 !important;
    }
    .stRadio > div { 
        gap: 0.25rem !important; 
    }
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
        margin-bottom: 0 !important;
        line-height: 1.2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Issue Position")

topic = st.selectbox("Topic", list_of_issue_topics, index=0)
list_of_issues = topic_to_list_of_issue_map.get(topic)

# Issue question selection
dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)

# Check if this question supports Binary Sankey BEFORE creating the radio button
supports_binary_sankey = check_needs_binary_sankey(issue_question)

# Sidebar for settings
with st.sidebar:
    st.title("Please Select")
    
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)
    
    st.markdown("**Options**")
    checks = ideological_check() if group == "Ideological Groups" else political_check()
    
    st.markdown("**Visualization Type**")
    if supports_binary_sankey:
        viz_type = st.radio("", ["Direct Flow", "Binary Flow"], label_visibility="collapsed")
    else:
        viz_type = st.radio("", ["Direct Flow"], label_visibility="collapsed")

list_of_groups = list_of_groups_check(group, checks)

show_saved = show_saved_button("sankey", issue_question, list_of_groups, viz_type=viz_type)

title = wrap_title(description_map.get(issue_question))

st.divider()
col1, col2 = st.columns(2)
col1.header("Issue Position Questions")

with col2:
    star_button("star-btn-sankey", "sankey", df, issue_question, list_of_groups, group, title=title, viz_type=viz_type)

# Create visualization based on type
if viz_type == "Binary Flow":
    hv_obj = create_binary_flow_sankey_holoviews(df, issue_question, list_of_groups, group, title=title)
else:
    hv_obj = sankeyGraph(df, issue_question, list_of_groups, group, title=title)

# Render the plot
if hv_obj is None:
    st.warning("No data available for this combination.")
else:
    bokeh_plot = hv.render(hv_obj)
    streamlit_bokeh(bokeh_plot, use_container_width=True)

expander(df, issue_question, page="issue")
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
import streamlit as st
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import set_logo, description_map, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df, wrap_title
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_save_list_css
from functions.ad_sankey import create_agree_disagree_sankey_holoviews, check_needs_ad_sankey
from functions.saved import star_button, show_saved_button


hv.extension('bokeh')

set_logo()
load_save_list_css()

# Custom CSS
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 0.1rem !important; }
    .stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { margin-bottom: 0 !important; padding-bottom: 0 !important; }
    .stRadio > div { gap: 0.25rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Issue Position")

col1, col2, col3, col4, col5 = st.columns([3, 0.3, 1, 0.8, 1])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)

# Issue question selection
dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)

# Check if this question supports A/D Sankey BEFORE creating the radio button
supports_ad_sankey = check_needs_ad_sankey(issue_question)

with col3:
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)

with col4:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>', unsafe_allow_html=True)
    checks = ideological_check() if group == "Ideological Groups" else political_check()

with col5:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Visualization Type</div>', unsafe_allow_html=True)
    if supports_ad_sankey:
        viz_type = st.radio("", ["Traditional Sankey", "Agree/Disagree Flow"], label_visibility="collapsed")
    else:
        viz_type = st.radio("", ["Traditional Sankey"], label_visibility="collapsed")

list_of_groups = list_of_groups_check(group, checks)

show_saved = show_saved_button("sankey", issue_question, list_of_groups, viz_type=viz_type)

title = wrap_title(description_map.get(issue_question))

st.divider()
col1, col2 = st.columns(2)
col1.header("Issue Position Questions")

with col2:
    star_button("star-btn-sankey", "sankey", df, issue_question, list_of_groups, group, title=title, viz_type=viz_type)

# Create visualization based on type
if viz_type == "Agree/Disagree Flow":
    hv_obj = create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group, title=title)
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
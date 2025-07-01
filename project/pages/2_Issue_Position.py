import streamlit as st
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import set_logo, description_map, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_custom_css
from functions.ad_sankey import create_agree_disagree_sankey_holoviews

hv.extension('bokeh')

# Custom CSS
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: 0.1rem !important; }
    .stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { margin-bottom: 0 !important; padding-bottom: 0 !important; }
    .stRadio > div { gap: 0.25rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Issue Position")
st.divider()

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

list_of_groups = list_of_groups_check(group, checks)
st.markdown(f"### {description_map.get(issue_question)}")

if viz_type=="Agree/Disagree Flow":
    hv_obj = create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group)
else:
    hv_obj = sankeyGraph(df, issue_question, list_of_groups, group)

if hv_obj is None:
    st.warning("No data available for this combination.")
else:
    bokeh_plot = hv.render(hv_obj)
    streamlit_bokeh(bokeh_plot, use_container_width=True)

expander(df, issue_question, page="issue")
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")

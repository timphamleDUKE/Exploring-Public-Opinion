import streamlit as st
import pandas as pd
import holoviews as hv
from functions.dictionaries import *
from functions.sankey import sankeyGraph, display_sankey_streamlit_bokeh
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.details import expander

set_logo()
st.title("Issue Position")

col1, col2 = st.columns([1, 2])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)

list_of_issues = topic_to_list_of_issue_map.get(topic)

with col2:
    dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)

issue_question = description_to_renamed.get(dropdown_issue_question)
group = st.radio("Groups", ["Ideological Groups", "Political Groups"])

st.markdown(
    '<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>',
    unsafe_allow_html=True
)

if group == "Ideological Groups":
    checks = ideological_check()
else:
    checks = political_check()

list_of_groups = list_of_groups_check(group, checks)

# Filter data to only include valid responses (>= 1)
df_filtered = df[df[issue_question] >= 1].copy()

sankey_graph = (sankeyGraph(df, issue_question, list_of_groups, group))

# Display plots
st.markdown(f"### {description_map.get(issue_question)}")

try:
    st.pyplot(sankey_graph, use_container_width=True)
except:
    try:
        st.plotly_chart(sankey_graph, use_container_width=True)
    except:
        bokeh_plot = hv.render(sankey_graph)
        display_sankey_streamlit_bokeh(df, issue_question, list_of_groups, group)

# Expander

expander(df, issue_question, list_of_groups, group)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
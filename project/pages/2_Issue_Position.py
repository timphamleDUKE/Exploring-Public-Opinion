import streamlit as st
import holoviews as hv
from functions.dictionaries import *
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from streamlit_bokeh import streamlit_bokeh

set_logo()

st.title("Issue Position")

st.divider()

#Columns
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)

with col2:
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)

with col3:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>', unsafe_allow_html=True)
    if group == "Ideological Groups":
        checks = ideological_check()
    else:
        checks = political_check()

dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)

# Filter data to only include valid responses (>= 1)
df_filtered = df[df[issue_question] >= 1].copy()

list_of_groups = list_of_groups_check(group, checks)

# Display plots
st.write("")
st.markdown(f"### {description_map.get(issue_question)}")

sankey_graph = (sankeyGraph(df, issue_question, list_of_groups, group))
bokeh_plot = hv.render(sankey_graph)
streamlit_bokeh(bokeh_plot, use_container_width=True)

# Expander
expander(df, issue_question)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
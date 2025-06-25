import streamlit as st
import pandas as pd
import holoviews as hv
from functions.dictionaries import set_logo, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df, description_map, full_description_map
from functions.sankey import sankeyGraph, display_sankey_streamlit_bokeh
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check


set_logo()

st.title("Issue Position")

with st.sidebar:
    st.title("Customize:")

    topic = st.selectbox("Topic", list_of_issue_topics, index = 0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)
    issue_question = st.selectbox("Issue Question", list_of_issues, index = 0)
    issue_question = description_to_renamed.get(issue_question)

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
expander = st.expander("Details")

full_question = full_description_map.get(issue_question)

if pd.notna(full_question):
    expander.header("Full Question from ANES:")
    expander.write(full_question)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
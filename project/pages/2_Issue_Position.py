import streamlit as st
import pandas as pd
from functions.dictionaries import set_logo, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df, description_map, full_description_map
from functions.sankey import sankeyGraph

set_logo()

st.title("Issue Position")

with st.sidebar:
    st.title("Customize:")

    topic = st.selectbox("Topic", list_of_issue_topics, index = 0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)
    issue_question = st.selectbox("Issue Question", list_of_issues, index = 0)
    issue_question = description_to_renamed.get(issue_question)

    lib_con_pt = st.radio("Groups", ("Liberal/Conservative 2-Point Scale", "Liberal/Conservative 7-Point Scale"))

sankey_graph = (sankeyGraph(df, issue_question, lib_con_pt))

# Display plots

st.markdown(f"### {description_map.get(issue_question)}")
st.plotly_chart(sankey_graph, use_container_width=True)

# Expander
expander = st.expander("See More")

full_question = full_description_map.get(issue_question)

if pd.notna(full_question):
    expander.header("Full Question:")
    expander.write(full_question)

expander.header("Dataframe:")
expander.write(df)

# Caption
st.caption("This Sankey diagram uses survey weights to represent population-level transitions between ideological self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")

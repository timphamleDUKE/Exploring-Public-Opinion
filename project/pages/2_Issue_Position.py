import streamlit as st
import pandas as pd
import holoviews as hv
from functions.dictionaries import *
from functions.sankey import sankeyGraph, display_sankey_streamlit_bokeh

set_logo()
st.title("Issue Position")

col1, col2 = st.columns([1, 2])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)

list_of_issues = topic_to_list_of_issue_map.get(topic)

with col2:
    dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)

issue_question = description_to_renamed.get(dropdown_issue_question)
lib_con_pt = st.radio("Groups", ("Lib/Con 2-Point Scale", "Lib/Con 7-Point Scale", "Political Party"))

#with st.sidebar:
#    st.title("Customize:")
#
#    topic = st.selectbox("Topic", list_of_issue_topics, index = 0)
#    list_of_issues = topic_to_list_of_issue_map.get(topic)
#    issue_question = st.selectbox("Issue Question", list_of_issues, index = 0)
#    issue_question = description_to_renamed.get(issue_question)
#    lib_con_pt = st.radio("Groups", ("Lib/Con 2-Point Scale", "Lib/Con 7-Point Scale", "Political Party"))

sankey_graph = (sankeyGraph(df, issue_question, lib_con_pt))

# Display plots
st.markdown(f"### {description_map.get(issue_question)}")

try:
    st.pyplot(sankey_graph, use_container_width=True)
except:
    try:
        st.plotly_chart(sankey_graph, use_container_width=True)
    except:
        bokeh_plot = hv.render(sankey_graph)
        display_sankey_streamlit_bokeh(df, issue_question, lib_con_pt)


# Expander
expander = st.expander("Details")
full_question = full_description_map.get(issue_question)

if pd.notna(full_question):
    expander.header("Full Question from ANES:")
    expander.write(full_question)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
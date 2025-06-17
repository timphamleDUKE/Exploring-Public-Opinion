import streamlit as st
from functions.dictionaries import set_logo, list_of_issues, df, description_map
from functions.sankey import sankeyGraph

set_logo()

st.title("Issue Position Questions")

with st.sidebar:
    st.title("Customize:")
    issue_question = st.selectbox("Issue Position Question", list_of_issues)
    lib_con_pt = st.radio("Group By", ("Liberal/Conservative 2-Point Scale", "Liberal/Conservative 7-Point Scale"))

sankey_graph = (sankeyGraph(df, issue_question, lib_con_pt))

# Display plots

st.write(df)
st.markdown(f"### {description_map.get(issue_question)}")
st.plotly_chart(sankey_graph, use_container_width=True)

st.caption("This Sankey diagram uses survey weights to represent population-level transitions between ideological self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")

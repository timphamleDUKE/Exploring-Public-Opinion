import streamlit as st
from functions.dictionaries import set_logo

set_logo()

session_state = st.session_state

if "compare_list" in session_state:
    counter = 0;
    for item in session_state["compare_list"]:
        graph_object = item["graph_object"]
        st.plotly_chart(graph_object, use_container_width=True, key = counter)
        counter += 1

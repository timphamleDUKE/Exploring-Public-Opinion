import streamlit as st
import pandas as pd
from functions.dictionaries import set_logo
from functions.css import load_custom_css

set_logo()

st.title("Demographics Test")
st.divider()

density_graph = densityGraph(
    df,
    thermometer_question,
    list_of_groups,
    group,
    title=description_map.get(thermometer_question)
)

st.plotly_chart(density_graph, use_container_width=True)
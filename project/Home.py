import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from functions.dictionaries import *
from functions.density import densityGraph
from functions.sankey import sankeyGraph

set_logo()

with st.sidebar:
    st.title("Select the following:")

    thermometer_question = st.selectbox("Thermometer Question", list_of_thermometer)

    st.text("Group By")
    republican_check = st.checkbox("Republican Party", value = True)
    democratic_check = st.checkbox("Democratic Party", value = True)
    independent_check = st.checkbox("None/Independent Party", value = False)

    lib_con_check = st.checkbox("Liberal/Conservative Meter", value = False)

    issue_question = st.selectbox("Issue Position Question", list_of_issues)

    weighting_method = st.selectbox("Weighting Method", ("simple", "replication", "bootstrap"), placeholder = "bootstrap")


list_of_groups = []
if republican_check:
    list_of_groups.append("Republican Party")

if democratic_check:
    list_of_groups.append("Democratic Party")

if independent_check:
    list_of_groups.append("None/Independent Party")


density_graph = (densityGraph(df, thermometer_question, list_of_groups, weight_method=weighting_method))

sankey_graph = (sankeyGraph(df, issue_question, list_of_groups))

# Display plots

st.write(df)

st.plotly_chart(density_graph, use_container_width=True)

st.plotly_chart(sankey_graph, use_container_width=True)

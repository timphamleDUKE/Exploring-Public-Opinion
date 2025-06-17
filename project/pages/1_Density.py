import streamlit as st
import pandas as pd
from functions.dictionaries import set_logo, list_of_thermometer, df, description_map, full_description_map
from functions.density import densityGraph

set_logo()

st.title("Thermometer Questions")

with st.sidebar:
    st.title("Customize:")

    col1, col2 = st.columns(2)

    with col1:
        topic = st.selectbox("Topic", ("Race", "Candidate"))

    with col2:
        thermometer_question = st.selectbox("Thermometer Question", list_of_thermometer)


    st.text("Group By")
    republican_check = st.checkbox("Republican Party", value = True)
    democratic_check = st.checkbox("Democratic Party", value = True)
    other_check = st.checkbox("Other", value = False)
    na_check = st.checkbox("N/A", value = False)



    st.text("Compare")
    compare_weight = st.toggle("Compare Weighted/Unweighted", value = False)

list_of_groups = []
if republican_check:
    list_of_groups.append("Republican Party")

if democratic_check:
    list_of_groups.append("Democratic Party")

if other_check:
    list_of_groups.append("Other")

if na_check:
    list_of_groups.append("N/A")

density_graph = (densityGraph(df, thermometer_question, list_of_groups))

# Display plots
st.markdown(f"### {description_map.get(thermometer_question)}")
st.plotly_chart(density_graph, use_container_width=True)

# Expander
expander = st.expander("See More")

full_question = full_description_map.get(thermometer_question)

if pd.notna(full_question):
    expander.header("Full Question:")
    expander.write(full_question)

expander.header("Dataframe:")
expander.write(df)

# Caption
st.caption("These plots use an approximate method for density estimation and do not compute standard errors using Taylor series linearization as recommended by ANES for formal inference.")


import streamlit as st
from functions.dictionaries import set_logo, list_of_thermometer, df, description_map
from functions.density import densityGraph

set_logo()

st.title("Thermometer Questions")

with st.sidebar:
    st.title("Customize:")

    thermometer_question = st.selectbox("Thermometer Question", list_of_thermometer)

    st.text("Group By")
    republican_check = st.checkbox("Republican Party", value = True)
    democratic_check = st.checkbox("Democratic Party", value = True)
    independent_check = st.checkbox("None/Independent Party", value = False)

list_of_groups = []
if republican_check:
    list_of_groups.append("Republican Party")

if democratic_check:
    list_of_groups.append("Democratic Party")

if independent_check:
    list_of_groups.append("None/Independent Party")

density_graph = (densityGraph(df, thermometer_question, list_of_groups))

# Display plots
st.write(df)
st.markdown(f"### {description_map.get(thermometer_question)}")
st.plotly_chart(density_graph, use_container_width=True)

st.caption("These plots use an approximate method for density estimation and do not compute standard errors using Taylor series linearization as recommended by ANES for formal inference.")


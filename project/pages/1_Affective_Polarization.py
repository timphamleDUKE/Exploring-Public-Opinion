import streamlit as st
import pandas as pd
from functions.dictionaries import set_logo, list_of_thermometer_topics, topic_to_list_of_thermometer_map, df, description_map, full_description_map, description_to_renamed
from functions.density import densityGraph

set_logo()

st.title("Affective Polarization")

with st.sidebar:
    st.title("Customize:")

    
    topic = st.selectbox("Topic", list_of_thermometer_topics, index = 3)
    list_of_thermometer = topic_to_list_of_thermometer_map.get(topic)
    thermometer_question = st.selectbox("Thermometer Question", list_of_thermometer, index = 0)

    thermometer_question = description_to_renamed.get(thermometer_question)

    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Groups</div>',
        unsafe_allow_html=True
    )
    republican_check = st.checkbox("Republican Party", value = True)
    democratic_check = st.checkbox("Democratic Party", value = True)
    other_check = st.checkbox("Other", value = False)
    na_check = st.checkbox("N/A", value = False)

    # st.text("Compare")
    # compare_weight = st.toggle("Compare Weighted/Unweighted", value = False)

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
expander = st.expander("Details")

full_question = full_description_map.get(thermometer_question)

if pd.notna(full_question):
    expander.header("Full Question from ANES:")
    expander.write(full_question)

expander.header("Dataframe:")
expander.write(df)

# Caption
st.caption("These plots use an approximate method for density estimation and do not compute standard errors using Taylor series linearization as recommended by ANES for formal inference.")


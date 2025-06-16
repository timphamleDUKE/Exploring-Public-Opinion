import streamlit as st
from functions.dictionaries import set_logo, list_of_issues, list_of_thermometer, df
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

    weighting_method = st.selectbox("Weighting Method", ("simple", "replication", "bootstrap"), index = 2)


list_of_groups = []
if republican_check:
    list_of_groups.append("Republican Party")

if democratic_check:
    list_of_groups.append("Democratic Party")

if independent_check:
    list_of_groups.append("None/Independent Party")

sankey_graph = (sankeyGraph(df, issue_question, list_of_groups))

# Display plots

st.write(df)
st.plotly_chart(sankey_graph, use_container_width=True)

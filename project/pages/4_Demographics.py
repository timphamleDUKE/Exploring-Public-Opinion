import streamlit as st
from functions.dictionaries import *
from functions.density import densityGraphFaceted
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check


set_logo()
st.title("Demographics Test")
st.divider()

# Sidebar
with st.sidebar:
    st.title("Please Select:")

    topic = st.selectbox("Topic", list_of_thermometer_topics, index=0)
    list_of_thermometer = topic_to_list_of_thermometer_map.get(topic)

    dropdown_question = st.selectbox("Thermometer Question", list_of_thermometer, index=0)
    thermometer_question = dropdown_to_renamed.get(dropdown_question)

    group = st.radio("Groups", ["Ideological Groups", "Political Groups"])

    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>',
        unsafe_allow_html=True
    )

    if group == "Ideological Groups":
        checks = ideological_check()
    else:
        checks = political_check()
    
    list_of_groups = list_of_groups_check(group, checks)

    facet = st.selectbox("Facet By", list_of_demographics, index=0)


facet_var = "educ"
density_graph = densityGraphFaceted(
    df,
    thermometer_question,
    list_of_groups,
    group,
    title=description_map.get(thermometer_question),
    facet_var=facet_var,
    facet_map=educ_facet_map,
    valid_facet_values=educ_valid_facet_values
)

st.plotly_chart(density_graph, use_container_width=True)

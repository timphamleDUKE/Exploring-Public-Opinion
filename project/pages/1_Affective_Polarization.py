import streamlit as st
import pandas as pd
from functions.sidebar import ideological_check, political_check, list_of_groups_check
from functions.dictionaries import set_logo, list_of_thermometer_topics, topic_to_list_of_thermometer_map, df, description_map, full_description_map, description_to_renamed
from functions.density import densityGraph

set_logo()

st.title("Affective Polarization")

with st.sidebar:
    st.title("Please Select:")

    
    topic = st.selectbox("Topic", list_of_thermometer_topics, index = 2)
    list_of_thermometer = topic_to_list_of_thermometer_map.get(topic)
    thermometer_question = st.selectbox("Thermometer Question", list_of_thermometer, index = 0)

    thermometer_question = description_to_renamed.get(thermometer_question)

    group = st.radio(
        "Groups",
        ["Ideological Groups", "Political Groups"]
    )   

    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>',
        unsafe_allow_html=True
    )

    if group == "Ideological Groups":
        checks = ideological_check()
    else:
        checks = political_check()
    
list_of_groups = list_of_groups_check(group, checks)

density_graph = (densityGraph(df, thermometer_question, list_of_groups, group))

# democratic_graph = (densityGraph(df, "democrat_thermometer_pre", ("Republican Party", "Democratic Party")))
# republican_graph = (densityGraph(df, "republican_thermometer_pre", ("Republican Party", "Democratic Party")))

# col1, col2 = st.columns(2)

# with col1:
#     st.write(democratic_graph)
# with col2:
#     st.write(republican_graph)


# Display plots
st.markdown(f"### {description_map.get(thermometer_question)}")
st.plotly_chart(density_graph, use_container_width=True)

# Expander
expander = st.expander("Details")

full_question = full_description_map.get(thermometer_question)

if pd.notna(full_question):
    expander.header("Full Question from ANES:")
    expander.write(full_question)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
import streamlit as st
import pandas as pd
from functions.sidebar import ideological_check, political_check, list_of_groups_check
from functions.dictionaries import *
from functions.density import densityGraph

set_logo()
st.title("Affective Polarization")

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

density_graph = densityGraph(
    df,
    thermometer_question,
    list_of_groups,
    group,
    title=description_map.get(thermometer_question)
)

democratic_graph = densityGraph(
    df,
    "democrat_thermometer_pre",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("democrat_thermometer_pre")
)

republican_graph = densityGraph(
    df,
    "republican_thermometer_pre",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("republican_thermometer_pre")
)

liberal_graph = densityGraph(
    df,
    "liberals_thermometer",
    ("Liberal", "Conservative"),
    group="Ideological Groups",
    title=description_map.get("liberals_thermometer")
)

conservative_graph = densityGraph(
    df,
    "conservatives_thermometer",
    ("Liberal", "Conservative"),
    group="Ideological Groups",
    title=description_map.get("conservatives_thermometer")
)

harris_graph_pre = densityGraph(
    df,
    "harris_thermometer_pre",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("harris_thermometer_pre")
)

harris_graph_post = densityGraph(
    df,
    "harris_thermometer_post",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("harris_thermometer_post")
)

trump_graph_pre = densityGraph(
    df,
    "trump_thermometer_pre",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("trump_thermometer_pre")
)

trump_graph_post = densityGraph(
    df,
    "trump_thermometer_post",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("trump_thermometer_post")
)

# Tabs
tab1, tab2, tab3 = st.tabs(["Parties", "Ideologies", "Candidates"])

with tab1:
    st.subheader("Thermometer Ratings: Democratic & Republican Parties")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(democratic_graph, use_container_width=True, key="dem_chart")
    with col2:
        st.plotly_chart(republican_graph, use_container_width=True, key="rep_chart")

with tab2:
    st.subheader("Thermometer Ratings: Liberals & Conservatives")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(liberal_graph, use_container_width=True, key="lib_chart")
    with col2:
        st.plotly_chart(conservative_graph, use_container_width=True, key="cons_chart")

with tab3:
    st.subheader("Thermometer Ratings: Presidential Candidates")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(harris_graph_pre, use_container_width=True, key="harris_chart_pre")
        st.plotly_chart(harris_graph_post, use_container_width=True, key="harris_chart_post")
    with col2:
        st.plotly_chart(trump_graph_pre, use_container_width=True, key="trump_chart_pre")
        st.plotly_chart(trump_graph_post, use_container_width=True, key="trump_chart_post")

# Display Plot
st.divider()
st.header("Thermometer Questions")
st.plotly_chart(density_graph, use_container_width=True)

# Expander
full_question = full_description_map.get(thermometer_question)

if pd.notna(full_question):
    with st.expander("Details"):
        st.subheader("Full Question from ANES:")
        st.write(full_question)

# Caption
st.caption(
    "This graph uses survey weights to represent population-level transitions between party self-placement "
    "and responses. However, it does not calculate standard errors using Taylor series linearization as "
    "recommended by ANES for formal inference."
)
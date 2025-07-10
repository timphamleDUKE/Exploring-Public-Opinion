import streamlit as st
from functions.dictionaries import *
from functions.density import densityGraphFaceted
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check
from functions.expander import expander

set_logo()
st.title("Demographics Test")

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

    # Demographics dropdown
    demog_options = sorted(facet_display_map.values())
    facet_display = st.selectbox("Facet By", demog_options, index=0)
    facet_var = {v: k for k, v in facet_display_map.items()}[facet_display]
    

facet_settings = facet_config.get(facet_var)

if facet_settings:
    if "map_func" in facet_settings:
        df["facet_label"] = facet_settings["map_func"](df)
        facet_map = dict(zip(df[facet_var], df["facet_label"]))
        valid_facet_values = facet_settings["valid_values"]
    else:
        facet_map = facet_settings.get("map_plot", facet_settings["map"])
        valid_facet_values = facet_settings.get("valid_values_plot", facet_settings["valid_values"])
        df["facet_label"] = df[facet_var].map(facet_map)


density_graph = densityGraphFaceted(
    df,
    thermometer_question,
    list_of_groups,
    group,
    title=description_map.get(thermometer_question),
    facet_var=facet_var,
    facet_map=facet_map,
    valid_facet_values=valid_facet_values
)

st.plotly_chart(density_graph, use_container_width=True)

# Expander
expander(df, thermometer_question, "affective")

# Caption
st.caption(
    "This graph uses survey weights to represent population-level transitions between party self-placement "
    "and responses. However, it does not calculate standard errors using Taylor series linearization as "
    "recommended by ANES for formal inference."
)
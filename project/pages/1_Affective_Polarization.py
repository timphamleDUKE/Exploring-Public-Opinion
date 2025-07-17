import streamlit as st
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check
from functions.dictionaries import set_logo, list_of_thermometer_topics, topic_to_list_of_thermometer_map, df, description_map, dropdown_to_renamed
from functions.facet import *
from functions.density import densityGraph, densityGraphFaceted
from functions.expander import expander
from functions.saved import star_button, show_saved_button
from functions.css import load_save_list_css
from functions.directionspopup import show_ap_directions_popup

set_logo()
load_save_list_css()

show_ap_directions_popup()

# Tabs
tab1, tab2 = st.tabs(["Featured", "Explore"])

with tab1:
    st.write("Explore key trends in Affective Polarization with density plots showing how Democrats, Republicans, and people across the ideological spectrum rate each other. You’ll also see how each party rated the 2024 presidential candidates, both before and after the election.")     

    st.header("Thermometer Ratings: Democrats & Republicans (2024)")
    col1, col2 = st.columns(2)
    with col1:
        democratic_graph = densityGraph(
            df,
            "democrat_thermometer_pre",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("democrat_thermometer_pre"), 
            yaxis_range=[0, 0.041]
        )

        st.plotly_chart(democratic_graph, use_container_width=True, key="dem_chart")
    with col2:
        republican_graph = densityGraph(
            df,
            "republican_thermometer_pre",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("republican_thermometer_pre"),
            yaxis_range=[0, 0.041]
        )

        st.plotly_chart(republican_graph, use_container_width=True, key="rep_chart")
    
    st.divider()

    st.header("Thermometer Ratings: Liberals & Conservatives (2024)")
    col1, col2 = st.columns(2)
    with col1:
        liberal_graph = densityGraph(
            df,
            "liberals_thermometer",
            ("Liberal", "Conservative"),
            group="Ideological Groups",
            title=description_map.get("liberals_thermometer"),
            yaxis_range=[0, 0.023]
        )

        st.plotly_chart(liberal_graph, use_container_width=True, key="lib_chart")
    with col2:
        conservative_graph = densityGraph(
            df,
            "conservatives_thermometer",
            ("Liberal", "Conservative"),
            group="Ideological Groups",
            title=description_map.get("conservatives_thermometer"),
            yaxis_range=[0, 0.023]
        )

        st.plotly_chart(conservative_graph, use_container_width=True, key="cons_chart")

    st.divider()

    st.header("Thermometer Ratings: Presidential Candidates (2024)")
    col1, col2 = st.columns(2)
    with col1:
        harris_graph_pre = densityGraph(
            df,
            "harris_thermometer_pre",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("harris_thermometer_pre"),
            yaxis_range=[0, 0.072]
        )

        harris_graph_post = densityGraph(
            df,
            "harris_thermometer_post",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("harris_thermometer_post"),
            yaxis_range=[0, 0.072]
        )

        st.plotly_chart(harris_graph_pre, use_container_width=True, key="harris_chart_pre")

        st.plotly_chart(harris_graph_post, use_container_width=True, key="harris_chart_post")

    with col2:
        trump_graph_pre = densityGraph(
            df,
            "trump_thermometer_pre",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("trump_thermometer_pre"),
            yaxis_range=[0, 0.072]
        )

        trump_graph_post = densityGraph(
            df,
            "trump_thermometer_post",
            ("Republicans", "Democrats"),
            group="Political Groups",
            title=description_map.get("trump_thermometer_post"),
            yaxis_range=[0, 0.072]
        )

        st.plotly_chart(trump_graph_pre, use_container_width=True, key="trump_chart_pre")

        st.plotly_chart(trump_graph_post, use_container_width=True, key="trump_chart_post")

# Display Plot
with tab2:
    st.write("Dig deeper into the data using interactive tools. Filter ANES 2024 feeling thermometer responses by party, ideology, and more. Customize the graphs to compare groups of the survey respondents.")
    
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

        demog_options = sorted(facet_display_map.values())
        facet_display = st.selectbox("Compare By", demog_options, index=0)
        facet_var = {v: k for k, v in facet_display_map.items()}[facet_display]

        # Saved List Button
        show_saved = show_saved_button("density", thermometer_question, list_of_groups)

    densityCol1, densityCol2 = st.columns(2)
    densityCol1.header("Thermometer Ratings (2024)")

    with densityCol2:
        star_button("star-btn-density", "density", df, thermometer_question, list_of_groups, group)

    density_graph = densityGraph(
        df,
        thermometer_question,
        list_of_groups,
        group,
        title=description_map.get(thermometer_question)
    )

    st.plotly_chart(density_graph, use_container_width=True)

    st.divider()

    facetCol1, facetCol2 = st.columns(2)
    facetCol1.header("Group Comparisons")

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

    with facetCol2:
        star_button("star-btn-facet","density", df, thermometer_question, list_of_groups, group, facet=facet_display, valid_facet_values=valid_facet_values)

    density_graph = densityGraphFaceted(
        df,
        thermometer_question,
        list_of_groups,
        group,
        title=description_map.get(thermometer_question),
        valid_facet_values=valid_facet_values
    )

    st.plotly_chart(density_graph, use_container_width=True)
    expander(df, thermometer_question, "affective")

# Caption
st.divider()
st.caption(
    "This graph uses survey weights to represent population-level transitions between party self-placement "
    "and responses. However, it does not calculate standard errors using Taylor series linearization as "
    "recommended by ANES for formal inference."
)
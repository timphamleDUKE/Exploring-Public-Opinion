import pandas as pd
import streamlit as st
from functions.dictionaries import *
from functions.density import densityGraphFaceted
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check

set_logo()
st.title("User Input Test")

# Sidebar
with st.sidebar:
    st.title("Please Select:")
    topic = st.selectbox("Topic", list_of_thermometer_topics)
    thermometer_question = dropdown_to_renamed[
        st.selectbox("Thermometer Question", topic_to_list_of_thermometer_map[topic])
    ]
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"])
    checks = ideological_check() if group=="Ideological Groups" else political_check()
    list_of_groups = list_of_groups_check(group, checks)

# User inputs
st.header("Your information")

user_age = st.slider("Age", 18, 100, 18)
user_educ = st.selectbox("Education", facet_config["educ"]["valid_values"])
user_gender = st.selectbox("Gender", facet_config["gender"]["valid_values"])
user_income = st.selectbox("Income", facet_config["income"]["valid_values"])
user_marriage = st.selectbox("Marital Status", facet_config["marriage"]["valid_values"])
user_race_ethnicity = st.selectbox("Race/Ethnicity", facet_config["race_ethnicity"]["valid_values"])
user_religion = st.selectbox("Religion", facet_config["religion"]["valid_values"])
user_rating = st.number_input(
    f"Your rating for “{description_map[thermometer_question]}”",
    min_value=0, max_value=100, value=50, step=1
)

if st.button("Generate Plots"):
    st.divider()
    # Title
    st.header(description_map.get(thermometer_question))

    # Helper
    def build_facet_map_and_labels(var):
        settings = facet_config[var]
        if "map_func" in settings:
            buckets = settings["map_func"](df)
            mapping = dict(zip(df[var], buckets))
            labels = settings["valid_values"]
        else:
            mapping = settings["map"]
            labels = settings["valid_values"]
        return mapping, labels

    # 2 columns per row
    cols_per_row = 2
    items = list(facet_display_map.items())
    for row_start in range(0, len(items), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for idx, (var, pretty) in enumerate(items[row_start:row_start+cols_per_row]):
            with row_cols[idx]:
                st.subheader(f"Faceted by {pretty}")
                facet_map, all_labels = build_facet_map_and_labels(var)

                # pick the single bucket for this var
                if var == "age_election_day":
                    tiny = pd.DataFrame({"age_election_day":[user_age]})
                    user_label = build_age_facet_map(tiny).iat[0]
                    valid_facet_values = [user_label]
                elif var == "educ":
                    valid_facet_values = [user_educ]
                elif var == "gender":
                    valid_facet_values = [user_gender]
                elif var == "income":
                    valid_facet_values = [user_income]
                elif var == "marriage":
                    valid_facet_values = [user_marriage]
                elif var == "race_ethnicity":
                    valid_facet_values = [user_race_ethnicity]
                elif var == "religion":
                    valid_facet_values = [user_religion]
                else:
                    valid_facet_values = all_labels

                fig = densityGraphFaceted(
                    df,
                    thermometer_question,
                    list_of_groups,
                    group,
                    facet_var=var,
                    facet_map=facet_map,
                    valid_facet_values=valid_facet_values,
                    #title=description_map.get(thermometer_question),
                    title=None,
                    user_rating=user_rating
                )

                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

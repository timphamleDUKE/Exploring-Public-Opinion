import pandas as pd
import streamlit as st
from functions.dictionaries import *
from functions.density import densityGraphFaceted
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check

# Setup
set_logo()
st.title("User Input Test")

# Sidebar
with st.sidebar:
    st.title("Please Select:")
    topic = st.selectbox("Topic", list_of_thermometer_topics)
    thermometer_label = st.selectbox("Thermometer Question", topic_to_list_of_thermometer_map[topic])
    thermometer_question = dropdown_to_renamed[thermometer_label]

    group = st.radio("Groups", ["Ideological Groups", "Political Groups"])
    checks = ideological_check() if group == "Ideological Groups" else political_check()
    list_of_groups = list_of_groups_check(group, checks)

# User inputs
st.header("Your information")

user_inputs = {}
for key in ["age_election_day", "educ", "gender", "income", "marriage", "race_ethnicity", "religion"]:
    label = facet_display_map.get(key, key.replace("_", " ").title())
    valid_options = facet_config[key]["valid_values"]
    if key == "age_election_day":
        user_inputs[key] = st.slider(label, 18, 100, 18)
    else:
        user_inputs[key] = st.selectbox(label, valid_options)

user_rating = st.number_input(
    f"Your rating for “{description_map[thermometer_question]}”",
    min_value=0, max_value=100, value=50, step=1
)

# Plots
if st.button("Generate Plots"):
    st.divider()
    st.header(description_map.get(thermometer_question))

    cols_per_row = 2
    facet_items = list(facet_display_map.items())

    for row_start in range(0, len(facet_items), cols_per_row):
        row_cols = st.columns(cols_per_row)

        for idx, (facet_var, pretty_name) in enumerate(facet_items[row_start:row_start + cols_per_row]):
            with row_cols[idx]:
                st.subheader(f"Faceted by {pretty_name}")
                settings = facet_config[facet_var]

                # Build facet label column
                if "map_func" in settings:
                    buckets = settings["map_func"](df)
                    df["facet_label"] = buckets
                    facet_map_dict = dict(zip(df[facet_var], buckets))
                else:
                    facet_map_dict = settings.get("map_plot", settings.get("map"))
                    if facet_map_dict is None:
                        st.error(f"No mapping found for facet '{facet_var}'")
                        st.stop()
                    df["facet_label"] = df[facet_var].map(facet_map_dict)

                # Get user-selected facet label
                user_val = user_inputs[facet_var]
                if facet_var == "age_election_day":
                    user_label = build_age_facet_map(pd.DataFrame({facet_var: [user_val]})).iat[0]
                elif "map_plot" in settings:
                    reverse_map = {v: k for k, v in settings["map"].items()}
                    key = reverse_map.get(user_val)
                    user_label = settings["map_plot"].get(key)
                else:
                    user_label = user_val

                valid_facet_values = [user_label]

                # Generate plot
                fig = densityGraphFaceted(
                    df,
                    thermometer_question,
                    list_of_groups,
                    group,
                    valid_facet_values=valid_facet_values,
                    title=None,
                    user_rating=user_rating
                )

                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

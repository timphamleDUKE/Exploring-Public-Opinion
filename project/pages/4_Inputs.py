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

# Inputs
st.header("Your information")
user_inputs = {
    "age_election_day": st.slider("Age", 18, 100, 18),
    "educ": st.selectbox("Education", facet_config["educ"]["valid_values"]),
    "gender": st.selectbox("Gender", facet_config["gender"]["valid_values"]),
    "income": st.selectbox("Income", facet_config["income"]["valid_values"]),
    "marriage": st.selectbox("Marital Status", facet_config["marriage"]["valid_values"]),
    "race_ethnicity": st.selectbox("Race/Ethnicity", facet_config["race_ethnicity"]["valid_values"]),
    "religion": st.selectbox("Religion", facet_config["religion"]["valid_values"]),
}

user_rating = st.number_input(
    f"Your rating for “{description_map[thermometer_question]}”",
    min_value=0, max_value=100, value=50, step=1
)

# Plots
if st.button("Generate Plots"):
    st.divider()
    st.header(description_map.get(thermometer_question))

    cols_per_row = 2
    items = list(facet_display_map.items())

    for row_start in range(0, len(items), cols_per_row):
        row_cols = st.columns(cols_per_row)

        for idx, (facet_var, pretty_name) in enumerate(items[row_start:row_start + cols_per_row]):
            with row_cols[idx]:
                st.subheader(f"Faceted by {pretty_name}")

                settings = facet_config[facet_var]

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

                valid_facet_values = settings.get("valid_values_plot", settings.get("valid_values", []))

                # Get user's selected value for this facet
                if facet_var == "age_election_day":
                    tiny = pd.DataFrame({facet_var: [user_inputs[facet_var]]})
                    user_label = build_age_facet_map(tiny).iat[0]
                    valid_facet_values = [user_label]
                else:
                    valid_facet_values = [user_inputs[facet_var]]

                fig = densityGraphFaceted(
                    df,
                    thermometer_question,
                    list_of_groups,
                    group,
                    facet_var=facet_var,
                    facet_map=facet_map_dict,
                    valid_facet_values=valid_facet_values,
                    title=None,
                    user_rating=user_rating
                )

                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

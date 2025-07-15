import pandas as pd
import streamlit as st
from functions.dictionaries import *
from functions.density import densityGraphFaceted
from functions.sidebar_density import ideological_check, political_check, list_of_groups_check
from functions.facet import *

# Setup
set_logo()

# Custom CSS for clean styling
st.markdown("""
<style>
    .section-header {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4a90e2;
        margin: 1.5rem 0 1rem 0;
    }
    
    .stButton > button {
        background: #7c3aed;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        font-weight: 500;
        width: 100%;
    }
    
    .user-info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

st.title("User Input Analysis")

# Sidebar for Analysis Settings
with st.sidebar:
    st.title("Please Select")
    
    topic = st.selectbox("Topic", list_of_thermometer_topics)
    thermometer_label = st.selectbox("Question", topic_to_list_of_thermometer_map[topic])
    thermometer_question = dropdown_to_renamed[thermometer_label]
    
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"])
    checks = ideological_check() if group == "Ideological Groups" else political_check()
    list_of_groups = list_of_groups_check(group, checks)

# User Information
user_inputs = {}

# Organize inputs in a clean grid
col1, col2, col3 = st.columns(3)

with col1:
    user_inputs["age_election_day"] = st.slider("Age", 18, 100, 35)
    user_inputs["educ"] = st.selectbox("Education", facet_config["educ"]["valid_values"])

with col2:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)  # Reduced spacing
    user_inputs["gender"] = st.selectbox("Gender", facet_config["gender"]["valid_values"])
    user_inputs["marriage"] = st.selectbox("Marital Status", facet_config["marriage"]["valid_values"])

with col3:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)  # Reduced spacing
    user_inputs["race_ethnicity"] = st.selectbox("Race/Ethnicity", facet_config["race_ethnicity"]["valid_values"])
    user_inputs["income"] = st.selectbox("Income", facet_config["income"]["valid_values"])

user_inputs["religion"] = st.selectbox("Religion", facet_config["religion"]["valid_values"])

# Rating
user_rating = st.slider(
    f'Your rating for "{description_map[thermometer_question]}"',
    min_value=0, max_value=100, value=50
)

# Generate Analysis
if st.button("Generate Analysis"):
    st.divider()
    st.header(f"Analysis: {description_map.get(thermometer_question)}")
    
    # Create plots in a 2-column layout
    facet_items = list(facet_display_map.items())
    
    for i in range(0, len(facet_items), 2):
        col1, col2 = st.columns(2)
        columns = [col1, col2]
        
        for j, (facet_var, pretty_name) in enumerate(facet_items[i:i+2]):
            with columns[j]:
                st.subheader(f"By {pretty_name}")
                
                settings = facet_config[facet_var]
                
                # Build facet mapping
                if "map_func" in settings:
                    buckets = settings["map_func"](df)
                    df["facet_label"] = buckets
                else:
                    facet_map_dict = settings.get("map_plot", settings.get("map"))
                    if facet_map_dict is None:
                        st.error(f"No mapping found for facet '{facet_var}'")
                        continue
                    df["facet_label"] = df[facet_var].map(facet_map_dict)
                
                # Get user's group
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
                    height=350,
                    margin=dict(l=20, r=20, t=30, b=20),
                    font=dict(size=11)
                )
                
                st.plotly_chart(fig, use_container_width=True)
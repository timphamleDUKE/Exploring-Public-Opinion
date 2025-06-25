import streamlit as st
import pandas as pd
import holoviews as hv
from functions.dictionaries import *
from functions.sankey import sankeyGraph, display_sankey_streamlit_bokeh

set_logo()
st.title("Issue Position")

with st.sidebar:
    st.title("Customize:")
    
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)
    issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
    issue_question = description_to_renamed.get(issue_question)
    
    lib_con_pt = st.radio("Groups", ("Lib/Con 2-Point Scale", "Lib/Con 7-Point Scale", "Political Party"))

# Filter data to only include valid responses (>= 1)
df_filtered = df[df[issue_question] >= 1].copy()

sankey_graph = (sankeyGraph(df_filtered, issue_question, lib_con_pt))

# Display plots
st.markdown(f"### {description_map.get(issue_question)}")

try:
    st.pyplot(sankey_graph, use_container_width=True)
except:
    try:
        st.plotly_chart(sankey_graph, use_container_width=True)
    except:
        bokeh_plot = hv.render(sankey_graph)
        display_sankey_streamlit_bokeh(df_filtered, issue_question, lib_con_pt)

# Expander
expander = st.expander("Details")
full_question = full_description_map.get(issue_question)
if pd.notna(full_question):
    expander.subheader("Full Question from ANES:")
    expander.write(full_question)

# Add vote count table
expander.header("Response Counts by Party:")

# Get answer choices for the current question
answer_choices = find_answer_choices(issue_question)

# Create vote count table using filtered data
if lib_con_pt == "Political Party":
    # Filter data for Republicans and Democrats with valid responses
    party_data = df_filtered[df_filtered['party_id'].isin(['Republican', 'Democrat'])].copy()
    
    # Create crosstab of party vs issue response and transpose to swap axes
    vote_counts = pd.crosstab(party_data['party_id'], party_data[issue_question], margins=True).T
    
    # Rename the index (response values) to descriptive labels
    if answer_choices:
        vote_counts.index = vote_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}" if x != 'All' and x in answer_choices else x)
    
    expander.dataframe(vote_counts, use_container_width=True)
else:
    # For Lib/Con scales, show counts by ideology group
    ideology_col = 'lib_con_2pt' if lib_con_pt == "Lib/Con 2-Point Scale" else 'lib_con_7pt'
    
    # Filter out missing values and use already filtered data
    filtered_data = df_filtered.dropna(subset=[ideology_col, issue_question]).copy()
    
    # Create crosstab and transpose to swap axes
    vote_counts = pd.crosstab(filtered_data[ideology_col], filtered_data[issue_question], margins=True).T
    
    # Rename the index (response values) to descriptive labels
    if answer_choices:
        vote_counts.index = vote_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}" if x != 'All' and x in answer_choices else x)
    
    expander.dataframe(vote_counts, use_container_width=True)

# Caption
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
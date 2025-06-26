import streamlit as st
import pandas as pd
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df, issue_question, list_of_groups, group):
    expander = st.expander("Details")

    matched_row = codebook[codebook["Renamed"] == issue_question]

    if not matched_row.empty and matched_row["Original Question"].notna().any():
        expander.subheader("Full Question from ANES:")
        full_question = full_description_map.get(issue_question)
        expander.write(full_question)

    # Add vote count table
    expander.subheader(f"Response Counts by {group}:")

    if group == "Ideological Groups":
        group_col = "lib_con_7pt"
    else:
        group_col = "poli_party_self_7pt"

    # Filters for valid answer choices
    df = df[df[issue_question] >= 1]

    answer_choices = find_answer_choices(issue_question)

    # Create vote count table using filtered data
    if group == "Political Groups":
        # Filter data for Republicans and Democrats with valid responses
        filtered_data = df.dropna(subset=[group_col, issue_question]).copy()

        # Create crosstab - DON'T transpose to keep answer choices as rows
        vote_counts = pd.crosstab(filtered_data[issue_question], filtered_data['poli_party_self_7pt'], margins=True)

        # Rename the index (response values) to descriptive labels
        if answer_choices:
            vote_counts.index = vote_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}" if x != 'All' and x in answer_choices else x)

        # Get column mapping for political party
        party_choices = find_answer_choices('poli_party_self_7pt')
        if party_choices:
            vote_counts.columns = vote_counts.columns.map(lambda x: f"{x}. {party_choices.get(x, x)}" if x != 'All' and x in party_choices else x)

        expander.dataframe(vote_counts, use_container_width=True)
    else:
        # Filter out missing values and use already filtered data
        filtered_data = df.dropna(subset=[group_col, issue_question]).copy()

        # Create crosstab - DON'T transpose to keep answer choices as rows
        vote_counts = pd.crosstab(filtered_data[issue_question], filtered_data[group_col], margins=True)

        # Rename the index (response values) to descriptive labels
        if answer_choices:
            vote_counts.index = vote_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}" if x != 'All' and x in answer_choices else x)

        # Get column mapping for ideological groups
        ideology_choices = find_answer_choices('lib_con_7pt')
        if ideology_choices:
            vote_counts.columns = vote_counts.columns.map(lambda x: f"{x}. {ideology_choices.get(x, x)}" if x != 'All' and x in ideology_choices else x)

        expander.dataframe(vote_counts, use_container_width=True)


import streamlit as st
import pandas as pd
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df, issue_question):
    exp = st.expander("Details")

    # Show full question
    matched_row = codebook[codebook["Renamed"] == issue_question]
    if not matched_row.empty and matched_row["Original Question"].notna().any():
        exp.subheader("Full Question from ANES:")
        full_question = full_description_map.get(issue_question)
        exp.write(full_question)

    # Filter valid responses
    #df = df[df[issue_question] >= 1].copy()
    answer_choices = find_answer_choices(issue_question)

    # Count and percent
    counts = df[issue_question].value_counts().sort_index()
    counts.index.name = None
    total = counts.sum()
    percentages = counts / total * 100

    result_df = pd.DataFrame({
        "Answer Choice": counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}"),
        "Count": counts.values,
        "Percent": percentages.round(1).astype(str) + "%"
    })

    result_df.loc[len(result_df.index)] = ["Total", total, "100%"]
    result_df.set_index("Answer Choice", inplace=True)

    # Display table
    exp.subheader("Raw Response Counts:")
    exp.table(result_df)

    # Bar chart
    exp.subheader("Visual Breakdown:")
    exp.bar_chart(counts)
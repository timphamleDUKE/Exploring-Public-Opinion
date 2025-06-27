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
    missing_df = df[df[issue_question] < 1]
    valid_df = df[df[issue_question] >= 1]

    answer_choices = find_answer_choices(issue_question)

    # Count and percent
    full_counts = df[issue_question].value_counts().sort_index()
    missing_total = full_counts[full_counts.index < 1].sum()
    clean_counts = full_counts[full_counts.index >= 1].copy()
    clean_counts.loc["Missing"] = missing_total

    clean_counts.index.name = None
    total = clean_counts.sum()
    percentages = clean_counts / total * 100

    result_df = pd.DataFrame({
        "Answer Choice": clean_counts.index.map(
            lambda x: "Missing" if x == "Missing" else f"{x}. {answer_choices.get(x, x)}"
        ),
        "Count": clean_counts.values,
        "Percent": percentages.round(1).astype(str) + "%"
    })


    result_df.loc[len(result_df.index) + 1] = ["Total", total, "100%"]
    result_df.set_index("Answer Choice", inplace=True)

    # Display table
    exp.subheader("Raw Response Counts:")
    exp.table(result_df)

    # Bar chart
    exp.subheader("Visual Breakdown:")

    labeled_counts = clean_counts.rename(
        index={k: v for k, v in answer_choices.items() if k in clean_counts.index and k != "Missing"}
    )
    
    exp.bar_chart(labeled_counts, color = "#7c41d2", horizontal = True, height = 500)

    exp.caption("Missing Values include those that answered: Don't Know, Inapplicable, Refused, Insufficient Partials, Sufficient Breakoffs, etc.")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df, issue_question):
    exp = st.expander("Details")

    # Show full question
    matched_row = codebook[codebook["Renamed"] == issue_question]
    if not matched_row.empty and matched_row["Original Question"].notna().any():
        exp.subheader("Full Question from ANES")
        full_question = full_description_map.get(issue_question)
        exp.write(full_question)

    # Get response labels
    answer_choices = find_answer_choices(issue_question) or {}

    # Raw counts
    raw_counts = df[issue_question].value_counts().sort_index()
    total = raw_counts.sum()
    percentages = raw_counts / total * 100

    result_df = pd.DataFrame({
        "Answer Choice": raw_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}"),
        "Count": raw_counts.values,
        "Percent": percentages.round(1).astype(str) + "%"
    })
    result_df.loc[len(result_df)] = ["Total", total, "100%"]
    result_df.set_index("Answer Choice", inplace=True)

    exp.subheader("Raw Response Counts")
    exp.table(result_df)

    # Bar chart
    exp.subheader("Visual Breakdown")
    labeled_counts = raw_counts.rename(index={k: v for k, v in answer_choices.items() if k in raw_counts.index})
    labeled_counts_sorted = labeled_counts.sort_values(ascending=False)

    bar_values = labeled_counts_sorted.values
    bar_labels = labeled_counts_sorted.index.tolist()

    fig = go.Figure(go.Bar(
        x=bar_values,
        y=bar_labels,
        orientation='h',
        marker=dict(color="#7c41d2")
    ))
    fig.update_layout(
        height=500,
        margin=dict(l=100, r=20, t=10, b=40),
        xaxis_title="Number of Responses",
        yaxis_title="Answer Choice",
        yaxis=dict(autorange="reversed"),
        font=dict(size=14, family="Arial")
    )

    exp.plotly_chart(fig, use_container_width=True)
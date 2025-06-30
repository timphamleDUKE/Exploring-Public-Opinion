import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df, issue_question, page):
    exp = st.expander("Details")

    # Show full question
    matched_row = codebook[codebook["Renamed"] ==  issue_question]
    if not matched_row.empty and matched_row["Original Question"].notna().any():
        exp.subheader("Full Question from ANES")
        full_question = full_description_map.get(issue_question)
        exp.write(full_question)

    # Table
    answer_choices = find_answer_choices(issue_question)
    raw_counts = df[issue_question].value_counts().sort_index()
    raw_counts.index.name = None
    total = raw_counts.sum()
    percentages = raw_counts / total * 100

    if page == "issue":
        answer_labels = raw_counts.index.map(lambda x: f"{x}. {answer_choices.get(x, x)}")
    else:
        answer_labels = raw_counts.index

    # Create result table and append Total row
    result_df = pd.concat([
        pd.DataFrame({
            "Answer Choice": answer_labels,
            "Count": raw_counts.values,
            "Percent": percentages.round(1).astype(str) + "%"
        }),
        pd.DataFrame([["Total", total, "100%"]], columns=["Answer Choice", "Count", "Percent"])
    ], ignore_index=True)

    row_height = 35
    header_height = 40
    table_height = header_height + row_height * len(result_df)

    exp.subheader("Raw Response Counts")
    exp.dataframe(result_df, hide_index=True, height=table_height)

    # Bar chart
    exp.subheader("Visual Breakdown")

    labeled_counts = raw_counts.rename(
        index={k: v for k, v in answer_choices.items() if k in raw_counts.index}
    )
    labeled_counts.index = labeled_counts.index.astype(str)
    labeled_counts_sorted = labeled_counts.sort_values(ascending=False)


    fig = go.Figure(go.Bar(
        x=labeled_counts_sorted.values,
        y=labeled_counts_sorted.index.tolist(),
        orientation='h',
        marker=dict(color="#7c41d2"),
        customdata=labeled_counts_sorted.values.reshape(-1, 1),
        hovertemplate="<b>%{y}</b><br>Count: %{customdata[0]}<extra></extra>"
    ))

    fig.update_layout(
        height=500,
        margin=dict(l=100, r=20, t=20, b=40),
        xaxis_title="Number of Responses",
        yaxis_title="Answer Choice",
        yaxis=dict(autorange="reversed"),  # Puts highest count at top
        font=dict(size=14)
    )

    exp.plotly_chart(fig, use_container_width=True)

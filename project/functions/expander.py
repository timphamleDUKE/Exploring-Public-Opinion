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

    # Get response labels
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
    
    # Create plotly bar chart with preserved order
    fig = px.bar(
        x = labeled_counts.values, 
        y = labeled_counts.index,
        orientation = 'h',
        color_discrete_sequence = ["#7c41d2"],
        height = 500,
        labels={
        'x': 'Count',  # Custom x-axis title
        'y': 'Answers'   # Custom y-axis title
        }
    )

    if page == "issue":
        fig.update_traces(
        width=0.5,  # Increase bar width (0.0 to 1.0, where 1.0 is maximum width)
        marker_line_width=0.1  # Remove bar borders for cleaner look (optional)
    ) 
    else:
        fig.update_traces(
        width=3,  # Increase bar width (0.0 to 1.0, where 1.0 is maximum width)
    )

    fig.update_layout(
        font=dict(size=15),  # Increase font size
        margin=dict(l=100, r=50, t=50, b=50)  # Adjust margins if needed
    )

    exp.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.dictionaries import full_description_map, codebook, find_answer_choices
import plotly.express as px

def expander(df, issue_question, page):
    exp = st.expander("Details")

    # Show full question
    matched_row = codebook[codebook["Renamed"] ==  issue_question]
    if not matched_row.empty and matched_row["Original Question"].notna().any():
        exp.subheader("Full Question from ANES")
        full_question = full_description_map.get(issue_question)
        exp.write(full_question)

    # Get response labels
    answer_choices = find_answer_choices(issue_question) or {}

    answer_choices = find_answer_choices(issue_question)

    # Count and percent
    full_counts = df[issue_question].value_counts().sort_index()
    missing_total = full_counts[(full_counts.index) < 1 | (full_counts.index > 100)].sum()
    clean_counts = full_counts[(full_counts.index >=  1) & (full_counts.index <=  100)].copy()
    clean_counts.loc["Missing"] = missing_total

    clean_counts.index.name = None
    total = clean_counts.sum()
    percentages = clean_counts / total * 100

    if page == "issue":
        result_df = pd.DataFrame({
            "Answer Choice": clean_counts.index.map(
                lambda x: "Missing" if x ==  "Missing" else f"{x}. {answer_choices.get(x, x)}"
            ),
            "Count": clean_counts.values,
            "Percent": percentages.round(1).astype(str) + "%"
        })
    else:
        result_df = pd.DataFrame({
            "Answer Choice": clean_counts.index,
            "Count": clean_counts.values,
            "Percent": percentages.round(1).astype(str) + "%"
        })

    result_df.loc[len(result_df.index) + 1] = ["Total", total, "100%"]
    result_df.set_index("Answer Choice", inplace = True)

    exp.subheader("Raw Response Counts")
    exp.table(result_df)

    # Bar chart
    exp.subheader("Visual Breakdown:")

    labeled_counts = clean_counts.rename(
        index = {k: v for k, v in answer_choices.items() if k in clean_counts.index and k !=  "Missing"}
    )
    
    labeled_counts.index = labeled_counts.index.astype(str)

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
        marker_line_width=0.1  # Remove bar borders for cleaner look (optional)
    )

    fig.update_layout(
        bargap=0.999,  # Reduce gap between bars (0.0 to 1.0)
        font=dict(size=12),  # Increase font size
        margin=dict(l=100, r=50, t=50, b=50)  # Adjust margins if needed
    )

    # Preserve the original order by setting category order
    exp.plotly_chart(fig, use_container_width = True)

    exp.caption("Missing Values include those that answered: Don't Know, Inapplicable, Refused, Insufficient Partials, Sufficient Breakoffs, etc.")
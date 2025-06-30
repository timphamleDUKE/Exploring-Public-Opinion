import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df, issue_question, page):
    exp = st.expander("Details")

    # Show full question
    matched_row = codebook[codebook["Renamed"] == issue_question]
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

    # Table label formatting
    def format_table_label(x):
        if page == "issue":
            return f"{x}. {answer_choices.get(x, x)}"
        elif page == "affective":
            if isinstance(x, (int, float)) and (x < 0 or x > 100):
                return f"{x}. {answer_choices.get(x, x)}"
            return str(x)
        else:
            return str(x)

    answer_labels = raw_counts.index.map(format_table_label)

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

    chart_df = pd.DataFrame({
        "value": raw_counts.index.astype(str),
        "count": raw_counts.values
    })

    def format_chart_label(x):
        try:
            num_x = int(x)
        except:
            return str(x)
        if page == "issue":
            return answer_choices.get(num_x, str(num_x))
        elif page == "affective":
            if num_x < 0 or num_x > 100:
                return answer_choices.get(num_x, str(num_x))
            return str(num_x)
        else:
            return str(num_x)

    chart_df["label"] = chart_df["value"].map(format_chart_label)
    chart_df_sorted = chart_df.sort_values(by="count", ascending=False)

    fig = go.Figure(go.Bar(
        x=chart_df_sorted["count"],
        y=chart_df_sorted["label"],
        orientation='h',
        marker=dict(color="#7c41d2"),
        customdata=chart_df_sorted["count"].values.reshape(-1, 1),
        hovertemplate="<b>%{y}</b><br>Count: %{customdata[0]}<extra></extra>"
    ))

    fig.update_layout(
        height=500,
        margin=dict(l=100, r=20, t=20, b=40),
        xaxis_title="Number of Responses",
        yaxis_title="Answer Choice",
        yaxis=dict(autorange="reversed"),
        font=dict(size=14)
    )

    exp.plotly_chart(fig, use_container_width=True)

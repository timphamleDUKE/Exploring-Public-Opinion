import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.dictionaries import full_description_map, codebook, find_answer_choices

def expander(df: pd.DataFrame, issue_question: str, page: str) -> None:
    """
    Show detailed counts table and bar chart for a given question.
    page must be either 'issue' or 'affective'.
    """

    exp = st.expander("Details")

    # Show full question
    matched = codebook[codebook["Renamed"] == issue_question]
    if not matched.empty and matched["Original Question"].notna().any():
        exp.subheader("Full Question from ANES")
        exp.write(full_description_map.get(issue_question, "—"))

    exp.subheader("Raw Response Counts")

    series = pd.to_numeric(df[issue_question], errors="coerce")
    answer_choices = find_answer_choices(issue_question) or {}

    if page == "issue":
        # 1) Metrics
        valid   = series.between(1, 100).sum()
        missing = (~series.between(1, 100)).sum()
        col1, col2 = exp.columns(2)
        col1.metric("Valid responses", valid)
        col2.metric("Missing responses", missing)

        # 2) Pull raw values as ints
        raw_int = series.dropna().astype(int)

        # 3) Count and sort by numeric code
        raw_counts = raw_int.value_counts().sort_index()
        codes = raw_counts.index  # ints
        labels = [f"{code}. {answer_choices.get(code, code)}" for code in codes]

        # 4) Build table with % sign
        total       = raw_counts.sum()
        percentages = (raw_counts / total * 100).round(2)
        percent_strs = [f"{p:.2f}%" for p in percentages.tolist()]

        df_table = pd.DataFrame({
            "Answer Choice": labels + ["Total"],
            "Count":         raw_counts.tolist() + [total],
            "Percent":       percent_strs + ["100%"]
        })
        height = 40 + 35 * len(df_table)
        exp.dataframe(df_table, hide_index=True, height=height)

        # 5) Bar chart (labels only, descending order)
        exp.subheader("Visual Breakdown")
        # map codes → descriptive text
        text_labels = [answer_choices.get(code, code) for code in codes]
        # apply those labels to counts
        counts = raw_counts.copy()
        counts.index = text_labels
        # sort descending by count
        counts_desc = counts.sort_values(ascending=False)
        # reverse so largest is on top
        bar_labels = counts_desc.index[::-1]
        bar_values = counts_desc.values[::-1]

        fig = go.Figure(go.Bar(
            x=bar_values,
            y=bar_labels,
            orientation='h',
            marker=dict(color="#7c41d2"),
            customdata=bar_values.reshape(-1, 1),
            hovertemplate="<b>%{y}</b><br>Count: %{customdata[0]}<extra></extra>"
        ))
        fig.update_layout(
            height=500,
            margin=dict(l=100, r=50, t=40, b=50),
            xaxis_title="Number of Responses",
            yaxis_title="Answer Choice",
            font=dict(size=14)
        )
        exp.plotly_chart(fig, use_container_width=True)

    elif page == "affective":
        # 1) Metrics
        valid   = series.between(0, 100).sum()
        missing = (~series.between(0, 100)).sum()
        col1, col2 = exp.columns(2)
        col1.metric("Valid responses", valid)
        col2.metric("Missing responses", missing)

        # 2) Counts & percentages
        raw_counts = series.value_counts().sort_index()
        total      = raw_counts.sum()
        percentages = (raw_counts / total * 100).round(2)

        # 3) Label missing codes only
        def affective_label(x: int) -> str:
            if x < 0 or x > 100:
                return f"{x}. {answer_choices.get(x, x)}"
            return str(x)

        labels = [affective_label(x) for x in raw_counts.index]

        # 4) Build table
        df_table = pd.concat([
            pd.DataFrame({
                "Answer Choice": labels,
                "Count":         raw_counts.values,
                "Percent":       [f"{p:.2f}%" for p in percentages.tolist()]
            }),
            pd.DataFrame([["Total", total, "100%"]], columns=["Answer Choice", "Count", "Percent"])
        ], ignore_index=True)
        row_h, hdr_h = 35, 40
        table_h = hdr_h + row_h * len(df_table)
        exp.dataframe(df_table, hide_index=True, height=table_h)

        # 5) Bar chart
        exp.subheader("Visual Breakdown")
        chart_counts = raw_counts.copy()
        chart_counts.index = labels
        chart_counts = chart_counts.sort_values(ascending=False)

        fig = go.Figure(go.Bar(
            x=chart_counts.values,
            y=chart_counts.index.tolist(),
            orientation='h',
            marker=dict(color="#7c41d2"),
            customdata=chart_counts.values.reshape(-1, 1),
            hovertemplate="<b>%{y}</b><br>Count: %{customdata[0]}<extra></extra>"
        ))
        fig.update_layout(
            height=500,
            margin=dict(l=100, r=50, t=40, b=50),
            xaxis_title="Number of Responses",
            yaxis_title="Answer Choice",
            yaxis=dict(autorange="reversed"),
            font=dict(size=14)
        )
        exp.plotly_chart(fig, use_container_width=True)

    else:
        exp.warning("Unsupported page type. Must be 'issue' or 'affective'.")

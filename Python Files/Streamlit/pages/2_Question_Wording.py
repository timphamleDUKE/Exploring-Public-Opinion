import streamlit as st
import textstat
import pandas as pd
from transformers import pipeline
from Home import *

set_logo()

# ---- Load Transformer Model (cached for performance) ---- #
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

sentiment_pipeline = load_sentiment_model()

# ---- Helper Functions ---- #
def analyze_question(text):
    sentiment_result = sentiment_pipeline(text)[0]

    # Properly map label codes to human-readable names
    label_map = {
        "LABEL_0": "🔴 Negative",
        "LABEL_1": "🟡 Neutral",
        "LABEL_2": "🟢 Positive"
    }
    raw_label = sentiment_result["label"]
    sentiment_label = label_map.get(raw_label, raw_label)
    sentiment_score = round(sentiment_result["score"], 2)

    return {
        "Flesch Reading Ease": round(textstat.flesch_reading_ease(text), 2),
        "Flesch-Kincaid Grade": round(textstat.flesch_kincaid_grade(text), 2),
        "Transformer Sentiment": f"{sentiment_label} ({sentiment_score})",
        "Word Count": int(len(text.split()))
    }

def interpret_metric(metric, value):
    if metric == "Flesch Reading Ease":
        if value >= 80: return "🟢 Very easy to read"
        elif value >= 60: return "🟡 Standard readability"
        else: return "🔴 Difficult to read"
    elif metric == "Flesch-Kincaid Grade":
        if value <= 6: return "🟢 Elementary level"
        elif value <= 10: return "🟡 Middle/High School"
        else: return "🔴 College level or above"
    elif metric == "Word Count":
        if value <= 10: return "🟢 Concise"
        elif value <= 20: return "🟡 Moderate"
        else: return "🔴 Long/Complex"
    return ""

# ---- Metric Descriptions ---- #
metric_descriptions = {
    "Flesch Reading Ease": "Higher = easier to read. 60–70 is average.",
    "Flesch-Kincaid Grade": "U.S. grade level needed to understand.",
    "Transformer Sentiment": "Context-aware classification: Positive, Neutral, or Negative.",
    "Word Count": "More words = potentially complex framing."
}

# ---- Streamlit UI ---- #
st.title("Survey Question Wording Comparison")

st.write("Select two survey questions below to compare their tone and complexity using sentiment analysis and readability scores.")

q1 = st.text_area("Question 1", value="Do you think the federal government should make it more difficult for people to buy a gun than it is now, make it easier for people to buy a gun, or keep the same as they are now?", height=100)
q2 = st.text_area("Question 2", value="Do you favor, oppose, or neither favor nor oppose requiring background checks for gun purchases at gun shows or other private sales?", height=100)

# ---- Analysis & Table Rendering ---- #
if q1.strip() and q2.strip():
    result1 = analyze_question(q1)
    result2 = analyze_question(q2)

    rows = []
    for metric in result1.keys():
        val1 = result1[metric]
        val2 = result2[metric]

        interp1 = interpret_metric(metric, val1) if isinstance(val1, (int, float)) else ""
        interp2 = interpret_metric(metric, val2) if isinstance(val2, (int, float)) else ""
        description = metric_descriptions.get(metric, "")

        rows.append({
            "Metric": f"**{metric}**",
            "What it means": description,
            "Question 1": f"{val1} {interp1}",
            "Question 2": f"{val2} {interp2}"
        })

    comparison_df = pd.DataFrame(rows)

    st.subheader("Tone & Complexity Comparison")
    st.table(comparison_df)

    # ---- Optional Insights ---- #
    st.subheader("Insight")
    insights = []

    if result1["Flesch-Kincaid Grade"] > result2["Flesch-Kincaid Grade"]:
        insights.append("Question 1 is harder to understand than Question 2.")
    elif result2["Flesch-Kincaid Grade"] > result1["Flesch-Kincaid Grade"]:
        insights.append("Question 2 is harder to understand than Question 1.")

    # Extract sentiment labels only
    s1_label = result1["Transformer Sentiment"].split()[0]
    s2_label = result2["Transformer Sentiment"].split()[0]

    if s1_label != s2_label:
        insights.append(f"Question 1 has a **{s1_label.lower()}** tone, while Question 2 is **{s2_label.lower()}** — indicating a difference in emotional framing.")

    if not insights:
        st.write("No major differences detected.")
    else:
        for i in insights:
            st.write(f"• {i}")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -- Set Page Configuration --
st.set_page_config(
    page_title="Survey Navigator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- Load and Prepare Data --
data = pd.read_csv("anes_2024.csv")
party = data["V241019"]
support = data["V241583"]
support = support.replace([-9, -8, -7, -1], np.nan)
party = party.replace([-9, -8, -7, -1], np.nan)
data = data.dropna(subset=["V241019", "V241583"]).copy()
data["Party"] = data["V241019"].map({1: "Democrat", 2: "Republican", 3: "Independent"})

mean_support_dem = support[party == 1].mean()
mean_support_rep = support[party == 2].mean()
polarization_score = abs(mean_support_dem - mean_support_rep)
total_variance = support.var()
normalized_polarization = polarization_score / np.sqrt(total_variance)

# -- Custom CSS Styling --
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #e1e8ed;
            font-family: 'Segoe UI', sans-serif;
            font-size: 18px;
        }
        .reportview-container .main .block-container {
            padding: 2rem 3rem;
        }
        .main-title {
            font-size: 3.5rem;
            color: #ffffff;
            padding-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.7rem;
            color: #8899a6;
            margin-bottom: 1.5rem;
        }
        .section-title {
            font-size: 2.3rem;
            color: #ffffff;
            margin-top: 2rem;
        }
        .stMarkdown p {
            font-size: 1.3rem;
        }
        .stButton button {
            font-size: 1.1rem;
        }
        .stSelectbox div, .stSlider div {
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<h1 id="home" class="main-title">Survey Navigator</h1>""", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explore survey data, question phrasing, and polarization metrics in one intuitive dashboard.</p>", unsafe_allow_html=True)

# -- Topic Selection Dropdown --
topics = ["Gun Control", "Immigration", "Healthcare", "Economy", "Climate Change"]
selected_topic = st.selectbox("Choose a Topic to Explore:", topics, index=0)

# -- Opinion Section --
st.markdown(f"""<h2 id="opinion" class="section-title">Polarization</h2>""", unsafe_allow_html=True)
col_gap, col_var, col_norm = st.columns(3)
col_gap.metric("Partisan Gap", f"{polarization_score:.2f}", "Gap in average support between parties")
col_var.metric("Variance", f"{total_variance:.2f}", "Dispersion of all responses")
col_norm.metric("Normalized Score", f"{normalized_polarization:.2f}", "Gap adjusted for variance")

st.markdown("""
<div style='margin-top: 1rem;'>
    <p><b>Partisan Gap:</b> Difference in average support between Democrats and Republicans.</p>
    <p><b>Variance:</b> Overall dispersion in opinion on the topic.</p>
    <p><b>Normalized Score:</b> Partisan gap adjusted relative to variance to show polarization strength.</p>
</div>
""", unsafe_allow_html=True)

polarization_df = pd.DataFrame({
    "Metric": ["Partisan Gap", "Variance", "Normalized Score"],
    "Value": [polarization_score, total_variance, normalized_polarization]
})
fig = px.bar(polarization_df, x="Metric", y="Value", text_auto='.2f',
             color="Metric", color_discrete_sequence=["#42a5f5", "#66bb6a", "#ffa726"],
             title="Polarization Metrics")
fig.update_layout(template="plotly_dark", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# -- Political Predictor --
st.markdown("""<h2 id="predictor" class="section-title">Political Predictor</h2>""", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 90, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    race = st.selectbox("Race", ["White", "Black", "Hispanic", "Asian", "Other"])
    region = st.selectbox("Region", ["East Coast", "Southeast", "Northeast", "Midwest", "West Coast"])
    income = st.selectbox("Income", ["<25k", "25–50k", "50–100k", "100k+"])
    education = st.selectbox("Education", ["High School", "Some College", "Bachelor's", "Graduate"])

    if st.button("Generate Prediction"):
        st.session_state.predicted_party = "Democrat" if region in ["Northeast", "West Coast"] else "Republican"
        st.session_state.views = {
            "Gun Control": "Strong Support" if education in ["Bachelor's", "Graduate"] else "Moderate",
            "Immigration": "Leaning Restrictive" if income == "<25k" else "Balanced"
        }

with col2:
    st.markdown("### Prediction")
    if "predicted_party" in st.session_state:
        st.success(f"Predicted Party: {st.session_state.predicted_party}")
        for issue, stance in st.session_state.views.items():
            st.markdown(f"- **{issue}**: {stance}")
    else:
        st.info("Enter demographic info and click Predict.")

# -- Optional: Graph comparing user prediction to overall support distribution --
if "views" in st.session_state:
    st.markdown("#### Your Support Compared to Overall Distribution")
    user_gc_support = 85 if st.session_state.views.get("Gun Control") == "Strong Support" else 60
    fig2 = px.histogram(data, x="V241583", nbins=30, title="Distribution of Gun Control Support",
                        labels={"V241583": "Gun Control Support Level"}, opacity=0.75)
    fig2.add_vline(x=user_gc_support, line_dash="dash", line_color="red", annotation_text="Your Position",
                  annotation_position="top right")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# -- Wording Section --
st.markdown("""<h2 id="comparison" class="section-title">Question Wording Comparison</h2>""", unsafe_allow_html=True)

ces_questions = {
    "Q1": "Do you support stricter gun control laws?",
    "Q2": "Should background checks be required?",
    "Q3": "Do you support mandatory permits?"
}
anes_questions = {
    "Q1": "Should it be more difficult to buy a gun?",
    "Q2": "How many guns are in your household?",
    "Q3": "Should handguns be banned for non-authorized users?"
}

ces_meta = {
    "Q1": {"reading": 8, "tone": "Neutral", "length": 10},
    "Q2": {"reading": 7, "tone": "Neutral", "length": 12},
    "Q3": {"reading": 9, "tone": "Slightly Negative", "length": 14}
}
anes_meta = {
    "Q1": {"reading": 9, "tone": "Negative", "length": 13},
    "Q2": {"reading": 8, "tone": "Neutral", "length": 9},
    "Q3": {"reading": 10, "tone": "Assertive", "length": 11}
}

col_ces, col_anes = st.columns(2)

with col_ces:
    st.markdown("### Cooperative Election Study Question")
    ces_sel = st.selectbox("Select CES Question", list(ces_questions.keys()), format_func=lambda x: ces_questions[x], key="ces_dropdown")
    meta = ces_meta.get(ces_sel, {})
    st.markdown(f"- Reading Level: {meta.get('reading', 'N/A')}")
    st.markdown(f"- Tone: {meta.get('tone', 'N/A')}")
    st.markdown(f"- Length: {meta.get('length', 'N/A')} words")

with col_anes:
    st.markdown("### American National Election Survey Question")
    anes_sel = st.selectbox("Select ANES Question", list(anes_questions.keys()), format_func=lambda x: anes_questions[x], key="anes_dropdown")
    meta = anes_meta.get(anes_sel, {})
    st.markdown(f"- Reading Level: {meta.get('reading', 'N/A')}")
    st.markdown(f"- Tone: {meta.get('tone', 'N/A')}")
    st.markdown(f"- Length: {meta.get('length', 'N/A')} words")

# -- Wording Comparison Graphs --
if ces_sel and anes_sel:
    wording_df = pd.DataFrame({
        "Survey": ["CES", "ANES"],
        "Reading Level": [ces_meta[ces_sel]["reading"], anes_meta[anes_sel]["reading"]],
        "Length": [ces_meta[ces_sel]["length"], anes_meta[anes_sel]["length"]]
    })
    st.markdown("#### Wording Feature Comparison")
    fig_read = px.bar(wording_df, x="Survey", y="Reading Level", title="Reading Level Comparison", color="Survey", template="plotly_dark")
    fig_len = px.bar(wording_df, x="Survey", y="Length", title="Length Comparison", color="Survey", template="plotly_dark")
    st.plotly_chart(fig_read, use_container_width=True)
    st.plotly_chart(fig_len, use_container_width=True)

# -- About Section --
st.markdown("""<h2 id="about" class="section-title">About the Survey Navigator</h2>""", unsafe_allow_html=True)
st.markdown("""
This app uses U.S. survey data from:
- [ANES](https://electionstudies.org/)
- [CES](https://cces.gov.harvard.edu/)
- [PEW](https://www.pewresearch.org/)
- [GSS](https://gss.norc.org/)

Made by students at the Duke Polarization Lab.
""")


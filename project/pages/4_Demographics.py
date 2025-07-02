import streamlit as st
from functions.dictionaries import set_logo, df, description_map, ideological_colors, ideological_fill_colors, political_colors, political_fill_colors
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functions.weights import get_anes_weighted_density_data

set_logo()
st.title("Demographics Test")
st.divider()

def densityGraphFaceted(df, question, groups, group, title=None, yaxis_range=None):
    # 1. Map gender codes to labels
    gender_map = {
        -9: None,
        -1: None,
        1: "Man",
        2: "Woman",
        3: "Other",
        4: "Other"
    }
    df["gender_label"] = df["gender"].map(gender_map)
    df = df[df["gender_label"].notna()]

    # 2. Filter valid gender values
    valid_genders = ["Man", "Woman", "Other"]
    df = df[df["gender_label"].isin(valid_genders)]

    # 3. Map group (party or ideology) values
    if group == "Ideological Groups":
        df["party"] = df["lib_con_7pt"].map({
            1: "Liberal", 2: "Liberal", 3: "Liberal",
            4: "Moderate",
            5: "Conservative", 6: "Conservative", 7: "Conservative",
            99: "Other", -4: "Other", -9: "Other"
        }).fillna("N/A")
        colors = ideological_colors
        fill_colors = ideological_fill_colors

    elif group == "Political Groups":
        df["party"] = df["poli_party_reg"].map({
            1: "Democratic Party", 2: "Republican Party",
            4: "Other", 5: "Other", -8: "Other", -9: "N/A"
        }).fillna("N/A")
        colors = political_colors
        fill_colors = political_fill_colors

    # 4. Filter main dataframe
    df = df[
        (df["party"].isin(groups)) &
        (df[question].between(0, 100)) &
        (df["gender_label"].notna())
    ]

    genders = sorted(df["gender_label"].unique())

    # 5. Create subplots by gender
    fig = make_subplots(
        rows=1, cols=len(genders),
        subplot_titles=genders,
        shared_yaxes=True
    )

    try:
        for i, gender in enumerate(genders):
            df_gender = df[df["gender_label"] == gender]
            for party in groups:
                subset = df_gender[df_gender["party"] == party][question].dropna()

                # Skip if not enough data to compute KDE
                if subset.nunique() < 2:
                    st.warning(f"Not enough variation for '{party}' in gender group '{gender}' — skipping.")
                    continue

                plotting_data = get_anes_weighted_density_data(
                    df_gender[df_gender["party"] == party],
                    question,
                    [party],
                    group_var="party",
                    seed=12345
                )

                if party not in plotting_data:
                    st.warning(f"No KDE data for '{party}' in gender '{gender}'")
                    continue

                x_range = plotting_data[party]["x_range"]
                y_values = plotting_data[party]["y_values"]

                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=y_values,
                    mode="lines",
                    name=party,
                    legendgroup=party,
                    showlegend=(i == 0),  # Only show legend once
                    line=dict(color=colors.get(party, "gray"), width=2),
                    fill="tozeroy",
                    fillcolor=fill_colors.get(party, "rgba(128,128,128,0.3)")
                ), row=1, col=i+1)

    except Exception as e:
        st.error(f"Error generating weighted density plot: {e}")
        return go.Figure()

    # 6. Layout
    fig.update_layout(
        title=dict(
            text=title if title else "",
            font=dict(size=24)
        ),
        xaxis_title="Thermometer Rating (0–100)",
        yaxis_title="Density",
        template="simple_white",
        font=dict(size=18),
        hovermode="x unified",
        legend=dict(font=dict(size=14))
    )

    if yaxis_range:
        for axis in fig.layout:
            if axis.startswith("yaxis"):
                fig.layout[axis].update(range=yaxis_range)

    return fig



density_graph = densityGraphFaceted(
    df,
    "feminists_thermometer",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("feminists_thermometer")
)

st.plotly_chart(density_graph, use_container_width=True)

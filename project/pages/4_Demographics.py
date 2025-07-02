import streamlit as st
import pandas as pd
import plotly.express as px
from functions.dictionaries import set_logo, list_of_thermometer_topics, topic_to_list_of_thermometer_map, df, description_map, dropdown_to_renamed
from functions.density import densityGraph

set_logo()
st.title("Demographics Test")
st.divider()

def densityGraphFaceted(df, question, groups, group, title=None, yaxis_range=None):
    # Map group values and define colors
    if group == "Ideological Groups":
        df["party"] = df["lib_con_7pt"].map({
            1: "Liberal", 2: "Liberal", 3: "Liberal",
            4: "Moderate",
            5: "Conservative", 6: "Conservative", 7: "Conservative",
            99: "Other", -4: "Other", -9: "Other"
        }).fillna("N/A")

    elif group == "Political Groups":
        df["party"] = df["poli_party_reg"].map({
            1: "Democratic Party", 2: "Republican Party",
            4: "Other", 5: "Other", -8: "Other", -9: "N/A"
        }).fillna("N/A")

    # Filter data
    df_filtered = df[
        (df["party"].isin(groups)) &
        (df[question].between(0, 100)) &
        (df["gender"].notna())
    ]

    # Plot using plotly express
    fig = px.histogram(
        df_filtered,
        x=question,
        color="party",
        facet_col="gender",  # Facet by gender
        histnorm="density",
        nbins=40,
        opacity=0.6,
        barmode="overlay",
        title=title,
        category_orders={"gender": ["Male", "Female"]}  # Optional: control order
    )

    fig.update_layout(
        xaxis_title="Thermometer Rating (0–100)",
        yaxis_title="Density",
        template="simple_white",
        font=dict(size=16)
    )

    if yaxis_range:
        for axis in fig.layout:
            if axis.startswith("yaxis"):
                fig.layout[axis].update(range=yaxis_range)

    return fig


#def densityGraph(df, question, groups, group, title=None, yaxis_range=None)
density_graph = densityGraphFaceted(
    df,
    "feminists_thermometer",
    ("Republican Party", "Democratic Party"),
    group="Political Groups",
    title=description_map.get("feminists_thermometer")
)

st.plotly_chart(density_graph, use_container_width=True)
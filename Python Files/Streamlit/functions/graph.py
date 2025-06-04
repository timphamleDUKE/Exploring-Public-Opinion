import streamlit as st
import plotly.express as px
from functions.dictionaries import group_by_dic, group_by_dic_reverse
from functions.weights import ces_calc_weights, anes_calc_weights
from plotly import graph_objects as go

# filtered dataframe, question variable, list of group bys

def display_chart(df, question, groups, study):
    for group in groups:
        st.plotly_chart(bar_graph(df, question, group, study), use_container_width=True)

def bar_graph(df, question, group, study):

    if study == "CES":
        grouped = ces_calc_weights(df, question, group)
    elif study == "ANES":
        # Use simplified calculation for consistent visualization
        grouped = anes_calc_weights(df, question, group)
        # If you need complex survey weights, uncomment the line below:
        # grouped = anes_calc_weights_complex(df, question, group)

    # Create horizontal stacked bar chart
    fig = px.bar(
        grouped,
        y="group",
        x="proportion",
        color="response",
        orientation='h',
        labels={
            "group": group_by_dic_reverse[group],
            "proportion": "Proportion",
            "response": "Response"
        },
        title=f"Proportional Distribution of {question} by {group_by_dic_reverse[group]}"
    )

    # Configure the layout for stacked bars
    fig.update_layout(
        barmode="stack", 
        xaxis_tickformat=".0%",
        # Ensure consistent styling
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=16, color='white'),
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)'
        )
    )
    
    # Reverse the order of y-axis to match your CES chart
    fig.update_yaxes(autorange="reversed")

    return fig
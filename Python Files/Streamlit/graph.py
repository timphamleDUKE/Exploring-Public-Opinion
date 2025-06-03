# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 15:09:11 2025

@author: heyti
"""

import streamlit as st
import plotly.express as px
from dictionaries import *
from plotly import graph_objects as go

# filtered dataframe, question variable, list of group bys

def display_chart(df, question, groups):
    for group in groups:
            st.plotly_chart(bar_graph(df, question, group), use_container_width=True)

def bar_graph(df, question, group):
    # Calculate count per (group, question)
    grouped = (
        df.groupby([group, question])
        .size()
        .reset_index(name='count')
    )

    # Calculate total per group (for normalization)
    totals = grouped.groupby(group)['count'].transform('sum')
    grouped['proportion'] = grouped['count'] / totals

    # Create horizontal stacked bar chart
    fig = px.bar(
        grouped,
        y=group,
        x='proportion',
        color=question,
        orientation='h',
        labels={
            f"{group}": group_by_dic_reverse[group],
            "proportion": "Proportion",
            question: "Response"
        },
        title=f"Proportional Distribution of {question} by {group_by_dic_reverse[group]}"
    )

    fig.update_layout(barmode="stack", xaxis_tickformat=".0%")

    return fig
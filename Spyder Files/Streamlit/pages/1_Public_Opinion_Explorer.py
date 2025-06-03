# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:23:25 2025

@author: heyti
"""

import streamlit as st
import pandas as pd
import numpy as np
from dictionaries import *
from graph import *

def public_opinion_explorer ():
    st.write("### Public Opinion Explorer")
    
    st.markdown("--description of page--")

    # inputs
    col1, col2, col3 = st.columns(3)

    study = col1.selectbox(
        "Study",
        ("Cooperative Election Study", "American National Election Studies"),
    )
    study = study_dic[study]

    topic = col2.selectbox(
        "Topic", 
        list_of_topics,
    )
    
    group_by = col3.multiselect(
        "Group By:",
        list_of_group_bys,
        default=["Political Party"],
    )

    year_range = st.slider(
        "Year",
        min_value = 2000,
        max_value = 2024,
        value = [2024,2024]
        )
    
    year = year_range[0] # hard coded

    select_study(study, year, topic, group_by)

    list_of_questions = codebook[
    (codebook["year"] == year) &
    (codebook["study"] == study) &
    (codebook["topic"] == topic)
    ]["question"].dropna().tolist()
    
    question = st.selectbox("Question", list_of_questions)

    graph(filtered_study_df, question, group_by)

def select_study(study, selected_year, selected_topic, selected_group_by):
    global filtered_study_df
    
    study_file_path = f"data/{study}_{selected_year}_clean.csv"
    study_df = pd.read_csv(study_file_path)

    select_columns = []

    for group_by in selected_group_by:
        if group_by in group_by_dic:
            select_columns.append(group_by_dic[group_by])

    matching_rows = codebook[(codebook["study"] == study) & (codebook["year"] == selected_year) & (codebook["topic"] == selected_topic)]
    select_columns.extend(matching_rows["variable"].dropna().tolist())

    filtered_study_df = study_df[select_columns]

def graph(df, question, group_by):
    question_var = codebook.loc[codebook["question"] == question, "variable"].iloc[0]
    st.write(question_var) # delete later

    group_by_vars = [group_by_dic[group] for group in group_by]

    st.write(group_by_vars) # delete later

    valid_rows = df[question_var] > 0
    for var in group_by_vars:
        valid_rows &= df[var] > 0

    filtered_df = df.loc[valid_rows, group_by_vars + [question_var]]

    st.dataframe(filtered_df) # delete later

    display_chart(filtered_df, question_var, group_by_vars)
    

public_opinion_explorer()
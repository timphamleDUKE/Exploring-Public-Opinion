# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:23:25 2025

@author: heyti
"""

import streamlit as st
import pandas as pd

def public_opinion_explorer ():
    st.write("### Public Opinion Explorer")
    
    st.markdown("--description of page--")
    
    
    # inputs
    
    col1, col2, col3 = st.columns(3)

    global study
    study = col1.selectbox(
        "Study",
        ("Cooperative Election Study", "American National Election Studies"),
    )
    
    list_of_topics = [
        "Abortion",
        "Gun Control"
    ]

    global topic
    topic = col2.selectbox(
        "Topic", 
        list_of_topics,
    )
    
    list_of_group_bys = [
        "Political Party", 
        "Education", 
        "Employment Status", 
        "Marriage", 
        "Income", 
        "Religion", 
        "Gender",
        "Race",
        "State",
        "Urban/Rural Status"
        ]
    
    global group_by
    group_by = col3.multiselect(
        "Group By:",
        list_of_group_bys,
        default=["Political Party"],
    )

    global year_range
    year_range = st.slider(
        "Year",
        min_value = 2000,
        max_value = 2024,
        value = [2024,2024]
        )
    
    year = year_range[0] # hard coded

    select_study_csv(study, year, topic, group_by)

    # list_of_questions = select_questions()
    list_of_questions = []
    
    question = st.multiselect("Question", list_of_questions)

def select_study_csv(study, year, topic, group_by):
    if study == "Cooperative Election Study":
        study = "CES"
    if study == "American National Election Studies":
        study = "ANES"
    
    study_file_path = f"../Data/{study}_{year}.csv"
    study_df = pd.read_csv(study_file_path)

    

    select_columns = []

    filtered_study_df = study_df[select_columns]

# def select_questions():
    
    
public_opinion_explorer()
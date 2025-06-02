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
        "Gun Rights"
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

    list_of_questions = filtered_study_df[topic].dropna().unique().tolist()
    
    question = st.multiselect("Question", list_of_questions)

def select_study_csv(selected_study, selected_year, selected_topic, selected_group_by):
    global topic
    global filtered_study_df

    if selected_study == "Cooperative Election Study":
        study = "CES"
    if selected_study == "American National Election Studies":
        study = "ANES"
    
    study_file_path = f"data/{study}_{selected_year}_clean.csv"
    study_df = pd.read_csv(study_file_path)

    select_columns = []

    group_by_dic = {
        "Political Party": "poli_party_reg", 
        "Education": "educ", 
        "Employment Status": "employ", 
        "Marriage": "marstat", 
        "Income": "faminc_new", 
        "Religion": "religion", 
        "Gender": "gender",
        "Race": "race",
        "State": "input_state",
        "Urban/Rural Status": "urban_rural"
    }

    for group_by in selected_group_by:
        if group_by in group_by_dic:
            select_columns.append(group_by_dic[group_by])

    topic_dic = {
        "Abortion": "q_abortion",
        "Gun Rights": "q_gun_rights",
        }
    
    if selected_topic in topic_dic:
        topic = topic_dic[selected_topic]

    select_columns.append(topic)

    global filtered_study_df
    filtered_study_df = study_df[select_columns]

public_opinion_explorer()
import streamlit as st

# Sidebar Components
def ideological_check():
    liberal_check = st.checkbox("Liberal", value = True)
    conservative_check = st.checkbox("Conservative", value = True)
    moderate_check = st.checkbox("Moderate", value = False)
    return liberal_check, conservative_check, moderate_check

def political_check():
    democratic_check = st.checkbox("Democratic Party", value = True)
    republican_check = st.checkbox("Republican Party", value = True)
    independent_check = st.checkbox("Independent", value = False)
    return democratic_check, republican_check, independent_check

def list_of_groups_check(group, checks):
    list_of_groups = []

    if group == "Ideological Groups":
        liberal, conservative, moderate = checks
        if liberal:
            list_of_groups.append("Liberal")
        if conservative:
            list_of_groups.append("Conservative")
        if moderate:
            list_of_groups.append("Moderate")

    elif group == "Political Groups":
        democratic, republican, independent= checks
        if democratic:
            list_of_groups.append("Democratic Party")
        if republican:
            list_of_groups.append("Republican Party")
        if independent:
            list_of_groups.append("Independent")

    return list_of_groups

lib_con_map_7pt_reverse = {
    "Liberal": [1, 2, 3],
    "Moderate": [4],
    "Conservative": [5, 6, 7]
}

political_map_reverse = {
    "Democratic Party": [1, 2, 3],
    "Independent": [4],
    "Republican Party": [5, 6, 7]
}
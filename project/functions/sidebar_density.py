import streamlit as st

# Sidebar Components
def ideological_check():
    liberal_check = st.checkbox("Liberal", value = True)
    conservative_check = st.checkbox("Conservative", value = True)
    moderate_check = st.checkbox("Moderate", value = False)
    other_check = st.checkbox("Other", value = False)
    return liberal_check, conservative_check, moderate_check, other_check

def political_check():
    democratic_check = st.checkbox("Democrats", value = True)
    republican_check = st.checkbox("Republicans", value = True)
    other_check = st.checkbox("Independents", value = False)
    na_check = st.checkbox("N/A", value = False)
    return democratic_check, republican_check, other_check, na_check

def list_of_groups_check(group, checks):
    list_of_groups = []

    if group == "Ideological Groups":
        liberal, conservative, moderate, other = checks
        if liberal:
            list_of_groups.append("Liberal")
        if conservative:
            list_of_groups.append("Conservative")
        if moderate:
            list_of_groups.append("Moderate")
        if other:
            list_of_groups.append("Other")

    elif group == "Political Groups":
        democratic, republican, other, na = checks
        if democratic:
            list_of_groups.append("Democrats")
        if republican:
            list_of_groups.append("Republicans")
        if other:
            list_of_groups.append("Independents")
        if na:
            list_of_groups.append("N/A")

    return list_of_groups

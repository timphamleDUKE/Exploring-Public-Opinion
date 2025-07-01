import streamlit as st
from functions.density import densityGraph
from functions.dictionaries import description_map
import base64

session_state = st.session_state


def star_toggle(page, df, thermometer_question, list_of_groups, group):

    if "compare_list" not in session_state:
        session_state["compare_list"] = []

    st.write(session_state)

    on_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M12 2l3.09 6.26L22 9.27l-5.18 5.05L18.18 22 12 18.27 5.82 22l1.36-7.68L2 9.27l6.91-1.01L12 2Z" fill="#7c41d2" stroke="#7c41d2" stroke-width="2"/>
    </svg>
    """

    off_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M12 2l3.09 6.26L22 9.27l-5.18 5.05L18.18 22 12 18.27 5.82 22l1.36-7.68L2 9.27l6.91-1.01L12 2Z" fill="none" stroke="#7c41d2" stroke-width="2"/>
    </svg>
    """

    on_base64 = base64.b64encode(on_svg.encode("utf-8")).decode("utf-8")
    off_base64 = base64.b64encode(off_svg.encode("utf-8")).decode("utf-8")

    # If compare_list contains the object change session_state accordingly
    if check_compare_list(thermometer_question, list_of_groups) == True:
        session_state["star_state"] = "on"
    else:
        session_state["star_state"] = "off"
    
    # If session_state off vs on
    if session_state["star_state"] == "off":
        load_star_css(off_base64)
    else:
        load_star_css(on_base64)
    
    if st.button("", key="star_toggle_btn"):
        # Toggle state only when button is clicked
        if session_state["star_state"] == "off":
            session_state["star_state"] = "on"
            # Add object to compare_list
            if check_compare_list(thermometer_question, list_of_groups) == False:
                add_compare_list(page, df, thermometer_question, list_of_groups, group)
        else:
            session_state["star_state"] = "off"
            if check_compare_list(thermometer_question, list_of_groups) == True:
                remove_compare_list(thermometer_question, list_of_groups)
        # Rerun to update the display
        st.rerun()

def check_compare_list(thermometer_question, list_of_groups):
    for item in session_state["compare_list"]:
        if item["id"] == get_compare_list_object(thermometer_question, list_of_groups):
            return True
    return False

def add_compare_list(page, df, thermometer_question, list_of_groups, group):
    if page == "density":
        graph_object = densityGraph(
            df, thermometer_question, list_of_groups, group, title=description_map.get(thermometer_question)
        )

    session_state["compare_list"].append({
        "id": get_compare_list_object(thermometer_question, list_of_groups),
        "graph_object": graph_object
    })

def remove_compare_list(thermometer_question, list_of_groups):
    for item in session_state["compare_list"]:
        if item["id"] == get_compare_list_object(thermometer_question, list_of_groups):
            session_state["compare_list"].remove(item)

def get_compare_list_object(thermometer_question, list_of_groups):
    return f"{thermometer_question}, {list_of_groups}"
    
def load_star_css(b64):
    hover_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M12 2l3.09 6.26L22 9.27l-5.18 5.05L18.18 22 12 18.27 5.82 22l1.36-7.68L2 9.27l6.91-1.01L12 2Z" fill="#4e2291" stroke="#4e2291" stroke-width="2"/>
    </svg>
    """
    hover_base64 = base64.b64encode(hover_svg.encode("utf-8")).decode("utf-8")


    st.markdown(f"""
        <style>
        .stButton {{
            display: flex;
            justify-content: flex-end !important;
            align-items: center !important;
            padding-top: 1rem;
        }}
                
        .stButton > button:hover {{
            background-image: url("data:image/svg+xml;base64,{hover_base64}");
            border: 1px solid #31333F;
        }}

        .stButton > button:active {{
            background-image: url("data:image/svg+xml;base64,{b64}");
            border: 1px solid #31333F;
        }}

        .stButton > button {{
            background-image: url("data:image/svg+xml;base64,{b64}");
            background-position: center;
            background-repeat: no-repeat;
            background-size: 70% 70%;  /* Adjust this to control size */
            border: 1px solid #31333F;
            padding: 0;
            width: 3.3rem;
            height: 2rem;
            margin: 0;
        }}

        </style>
    """, unsafe_allow_html=True)

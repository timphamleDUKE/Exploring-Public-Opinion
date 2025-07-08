import streamlit as st
from functions.density import densityGraph
from functions.dictionaries import description_map
from functions.ad_sankey import create_agree_disagree_sankey_holoviews, check_needs_ad_sankey
from functions.sankey import sankeyGraph
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh

import base64

session_state = st.session_state

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


def star_button(page, df, question, list_of_groups, group, title="", viz_type=""):

    if "saved_list" not in session_state:
        session_state["saved_list"] = []
    
    if "graph_ids" not in session_state:
        session_state["graph_ids"] = []

    # If saved_list contains the object change session_state accordingly
    if check_saved_list(question, list_of_groups, viz_type=viz_type) == True:
        session_state["star_state"] = "on"
    else:
        session_state["star_state"] = "off"
    
    # If session_state off vs on
    if session_state["star_state"] == "off":
        load_star_css(off_base64)
    else:
        load_star_css(on_base64)
    
    if st.button("", type="primary", key="star-btn", help="Save visualization"):
        # Toggle state only when button is clicked
        if session_state["star_state"] == "off":
            session_state["star_state"] = "on"
            # Add object to saved_list
            if check_saved_list(question, list_of_groups, viz_type=viz_type) == False:
                add_saved_list(page, df, question, list_of_groups, group, title, viz_type)
        else:
            session_state["star_state"] = "off"
            if check_saved_list(question, list_of_groups, viz_type=viz_type) == True:
                remove_saved_list(question, list_of_groups, viz_type, main = True)
        # Rerun to update the display
        st.rerun()
    
def check_saved_list(question, list_of_groups, viz_type):
    for item in session_state["saved_list"]:
        if item["id"] == get_saved_list_object(question, list_of_groups, viz_type):
            return True
    return False

def add_saved_list(page, df, question, list_of_groups, group, title, viz_type):
    if page == "density":
        graph_object = densityGraph(
            df, question, list_of_groups, group, title=description_map.get(question)
        )

    if page == "sankey":
        if viz_type == "Agree/Disagree Flow":
            graph_object = create_agree_disagree_sankey_holoviews(df, question, list_of_groups, group, title=title)
            bokeh_plot = hv.render(graph_object)
            graph_object = bokeh_plot
        else:
            graph_object = sankeyGraph(df, question, list_of_groups, group, title=title)
            bokeh_plot = hv.render(graph_object)
            graph_object = bokeh_plot

    session_state["saved_list"].append({
        "id": get_saved_list_object(question, list_of_groups, viz_type),
        "page": page,
        "graph_object": graph_object
    })
    session_state["graph_ids"].append(get_saved_list_object(question, list_of_groups, viz_type))


    st.toast("Saved Visualization!")


def remove_saved_list(question, list_of_groups, viz_type, main = False, id = None):
    if main:
        for item in session_state["saved_list"]:
            if item["id"] == get_saved_list_object(question, list_of_groups, viz_type):
                session_state["graph_ids"].remove(item["id"])
                session_state["saved_list"].remove(item)
        st.toast("Removed Visualization!")
    else:
        for item in session_state["saved_list"]:
            if item["id"] == id:
                session_state["graph_ids"].remove(item["id"])
                session_state["saved_list"].remove(item)
        st.toast("Removed Visualization!")


def get_saved_list_object(question, list_of_groups, viz_type=""):
    return f"{question}, {list_of_groups}, {viz_type}"
    
def load_star_css(b64):
    hover_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M12 2l3.09 6.26L22 9.27l-5.18 5.05L18.18 22 12 18.27 5.82 22l1.36-7.68L2 9.27l6.91-1.01L12 2Z" fill="#4e2291" stroke="#4e2291" stroke-width="2"/>
    </svg>
    """
    hover_base64 = base64.b64encode(hover_svg.encode("utf-8")).decode("utf-8")

    st.markdown(f"""
        <style>
        .stButton:has(button[kind="primary"]) {{
            display: flex;
            justify-content: flex-end !important;
            align-items: center !important;
            padding-top: 1rem;
        }}
        
        /* Target button regardless of wrapper structure */
        .stButton button[kind="primary"],
        .stButton > div button[kind="primary"],
        .stButton > div > div button[kind="primary"] {{
            background-image: url("data:image/svg+xml;base64,{b64}") !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-size: 70% 70% !important;
            border: 1px solid #31333F !important;
            padding: 0 !important;
            width: 3.3rem !important;
            height: 2rem !important;
            margin: 0 !important;
            background-color: transparent !important;
        }}

        /* Hover state */
        .stButton button[kind="primary"]:hover,
        .stButton > div button[kind="primary"]:hover,
        .stButton > div > div button[kind="primary"]:hover {{
            background-image: url("data:image/svg+xml;base64,{hover_base64}") !important;
            border: 1px solid #31333F !important;
        }}

        /* Active state */
        .stButton button[kind="primary"]:active,
        .stButton > div button[kind="primary"]:active,
        .stButton > div > div button[kind="primary"]:active {{
            background-image: url("data:image/svg+xml;base64,{b64}") !important;
            border: 1px solid #31333F !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def show_saved_button(page, question, list_of_groups, viz_type=""):
    @st.dialog("Saved List")
    def show_saved_list(page, question, list_of_groups):
        key = 0
        if "saved_list" not in session_state or len(session_state["saved_list"]) == 0:
            st.write("Save a visualization to display")
        else:
            for item in session_state["saved_list"]:
                if page == "density":
                    graph_object = item["graph_object"]
                    st.plotly_chart(graph_object, use_container_width=True, key = f"chart-{key}")
                    if st.button("Remove", key=f"remove-btn-{key}"):
                        remove_saved_list(question, list_of_groups, viz_type, main = False, id = item["id"])
                        st.rerun()
                    key += 1
                if page == "sankey":
                    graph_object = item["graph_object"]
                    # st.plotly_chart(graph_object, use_container_width=True, key = f"chart-{key}")
                    streamlit_bokeh(graph_object, use_container_width=True)

                    if st.button("Remove", key=f"remove-btn-{key}"):
                        remove_saved_list(question, list_of_groups, viz_type, main = False, id = item["id"])
                        st.rerun()
                    key += 1
    
    if st.button("Saved List"):
        show_saved_list(page, question, list_of_groups)
    
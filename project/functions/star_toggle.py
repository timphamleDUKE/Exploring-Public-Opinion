import streamlit as st
from functions.css import load_custom_css

def star_toggle(df, thermometer_question, list_of_groups, group):        

    load_custom_css()

    star_off = f"""
        <div class="star">
            <button class="star-button">
                <svg class="star-empty" width="24" height="24" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" 
                        fill="none" stroke="#7c41d2" stroke-width="2"/>
                </svg>
            </button>
        </div>
    """

    star_on = f"""
        <div class ="star">
            <button class="star-button">
                <svg class="star-filled" width="24" height="24" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" 
                        fill="#7c41d2" stroke="#7c41d2" stroke-width="2"/>
                </svg>
            </button>
        </div>
    """

    session_state = st.session_state

    if "star_state" not in st.session_state or "star_state" == "off":
        star = star_off
        session_state["star_state"] = "off"

    return star_off
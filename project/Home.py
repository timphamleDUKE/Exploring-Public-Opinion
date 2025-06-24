import streamlit as st
from functions.dictionaries import set_logo

set_logo()
st.title("Home")
st.divider()

st.markdown("""
**This project explores how American voters are often more aligned in their views than they might believe.**  
We show that despite emotional divides, their underlying opinions are surprisingly similar.
""")

def explore_card(title, image_path, description_text, button_key, page_path):
    with st.container(border=True):
        if st.button(title, key=button_key, use_container_width=True):
            st.switch_page(page_path)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image_path, use_container_width=True)
        with col2:
            st.markdown(description_text)

col1, col2 = st.columns(2)

with col1:
    explore_card(
        title="Affective Polarization",
        image_path="images/AP logo.png",
        description_text="""
Explore emotional and affective dimensions of political polarization.

• Sentiment patterns  
• Emotional responses  
• Affective divides  
• Partisan feelings
""",
        button_key="ap_button",
        page_path="pages/1_Affective_Polarization.py"
    )

with col2:
    explore_card(
        title="Issue Position",
        image_path="images/IP logo.png",
        description_text="""
Analyze political positions on key issues.

• Policy preferences  
• Issue stances  
• Position clustering  
• Ideological mapping
""",
        button_key="ip_button",
        page_path="pages/2_Issue_Position.py"
    )
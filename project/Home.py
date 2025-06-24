import streamlit as st
from functions.dictionaries import set_logo

set_logo()
st.title("Home")
st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)

# Text section at the top
st.markdown("""
**This project explores how American voters are often more aligned in their views than they might believe.** 
We show that despite emotional divides, their underlying opinions are surprisingly similar.
""")

# Create two columns for the boxes
col1, col2 = st.columns(2)

# AP Box
with col1:
    # Use st.container with border and styling
    with st.container(border=True):
        st.markdown("""
        <div style="
            background-color: #f8f9fa;
            border-radius: 5px;
        ">
        """, unsafe_allow_html=True)
        
        # Add centered clickable title with custom styling
        if st.button("AFFECTIVE POLARIZATION", 
                    key="ap_button", 
                    use_container_width=True,
                     type="primary"):
            st.switch_page("pages/1_Affective_Polarization.py")
        
        # Create columns inside the container
        ap_col1, ap_col2 = st.columns([1, 2])
        
        with ap_col1:
            st.image("images/AP logo.png", use_container_width=True)
        
        with ap_col2:
            st.markdown("""
            **How warmly or coldly do Americans feel about people on the other side?
          Track emotional responses by political identity over time.**

            """)
        
        st.markdown("</div>", unsafe_allow_html=True)

# IP Box
with col2:
    # Use st.container with border and styling
    with st.container(border=True):
        st.markdown("""
        <div style="
            background-color: #f8f9fa;
            border-radius: 5px;
        ">
        """, unsafe_allow_html=True)
        

        
        # Add centered clickable title with custom styling
        if st.button("ISSUE POSITION", 
                    key="ip_button", 
                    use_container_width=True,
                     type="primary"):
            st.switch_page("pages/2_Issue_Position.py")
        
        # Create columns inside the container
        ip_col1, ip_col2 = st.columns([1, 2])
        
        with ip_col1:
            st.image("images/IP logo.png", use_container_width=True)
        
        with ip_col2:
            st.markdown("""
            **Where do people stand on topics like immigration, healthcare, and the economy?**
            
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Add spacing before the ABOUT section
st.markdown("<br><br>", unsafe_allow_html=True)
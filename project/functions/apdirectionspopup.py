import streamlit as st

@st.dialog("Affective Polarization Information")
def show_directions_dialog():
    """Display directions in a proper dialog"""
    st.markdown("**What is Affective Polarization?**")
    st.write("Affective polarization refers to the emotional gap between how warmly people feel about their own political party compared to the opposing one. It's often measured using feeling thermometer ratings, where respondents rate a target on a 0–100 scale.")
    st.write("Explore key trends in affective polarization with density plots showing how Democrats, Republicans, and people across the ideological spectrum rate each other. You'll also see how each party rated the 2024 presidential candidates, both before and after the election.")

    st.markdown("**Feeling Thermometer Scale (0-100)**")
    st.write("0 = Very Cold/Negative | 50 = Neutral | 100 = Very Warm/Positive")

def show_directions_popup():
    """Display the directions popup to the right of the title"""
    # Create columns with specific width ratios - first column much wider
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([6, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown("# Affective Polarization")
    
    with col2:
        # Add custom CSS to align the button with the title
        st.markdown("""
        <style>
        .title-help-button {
            margin-top: 15px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="title-help-button">', unsafe_allow_html=True)
        if st.button("?", key="directions_button", help="View directions"):
            show_directions_dialog()
        st.markdown('</div>', unsafe_allow_html=True)
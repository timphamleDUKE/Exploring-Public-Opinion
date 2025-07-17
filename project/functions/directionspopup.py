import streamlit as st

# Affective Polarization popup
@st.dialog("Affective Polarization Dashboard")
def show_ap_directions_dialog():
    """Display affective polarization directions in a proper dialog"""
    st.markdown("**What is Affective Polarization?**")
    st.write("Affective polarization refers to the emotional gap between how warmly people feel about their own political party compared to the opposing one. It's often measured using feeling thermometer ratings, where respondents rate a target on a 0–100 scale.")
        
    st.markdown("**Feeling Thermometer Scale (0-100)**")
    st.write("0 = Very Cold/Negative | 50 = Neutral | 100 = Very Warm/Positive")

def show_ap_directions_popup():
    """Display the affective polarization directions popup to the right of the title"""
    # Create columns with specific width ratios - first column much wider
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([6.3, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Affective Polarization</h1>", unsafe_allow_html=True)
        
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
        if st.button("?", key="ap_directions_button", help="View directions"):
            show_ap_directions_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

# Issue Position popup
@st.dialog("Issue Position Dashboard")
def show_ip_directions_dialog():
    """Display issue position directions in a proper dialog"""
    st.markdown("**What is Issue Position Analysis?**")
    st.write("Issue position polarization is the widening gap in policy opinions between ideological groups, with people taking increasingly opposing stances on key political issues. This tool explores how different groups respond to policy questions using data from the 2024 ANES survey.")
        
    st.markdown("**How to Use This Tool:**")
    st.write("**Step 1:** Choose a Topic and specific Issue Question to analyze")
    st.write("**Step 2:** Select Groups (Ideological or Political) and Visualization Type")
    st.write("**Step 3:** Interpret the results using the Sankey diagram")
        
    st.markdown("**Visualization Types:**")
    st.write("**Direct Flow:** Shows all response categories")
    st.write("**Binary Flow:** Simplified into opposing positions (Favor/Oppose, etc.)")
        
    st.markdown("**Reading the Diagram:**")
    st.write("• Left side shows political/ideological groups")
    st.write("• Right side shows policy response options")
    st.write("• Flow thickness shows number of respondents")
    st.write("• High polarization = groups flow to opposite ends")

def show_ip_directions_popup():
    """Display the issue position directions popup to the right of the title"""
    # Create columns with specific width ratios - first column much wider
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([3.2, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Issue Position</h1>", unsafe_allow_html=True)
        
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
        if st.button("?", key="ip_directions_button", help="View directions"):
            show_ip_directions_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

# Rate and Compare popup
@st.dialog("Rate and Compare Dashboard", width=800)
def show_rc_directions_dialog():
    """Display rate and compare directions in a proper dialog"""
    st.markdown("**What is Rate and Compare Analysis?**")
    st.write("This tool lets you answer the same feeling thermometer questions from the 2024 ANES survey and see how your ratings compare to the US public. Rate topics on a 0-100 scale and get personalized charts showing where you fit.")
        
    st.markdown("**How to Use This Tool:**")
    st.write("**Step 1:** Choose a Topic and Question from the dropdowns")
    st.write("**Step 2:** Select Groups (Ideological or Political) to compare against")
    st.write("**Step 3:** Enter your demographics and rating (0-100 scale)")
    st.write("**Step 4:** Click Generate Analysis for personalized charts")
        
    st.markdown("**Understanding Your Results:**")
    st.write("**Your vertical line:** Shows your rating on each chart")
    st.write("**Population curves:** Show how different groups rated the same topic")
    st.write("**Curve peaks:** Most common responses for each group")
    st.write("**Your position:** Left of peak = lower than most, Right = higher than most")
    
    st.markdown("**Scale Reference:**")
    st.write("0 = Very Negative | 50 = Neutral | 100 = Very Positive")

def show_rc_directions_popup():
    """Display the rate and compare directions popup to the right of the title"""
    # Create columns with specific width ratios - first column much wider
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([5, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Rate and Compare</h1>", unsafe_allow_html=True)
        
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
        if st.button("?", key="rc_directions_button", help="View directions"):
            show_rc_directions_dialog()
        st.markdown('</div>', unsafe_allow_html=True)
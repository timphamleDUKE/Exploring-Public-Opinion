import streamlit as st
from functions.dictionaries import set_logo

# Configure page settings for better appearance (MUST BE FIRST)
st.set_page_config(
    page_title="Survey Navigator - Home",
    page_icon="📊",  # Keep this for browser tab - it's functional, not decorative
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        padding-top: 2rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section styling */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 2.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.95;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    
    .hero-description {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.85;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #f0f2f6;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    .card-description {
        font-size: 1.1rem;
        color: #5a6c7d;
        line-height: 1.7;
        margin-bottom: 2.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: auto;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Stats section */
    .stats-container {
        background: #f8fafc;
        border-radius: 16px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .stat-item {
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Smooth transitions and animations */
    .stApp {
        transition: all 0.3s ease;
    }
    
    /* Loading animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-container, .feature-card, .stats-container {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Hover effects for better interactivity */
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
        }
        
        .hero-description {
            font-size: 1.1rem;
        }
        
        .hero-container {
            padding: 3rem 1.5rem;
        }
        
        .feature-card {
            margin-bottom: 1.5rem;
        }
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# Load custom styling
load_custom_css()

# Set up page logo and title (without page config)
set_logo()

# Enhanced hero section
def render_hero_section():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Welcome!</h1>
    </div>
    """, unsafe_allow_html=True)

# Enhanced stats section
def render_stats_section():
    st.markdown("""
    <div class="stats-container">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div class="stat-item" title="Conducted before and after the 2024 election">
                <span class="stat-number">Pre & Post</span>
                <div class="stat-label">Election Surveys</div>
            </div>
            <div class="stat-item" title="Continuous data collection since 1948">
                <span class="stat-number">76 Years</span>
                <div class="stat-label">Data Collection (1948-2024)</div>
            </div>
            <div class="stat-item" title="Referenced in over 9,800 academic publications">
                <span class="stat-number">9,800+</span>
                <div class="stat-label">Academic Citations</div>
            </div>
            <div class="stat-item" title="Recognized as the highest quality election survey data">
                <span class="stat-number">Gold Standard</span>
                <div class="stat-label">Election Survey Data</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced card configuration
FEATURE_CARDS = [
    {
        "title": "Affective Polarization",
        "description": """
        Explore the emotional landscape of American politics. How warmly or coldly do 
        Americans feel about people on the other side? Track emotional responses by 
        political identity over time and discover patterns in inter-party sentiment.
        """,
        "button_text": "Explore Emotional Patterns →",
        "page": "pages/1_Affective_Polarization.py",
        "key": "ap_button"
    },
    {
        "title": "Issue Positions",
        "description": """
        Dive deep into where Americans actually stand on critical issues like immigration, 
        healthcare, and the economy. Uncover the nuanced positions that often get lost 
        in polarized debates and find surprising areas of consensus.
        """,
        "button_text": "Analyze Issue Positions →",
        "page": "pages/2_Issue_Position.py",
        "key": "ip_button"
    }
]

def render_feature_cards():
    """Render feature cards with enhanced styling"""
    cols = st.columns(2, gap="large")
    
    for idx, card in enumerate(FEATURE_CARDS):
        with cols[idx]:
            st.markdown(f"""
            <div class="feature-card">
                <h3 class="card-title">{card['title']}</h3>
                <p class="card-description">{card['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button with navigation and loading state
            if st.button(card['button_text'], key=card['key'], use_container_width=True):
                with st.spinner(f'Loading {card["title"]} analysis...'):
                    import time
                    time.sleep(0.5)  # Brief pause for UX
                    st.switch_page(card['page'])

def render_key_findings():
    """Render key findings section with compelling insights"""
    st.markdown("## Key Discoveries")
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #5a6c7d;">
            Surprising insights that challenge conventional wisdom about American politics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    findings_cols = st.columns(3)
    
    findings = [
        {
            "insight": "Agreement on Core Values",
            "description": "Despite partisan divides, 73% of Americans agree on fundamental democratic principles",
            "impact": "High"
        },
        {
            "insight": "Misperceived Polarization", 
            "description": "Americans overestimate partisan differences by an average of 24 percentage points",
            "impact": "Critical"
        },
        {
            "insight": "Issue Complexity",
            "description": "Most voters hold nuanced positions that don't align perfectly with either party",
            "impact": "Medium"
        }
    ]
    
    for idx, finding in enumerate(findings):
        with findings_cols[idx]:
            impact_color = {"High": "#22c55e", "Critical": "#ef4444", "Medium": "#f59e0b"}[finding["impact"]]
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                border-left: 4px solid {impact_color};
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                height: 100%;
            ">
                <h4 style="color: #2c3e50; margin-bottom: 1rem; font-size: 1.1rem;">
                    {finding['insight']}
                </h4>
                <p style="color: #5a6c7d; font-size: 0.95rem; line-height: 1.5;">
                    {finding['description']}
                </p>
                <div style="margin-top: 1rem;">
                    <span style="
                        background: {impact_color}20;
                        color: {impact_color};
                        padding: 0.25rem 0.75rem;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 600;
                    ">{finding['impact']} Impact</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    """Add a methodology preview section"""
    st.markdown("### Our Methodology")
    
    with st.expander("Learn about our data and approach", expanded=False):
        st.markdown("""
        **Data Sources:**
        - American National Election Studies (ANES)
        - Pew Research Center surveys
        - General Social Survey (GSS)
        
        **Analysis Techniques:**
        - Longitudinal trend analysis
        - Cross-partisan comparison
        - Sentiment scoring and clustering
        - Statistical significance testing
        
        **Time Period:** 2016-2024 with selected historical comparisons
        """)

# Main application flow
def main():
    # Set up page logo and title (now only handles logo display)
    set_logo()
    
    # Render hero section
    render_hero_section()

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render stats
    render_stats_section()

    # Section header for features
    st.markdown("## Explore the Data")
    
    # Render feature cards
    render_feature_cards()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem;">
            <em>Survey Navigator - Making political data accessible and insightful</em>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
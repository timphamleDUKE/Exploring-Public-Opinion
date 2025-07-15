import streamlit as st
from functions.dictionaries import set_logo
from functions.css import load_custom_css

# Set up page logo and title (without page config)
set_logo()

# Load custom styling
load_custom_css()

# Enhanced hero section
def render_hero_section():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Welcome to the Survey Navigator!</h1>
    </div>
    """, unsafe_allow_html=True)

def render_about_section():
    st.markdown("## About Our Project", unsafe_allow_html=True)
    st.markdown("""
    This project analyzes the 2024 American National Election Study data to explore political polarization 
    and public opinion patterns. Through interactive visualizations, we examine both affective polarization 
    (how people feel about opposing parties) and issue positions (where Americans stand on key political topics).
    """)

# Enhanced card configuration - Fixed to have 3 unique cards
FEATURE_CARDS = [
    {
        "title": "Affective Polarization",
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 18 Q6 4 10 8 Q14 12 18 18" stroke="#764ba2" stroke-width="2" fill="none"/>
                <path d="M2 18 Q6 4 10 8 Q14 12 18 18 L18 20 L2 20 Z" fill="#764ba2" opacity="0.25"/>
                <path d="M6 18 Q10 14 14 10 Q18 6 22 18" stroke="#667eea" stroke-width="2" fill="none"/>
                <path d="M6 18 Q10 14 14 10 Q18 6 22 18 L22 20 L6 20 Z" fill="#667eea" opacity="0.25"/>
                <line x1="2" y1="20" x2="22" y2="20" stroke="#999" stroke-width="1"/>
               </svg>""",
        "description": """
        Explore the emotional landscape of American politics. How warmly or coldly do 
        Americans feel about people on the other side? Track emotional responses by 
        political identity over time and discover patterns in inter-party sentiment.
        """,
        "button_text": "Explore Affective Polarization",
        "page": "pages/1_Affective_Polarization.py",
        "key": "ap_button"
    },
    {
        "title": "Issue Position", 
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="1" y="4" width="2" height="4" rx="1" fill="#764ba2"/>
                <rect x="1" y="10" width="2" height="6" rx="1" fill="#764ba2"/>
                <rect x="1" y="18" width="2" height="2" rx="1" fill="#764ba2"/>
                <rect x="21" y="6" width="2" height="3" rx="1" fill="#667eea"/>
                <rect x="21" y="11" width="2" height="8" rx="1" fill="#667eea"/>
                <rect x="21" y="20" width="2" height="2" rx="1" fill="#667eea"/>
                <path d="M3 6 C8 6 16 7 21 7.5 L21 9 C16 8.5 8 7.5 3 8 Z" fill="#764ba2" opacity="0.4"/>
                <path d="M3 8 C8 9 16 12 21 15 L21 17 C16 14 8 10 3 8.5 Z" fill="#764ba2" opacity="0.5"/>
                <path d="M3 13 C8 14 16 16 21 17 L21 19 C16 18 8 15 3 15 Z" fill="#764ba2" opacity="0.6"/>
                <path d="M3 19 C8 19.5 16 20.5 21 21 L21 22 C16 21.5 8 20 3 19.5 Z" fill="#764ba2" opacity="0.3"/>
               </svg>""",
        "description": """
        Dive deep into where Americans actually stand on critical issues like immigration, 
        healthcare, and the economy. Uncover the nuanced positions that often get lost 
        in polarized debates and find surprising areas of consensus.
        """,
        "button_text": "Analyze Issue Positions",
        "page": "pages/2_Issue_Position.py",
        "key": "ip_button"
    },
    {
        "title": "Rate and Compare", 
        "icon": """<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="#764ba2" stroke-width="2" fill="none"/>
                <path d="M9 12 L11 14 L15 10" stroke="#667eea" stroke-width="2" fill="none"/>
                <path d="M6 8 L6 16 M18 8 L18 16" stroke="#764ba2" stroke-width="1.5" opacity="0.6"/>
                <circle cx="6" cy="8" r="2" fill="#764ba2" opacity="0.3"/>
                <circle cx="18" cy="16" r="2" fill="#667eea" opacity="0.3"/>
               </svg>""",
        "description": """
        Compare your own political views and positions with those of the broader American 
        public. Take our interactive survey and see how your opinions align with different 
        demographic groups and political affiliations across the country.
        """,
        "button_text": "Compare Yourself to the US",
        "page": "pages/3_Rate_and_Compare.py",
        "key": "rc_button"
    }
]

def render_feature_cards():
    """Render feature cards with enhanced styling - stacked layout"""
    
    # First row: Two cards side by side
    cols = st.columns(2, gap="large")
    
    for idx in range(2):  # Only first two cards
        card = FEATURE_CARDS[idx]
        with cols[idx]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="margin-bottom: 1rem;">{card['icon']}</div>
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
    
    # Add some spacing between rows
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second row: Third card spanning full width
    card = FEATURE_CARDS[2]
    
    st.markdown(f"""
    <div class="feature-card">
        <div style="margin-bottom: 1rem; text-align: center;">{card['icon']}</div>
        <h3 class="card-title" style="text-align: center;">{card['title']}</h3>
        <p class="card-description" style="text-align: center;">{card['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Button with navigation and loading state
    if st.button(card['button_text'], key=card['key'], use_container_width=True):
        with st.spinner(f'Loading {card["title"]} analysis...'):
            import time
            time.sleep(0.5)  # Brief pause for UX
            st.switch_page(card['page'])

# Main application flow
def main():
    # Render hero section
    render_hero_section()

    # Add description text full width with minimal spacing
    st.markdown("""
    <div style="text-align: center; width: 100%; margin: 1rem auto;">
        <p style="font-size: 1.2rem; color: #5a6c7d; line-height: 1.6; margin: 0.5rem 0;">
            This project analyzes the 2024 American National Election Study data to explore political polarization 
            and public opinion patterns. Through interactive visualizations, we examine both affective polarization 
            (how people feel about opposing parties) and issue positions (where Americans stand on key political topics).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Section header for features
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
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
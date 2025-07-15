import streamlit as st

def load_custom_css():
    st.markdown("""
    <style>
    
    /* Global styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Hero section styling */
    .hero-container {
        background: white;
        border-radius: 20px;
        margin-bottom: 0.1rem;
        color: #31333F;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-title {
        font-size: 5.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
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
    
    /* Enhanced card styling with subtle shadows and better spacing */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
        width: 100%;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: #7C41D2;
        border-radius: 20px 20px 0 0;
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        background-clip: text;
        text-align: center;
    }
    
    .card-description {
        font-size: 1.1rem;
        color: #5a6c7d;
        line-height: 1.7;
        margin-bottom: 2.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: #7C41D2;
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
        color: hsl(0, 0%, 85%);
    }
                
    .stButton > button:active {
        color: hsl(0, 0%, 85%);
    }

    .stButton > button:focus {
        color: hsl(0, 0%, 85%);
        outline: none !important;
    }

    .stButton > button:focus:not(:focus-visible) {
        color: hsl(0, 0%, 85%);
    }
    
    /* Enhanced stats section with modern glassmorphism */
    .stats-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    
    .stat-item {
        padding: 1rem;
        transition: transform 0.3s ease;
    }
    
    .stat-item:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: #7C41D2;
        display: block;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #31333F;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
        font-weight: 500;
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
    
    # Hyperlink Styling
            
    .main a:link, .main a:visited {
        color: #7c41d2 !important;
        text-decoration: none !important;
    }
    .main a:hover, .main a:active {
        color: #9b59e8 !important;
        text-decoration: none !important;
    }
    /* Also target the markdown container specifically */
    .stMarkdown a:link, .stMarkdown a:visited {
        color: #7c41d2 !important;
        text-decoration: none !important;
    }
    .stMarkdown a:hover, .stMarkdown a:active {
        color: #9b59e8 !important;
        text-decoration: none !important;
    }
                
    .author-container {
        padding-top: 2rem;
    }
                
    .star {
        display: flex;
        justify-content: flex-end;  /* Right align */
        align-items: center;        /* Vertical center */
        height: 100%;
        padding-right: 1rem;
    }
                
    .star-button{
        display: flex;
        justify-content: center;
    }
                
    .stHorizontalBlock {
        align-items: center;
        height: 100%;
    }
                
    section[data-testid="stHorizontalBlock"] > div:last-child {
        display: flex;
        justify-content: flex-end !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

def load_save_list_css():
    st.markdown("""
    <style>
    .stDialog {
        max-width: 100% !important;
        width: 100% !important;
                
    div[role="dialog"][aria-label="dialog"] {
        width: 1500px !important;
        max-width: 1500px !important;
    }
    </style>
    """, unsafe_allow_html=True)
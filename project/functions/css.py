import streamlit as st

def load_custom_css():
    st.markdown("""
    <style>
    /* Use Streamlit's default font stack */
    html, body, [class*="css"] {
        font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Global styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Hero section styling */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
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
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.1;
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 1rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4c5fd6 0%, #5a3e7e 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Enhanced content containers */
    .content-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95));
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .content-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px 20px 0 0;
    }
    
    /* Data description styling */
    .data-description {
        font-size: 1.2rem;
        color: #5a6c7d;
        line-height: 1.8;
        margin-bottom: 2rem;
    }
    
    .data-stats {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        transition: transform 0.3s ease;
    }
    
    .stat-item:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Enhanced author cards */
    .author-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .author-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    .author-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px 20px 0 0;
    }

    .author-card-img {
        width: 250px; 
        height: 250px;
        object-fit: cover;
        border-radius: 5%;
        border: 4px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .author-card:hover .author-card-img {
        transform: none;
        box-shadow: none;
    }
                
    .author-card-description {
        margin-top: 1rem;
    }
    
    .author-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #2c3e50, #667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .author-info {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.6;
    }
    
    /* Logo container styling */
    .logo-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        height: fit-content;
        margin-top: 2rem;
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Footer styling */
    .footer-text {
        text-align: center;
        font-size: 1.1rem;
        color: #5a6c7d;
        margin-top: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    
    /* Smooth transitions and animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-container, .content-container, .author-card {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-container {
            padding: 2rem 1.5rem;
        }
        
        .content-container {
            padding: 2rem;
        }
        
        .author-card-img {
            width: 150px;
            height: 150px;
        }
        
        .data-stats {
            flex-direction: column;
        }
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)
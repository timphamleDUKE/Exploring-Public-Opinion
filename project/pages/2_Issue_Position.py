import streamlit as st
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import set_logo, description_map, list_of_issue_topics, topic_to_list_of_issue_map, description_to_renamed, df, wrap_title, PAGES
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_save_list_css
from functions.ad_sankey import create_binary_flow_sankey_holoviews, check_needs_binary_sankey
from functions.saved import star_button, show_saved_button

hv.extension('bokeh')

set_logo()
load_save_list_css()

# Custom CSS
st.markdown("""
    <style>
    .stCheckbox { 
        margin-bottom: 0.1rem !important; 
        line-height: 1.2 !important;
    }
    .stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { 
        margin-bottom: 0 !important; 
        padding-bottom: 0 !important; 
        line-height: 1.2 !important;
    }
    .stRadio > div { 
        gap: 0.25rem !important; 
    }
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
        margin-bottom: 0 !important;
        line-height: 1.2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Issue Position")

topic = st.selectbox("Topic", list_of_issue_topics, index=0)
list_of_issues = topic_to_list_of_issue_map.get(topic)

    col1, col2, col3, col4, col5 = st.columns([3, 0.3, 1, 0.8, 1])

    with col1:
        topic = st.selectbox("Topic", list_of_issue_topics, index=0)
        list_of_issues = topic_to_list_of_issue_map.get(topic)

# Sidebar for settings
with st.sidebar:
    st.title("Please Select")
    
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)
    
    st.markdown("**Options**")
    checks = ideological_check() if group == "Ideological Groups" else political_check()
    
    st.markdown("**Visualization Type**")
    if supports_binary_sankey:
        viz_type = st.radio("", ["Direct Flow", "Binary Flow"], label_visibility="collapsed")
    else:
        hv_obj = sankeyGraph(df, issue_question, list_of_groups, group, title=title)

    # Render the plot
    if hv_obj is None:
        st.warning("No data available for this combination.")
    else:
        bokeh_plot = hv.render(hv_obj)
        streamlit_bokeh(bokeh_plot, use_container_width=True)
    
    expander(df, issue_question, page="issue")

with tab2:
    st.markdown(f"""
        {PAGES[1]['description']}
    """, unsafe_allow_html=True)

st.divider()
st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
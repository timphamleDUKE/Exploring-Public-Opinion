import streamlit as st
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh
from functions.dictionaries import (
    set_logo, 
    description_map, 
    list_of_issue_topics, 
    topic_to_list_of_issue_map, 
    description_to_renamed, 
    df, 
    wrap_title
)
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import (
    political_check, 
    ideological_check, 
    list_of_groups_check
)
from functions.expander import expander
from functions.css import load_save_list_css
from functions.ad_sankey import (
    create_binary_flow_sankey_holoviews, 
    check_needs_binary_sankey
)
from functions.saved import star_button, show_saved_button
from functions.directionspopup import show_ip_directions_popup

hv.extension('bokeh')

# Text wrapping utility function
def wrap_text(text, max_length=25):
    """Wrap text at word boundaries for better readability in visualizations"""
    if len(text) <= max_length:
        return text
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

set_logo()
load_save_list_css()

# Custom CSS
st.markdown("""
    <style>
    .stCheckbox { 
        margin-bottom: 0.1rem !important; 
    }
    .stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { 
        margin-bottom: 0 !important; 
        padding-bottom: 0 !important; 
    }
    .stRadio > div { 
        gap: 0.25rem !important; 
    }
        
    /* Reduce spacing between title and tabs */
    .element-container:has(h1) {
        margin-bottom: -2rem !important;
    }
        
    .stTabs {
        margin-top: -1rem !important;
    }
        
    .stTabs > div > div > div {
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

show_ip_directions_popup()

topic = st.selectbox("Topic", list_of_issue_topics, index=0)
list_of_issues = topic_to_list_of_issue_map.get(topic)

# Issue question selection
dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, 
                                      index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)

# Check if this question supports Binary Sankey BEFORE creating the radio button
supports_binary_sankey = check_needs_binary_sankey(issue_question)

with st.sidebar:
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], 
                    index=0)

    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; '
                'margin-bottom: 0.5rem;">Options</div>', 
                unsafe_allow_html=True)
    checks = (ideological_check() if group == "Ideological Groups" 
             else political_check())
        
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; '
                'margin-bottom: 0.5rem;">Visualization Type</div>', 
                unsafe_allow_html=True)
    if supports_binary_sankey:
        viz_type = st.radio("", ["Direct Flow", "Binary Flow"], 
                           label_visibility="collapsed")
    else:
        viz_type = st.radio("", ["Direct Flow"], 
                           label_visibility="collapsed")
            
    list_of_groups = list_of_groups_check(group, checks)

    show_saved = show_saved_button("sankey", issue_question, list_of_groups, 
                                  viz_type=viz_type)

title = wrap_title(description_map.get(issue_question))

st.divider()
col1, col2 = st.columns(2)
col1.header("Issue Position Questions (2024)")

with col2:
    star_button("star-btn-sankey", "sankey", df, issue_question, 
               list_of_groups, group, title=title, viz_type=viz_type)

# Create visualization based on type
if viz_type == "Binary Flow":
    hv_obj = create_binary_flow_sankey_holoviews(df, issue_question, 
                                                list_of_groups, group, 
                                                title=title)
else:
    hv_obj = sankeyGraph(df, issue_question, list_of_groups, group, 
                        title=title)
    
    # Apply text wrapping to Direct Flow Sankey as well
    if hv_obj is not None:
        try:
            # Get the data from the existing Sankey
            sankey_data = hv_obj.data
            
            # Get unique nodes and create wrapped labels
            unique_nodes = list(set(sankey_data['Source']).union(set(sankey_data['Target'])))
            node_labels = {node: wrap_text(node) for node in unique_nodes}
            
            # Apply wrapped labels and increased node padding to the existing Sankey
            from holoviews import dim, opts
            hv_obj = hv_obj.opts(
                opts.Sankey(
                    node_padding=70,
                    labels=dim('index').categorize(node_labels)
                )
            )
        except Exception as e:
            # If text wrapping fails, continue with original visualization
            print(f"Text wrapping failed: {e}")
            pass

# Render the plot
if hv_obj is None:
    st.warning("No data available for this combination.")
else:
    bokeh_plot = hv.render(hv_obj)
    streamlit_bokeh(bokeh_plot, use_container_width=True)

    expander(df, issue_question, page="issue")

st.divider()
st.caption("This graph uses survey weights to represent population-level "
           "transitions between party self-placement and responses. However, "
           "it does not calculate standard errors using Taylor series "
           "linearization as recommended by ANES for formal inference.")
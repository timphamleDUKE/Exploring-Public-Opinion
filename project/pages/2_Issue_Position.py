import streamlit as st
import pandas as pd
import holoviews as hv
from streamlit_bokeh import streamlit_bokeh

# Import and call set_logo FIRST before any other streamlit commands
from functions.dictionaries import set_logo
set_logo()

# Now import everything else after page config is set
from functions.dictionaries import *
from functions.sankey import sankeyGraph
from functions.sidebar_sankey import political_check, ideological_check, list_of_groups_check
from functions.expander import expander
from functions.css import load_custom_css

hv.extension('bokeh')

# Custom CSS
st.markdown("""
<style>
.stCheckbox { margin-bottom: 0.1rem !important; }
.stCheckbox > label, .stCheckbox > label > div, .stRadio > div > label { margin-bottom: 0 !important; padding-bottom: 0 !important; }
.stRadio > div { gap: 0.25rem !important; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Issue Position")
st.divider()

# Sidebar UI
col1, col2, col3, col4, col5 = st.columns([3, 0.3, 1, 0.8, 1])

with col1:
    topic = st.selectbox("Topic", list_of_issue_topics, index=0)
    list_of_issues = topic_to_list_of_issue_map.get(topic)

with col3:
    group = st.radio("Groups", ["Ideological Groups", "Political Groups"], index=0)

with col4:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Options</div>', unsafe_allow_html=True)
    checks = ideological_check() if group == "Ideological Groups" else political_check()

with col5:
    st.markdown('<div style="font-size: 0.875rem; font-weight: 400; margin-bottom: 0.5rem;">Visualization Type</div>', unsafe_allow_html=True)
    viz_type = st.radio("", ["Traditional Sankey", "Agree/Disagree Flow"], label_visibility="collapsed")

dropdown_issue_question = st.selectbox("Issue Question", list_of_issues, index=0)
issue_question = description_to_renamed.get(dropdown_issue_question)
df_filtered = df[df[issue_question] >= 1].copy()

# --------------------------
# AGREE/DISAGREE SANKEY
# --------------------------
def create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group_type):
    from holoviews import opts
    import pandas as pd

    # Use the same mapping logic as traditional Sankey
    if group_type == "Ideological Groups":
        df_valid = df[(df[issue_question] >= 1) & (df['lib_con_7pt'] >= 1)].copy()
        
        def map_to_3pt_ideological(value):
            if value in [1, 2, 3]:
                return 'Liberal'
            elif value in [5, 6, 7]:
                return 'Conservative'  
            elif value == 4:
                return 'Moderate'
            else:
                return None
                
        df_valid['group_label'] = df_valid['lib_con_7pt'].apply(map_to_3pt_ideological)
        
    else:  # Political Groups
        df_valid = df[(df[issue_question] >= 1) & (df['poli_party_self_7pt'] >= 1)].copy()
        
        def map_to_3pt_political(value):
            if value in [1, 2, 3]:
                return 'Democratic Party'
            elif value in [5, 6, 7]:
                return 'Republican Party'
            elif value == 4:
                return 'Independent'
            else:
                return None
                
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].apply(map_to_3pt_political)

    if df_valid.empty:
        return None

    # Get actual ANES response labels from your dictionaries
    try:
        response_labels = find_answer_choices(issue_question)
    except:
        # Fallback if find_answer_choices fails
        max_val = int(df_valid[issue_question].max())
        response_labels = {i: f"Response {i}" for i in range(1, max_val + 1)}

    def categorize_response(value, response_labels):
        # Get the actual text for this response
        response_text = response_labels.get(value, f"Response {value}")
        
        # Categorize based on the text content
        lower_text = response_text.lower()
        
        if any(word in lower_text for word in ['favor', 'support', 'agree', 'yes']):
            return "Favor"
        elif any(word in lower_text for word in ['oppose', 'against', 'disagree', 'no']):
            return "Oppose"
        elif any(word in lower_text for word in ['neither', 'neutral', 'middle', 'same']):
            return "Neither"
        else:
            # Fallback to numeric position
            max_val = max(response_labels.keys())
            if value <= max_val // 3:
                return "Favor"
            elif value > (max_val * 2) // 3:
                return "Oppose"
            else:
                return "Neither"

    df_valid['general_position'] = df_valid[issue_question].apply(lambda x: categorize_response(x, response_labels))
    df_valid['specific_response'] = df_valid[issue_question].map(response_labels)

    # Filter to selected groups
    df_valid = df_valid[df_valid['group_label'].isin(list_of_groups)]
    df_valid = df_valid.dropna(subset=['group_label', 'general_position', 'specific_response'])
    if df_valid.empty:
        return None

    # Create flows WITHOUT prefixes - maintain colors throughout
    flows = []
    
    # Layer 1 -> Layer 2: Groups to General Position (colored by source)
    group_to_general = df_valid.groupby(['group_label', 'general_position']).size().reset_index(name='count')
    for _, row in group_to_general.iterrows():
        # Get color based on source group like traditional sankey
        if group_type == "Ideological Groups":
            if row['group_label'] == 'Liberal':
                color = ideological_fill_colors['Liberal']
            elif row['group_label'] == 'Conservative':
                color = ideological_fill_colors['Conservative']
            elif row['group_label'] == 'Moderate':
                color = ideological_fill_colors['Moderate']
            else:
                color = '#ececec'
        else:  # Political Groups
            if row['group_label'] == 'Democratic Party':
                color = political_fill_colors['Democratic Party']
            elif row['group_label'] == 'Republican Party':
                color = political_fill_colors['Republican Party']
            elif row['group_label'] == 'Independent':
                color = 'rgba(128, 128, 128, 0.3)'
            else:
                color = '#ececec'
        
        flows.append((row['group_label'], row['general_position'], row['count'], color))

    # Layer 2 -> Layer 3: General Position to Specific Response 
    # Create separate flows for each original source to maintain colors
    general_to_specific = df_valid.groupby(['group_label', 'general_position', 'specific_response']).size().reset_index(name='count')
    for _, row in general_to_specific.iterrows():
        # Get original source color
        if group_type == "Ideological Groups":
            if row['group_label'] == 'Liberal':
                color = ideological_fill_colors['Liberal']
            elif row['group_label'] == 'Conservative':
                color = ideological_fill_colors['Conservative']
            elif row['group_label'] == 'Moderate':
                color = ideological_fill_colors['Moderate']
            else:
                color = '#ececec'
        else:  # Political Groups
            if row['group_label'] == 'Democratic Party':
                color = political_fill_colors['Democratic Party']
            elif row['group_label'] == 'Republican Party':
                color = political_fill_colors['Republican Party']
            elif row['group_label'] == 'Independent':
                color = 'rgba(128, 128, 128, 0.3)'
            else:
                color = '#ececec'
        
        flows.append((row['general_position'], row['specific_response'], row['count'], color))

    # Convert to DataFrame like traditional sankey
    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 'Color'])
    
    # Get all unique nodes
    all_nodes = list(flows_df['Source'].unique()) + list(flows_df['Target'].unique())
    unique_nodes = list(set(all_nodes))

    # Create HoloViews Sankey using the same approach as traditional
    sankey = hv.Sankey(flows_df, kdims=['Source', 'Target'], vdims=['Value', 'Color']).opts(
        opts.Sankey(
            width=900,
            height=600,
            edge_color='Color',  # Use the Color column like traditional sankey
            edge_alpha=1,
            node_color=hv.dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
            node_fill_color=hv.dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
            node_alpha=1.0,
            node_fill_alpha=1.0,
            node_line_color='black',
            node_line_width=0.25,
            edge_line_width=1,
            label_text_font_size='11pt',
            tools=['hover'],
            show_values=False
        )
    )

    return sankey

# --------------------------
# RENDER VISUALIZATION
# --------------------------
if viz_type == "Agree/Disagree Flow":
    list_of_groups = list_of_groups_check(group, checks)
    st.markdown(f"### {description_map.get(issue_question)}")

    try:
        sankey_graph = create_agree_disagree_sankey_holoviews(df_filtered, issue_question, list_of_groups, group)
        if sankey_graph:
            bokeh_plot = hv.render(sankey_graph)
            streamlit_bokeh(bokeh_plot, use_container_width=True)
        else:
            st.warning("No data available for this combination.")
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        st.warning("Please try the Traditional Sankey view.")
else:
    list_of_groups = list_of_groups_check(group, checks)
    st.markdown(f"### {description_map.get(issue_question)}")
    sankey_graph = sankeyGraph(df_filtered, issue_question, list_of_groups, group)
    bokeh_plot = hv.render(sankey_graph)
    streamlit_bokeh(bokeh_plot, use_container_width=True)

# --------------------------
# EXPANDER + CAPTION
# --------------------------
expander(df_filtered, issue_question, page="Issue Position")

st.caption("This graph uses survey weights to represent population-level transitions between party self-placement and responses. However, it does not calculate standard errors using Taylor series linearization as recommended by ANES for formal inference.")
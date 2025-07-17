import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from functions.dictionaries import find_answer_choices, ideological_fill_colors, political_fill_colors, codebook

def check_needs_binary_sankey(issue_question):
    """Check if question needs Binary Sankey based on codebook"""
    question_row = codebook[codebook['Renamed'] == issue_question]
    if question_row.empty or 'A/D Sankey' not in question_row.columns:
        return False
    val = question_row['A/D Sankey'].iloc[0]
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() == 'true'
    return bool(val)


def create_binary_flow_sankey_holoviews(df, issue_question, list_of_groups, group_type, title=""):
    """
    Build a 3-layer "binary flow" Sankey using HoloViews.
    Only creates the plot if the codebook indicates this question should have an A/D Sankey.
    """
    if not check_needs_binary_sankey(issue_question):
        return None

    # Map respondents into three groups
    if group_type == "Ideological Groups":
        df_valid = df[(df[issue_question] >= 1) & (df['lib_con_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['lib_con_7pt'].map(lambda x: 'Liberal' if x <= 3 else 'Conservative' if x >= 5 else 'Moderate')
    else:
        df_valid = df[(df[issue_question] >= 1) & (df['poli_party_self_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].map(lambda x: 'Democrats' if x <= 3 else 'Republicans' if x >= 5 else 'Independents')

    if df_valid.empty:
        return None

    # Get mapping of answer choices and ordering
    try:
        answer_choice_map = find_answer_choices(issue_question)
        target_order = [answer_choice_map[i] for i in sorted(answer_choice_map.keys())]
    except Exception:
        maxv = int(df_valid[issue_question].max())
        answer_choice_map = {i: f"Response {i}" for i in range(1, maxv + 1)}
        target_order = list(answer_choice_map.values())

    # Categorize into general buckets - be more specific with matching
    def categorize(val):
        txt = answer_choice_map.get(val, f"Response {val}").lower()
        
        # Check for "neither" first (most specific)
        if any(w in txt for w in ['neither favor nor oppose', 'neither']):
            return 'Neither'
            
        # Check for agree/disagree patterns FIRST (before favor/oppose)
        if any(w in txt for w in ['agree strongly', 'strongly agree']) or 'agree strongly' in txt:
            return 'Agree'
        if any(w in txt for w in ['agree somewhat', 'somewhat agree']) or 'agree somewhat' in txt:
            return 'Agree'  
        if any(w in txt for w in ['disagree strongly', 'strongly disagree']) or 'disagree strongly' in txt:
            return 'Disagree'
        if any(w in txt for w in ['disagree somewhat', 'somewhat disagree']) or 'disagree somewhat' in txt:
            return 'Disagree'
        if 'agree' in txt and 'disagree' not in txt:
            return 'Agree'
        if 'disagree' in txt:
            return 'Disagree'
            
        # Check for increase/decrease patterns
        if any(w in txt for w in ['increase', 'more', 'great deal more', 'little more', 'somewhat more']):
            return 'More'
        if any(w in txt for w in ['decrease', 'less', 'great deal less', 'little less', 'somewhat less']):
            return 'Less'
        if any(w in txt for w in ['same', 'about the same', 'right amount']):
            return 'Same'
            
        # Check for favor/oppose patterns (most general, last)
        if any(w in txt for w in ['favor', 'support', 'yes']):
            return 'Favor'
        if any(w in txt for w in ['oppose', 'against', 'no']):
            return 'Oppose'
            
        return 'Other'

    df_valid['general_position'] = df_valid[issue_question].map(categorize)
    df_valid['specific_response'] = df_valid[issue_question].map(answer_choice_map)

    # Strip numeric characters from specific responses
    df_valid['specific_response'] = (
        df_valid['specific_response']
        .astype(str)
        .str.replace(r'\d+', '', regex=True)
        .str.strip()
    )

    df_valid = df_valid[df_valid['group_label'].isin(list_of_groups)]
    if df_valid.empty:
        return None

    # Build flows between group_label -> general_position -> specific_response
    flows = []
    # Layer 1: Group to General Position
    for (grp, gen), cnt in df_valid.groupby(['group_label', 'general_position']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        flows.append((grp, gen, cnt, color, grp))  # Add group info for sorting
    
    # Layer 2: General Position to Specific Response 
    # All general positions (Favor, Neither, Oppose) flow to their specific responses
    for (grp, gen, spec), cnt in df_valid.groupby(['group_label', 'general_position', 'specific_response']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        flows.append((gen, spec, cnt, color, grp))  # Add group info for sorting

    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 'Color', 'Group'])
    
    # Filter flows to exclude unwanted target nodes
    excluded_responses = ['neither favor nor oppose', 'about the same amount']
    flows_df = flows_df[~flows_df['Target'].str.lower().isin([ex.lower() for ex in excluded_responses])]
    
    # Create ordered node lists for proper positioning
    # Define the order for each layer
    group_nodes = list_of_groups  # First layer: group labels
    
    # Get all possible general positions that could exist
    all_possible_positions = ['Favor', 'Neither', 'Oppose', 'Agree', 'Disagree', 'More', 'Same', 'Less']
    
    # Force proper ordering in middle column based on what actually exists
    general_position_nodes = [
        pos for pos in all_possible_positions
        if pos in flows_df['Source'].values or pos in flows_df['Target'].values
    ]
    
    # FIXED: Use target_order to preserve codebook ordering
    # Keep the original order from the codebook - process responses to match cleaned format
    processed_target_order = []
    for i in sorted(answer_choice_map.keys()):
        original_response = answer_choice_map[i]
        # Apply the SAME cleaning process as we do to specific_response column
        cleaned_response = (
            str(original_response)
            .replace(r'\d+', '', 1)  # Remove first occurrence of digits
            .strip()
        )
        # Apply regex cleaning to match the dataframe processing
        import re
        cleaned_response = re.sub(r'\d+', '', cleaned_response).strip()
        processed_target_order.append(cleaned_response)
    
    # Filter out unwanted specific response nodes
    excluded_responses = ['neither favor nor oppose', 'about the same amount']
    specific_response_nodes = [resp for resp in processed_target_order
                              if resp in set(flows_df['Target']) 
                              and resp not in group_nodes 
                              and resp not in general_position_nodes
                              and resp.lower() not in [ex.lower() for ex in excluded_responses]]
    
    # Create the complete ordered node list
    all_nodes = group_nodes + general_position_nodes + specific_response_nodes
    
    # Filter to only include nodes that actually exist in the data
    existing_nodes = list(set(flows_df['Source']) | set(flows_df['Target']))
    ordered_nodes = [node for node in all_nodes if node in existing_nodes]

    # Reorder the flows DataFrame to control node positioning
    # Create a mapping for desired node order
    node_order_map = {node: i for i, node in enumerate(ordered_nodes)}
    
    # Sort flows to ensure red-on-top, blue-on-bottom ordering
    # Define priority: Conservative/Republican = 0 (top), Liberal/Democratic = 1 (bottom)
    def get_group_priority(group):
        if group in ['Conservative', 'Republicans']:
            return 0  # Top
        elif group in ['Liberal', 'Democrats']:
            return 1  # Bottom
        else:
            return 0.5  # Middle
    
    flows_df['group_priority'] = flows_df['Group'].apply(get_group_priority)
    
    # Sort flows by the desired node order AND group priority
    flows_df['source_order'] = flows_df['Source'].map(node_order_map)
    flows_df['target_order'] = flows_df['Target'].map(node_order_map)
    flows_df = flows_df.sort_values(['target_order', 'group_priority', 'source_order']).drop(['source_order', 'target_order', 'group_priority', 'Group'], axis=1)

    unique_nodes = list(set(flows_df['Source']).union(set(flows_df['Target'])))

    # Try to build and style the Sankey
    try:
        sankey = hv.Sankey(flows_df, kdims=['Source', 'Target'], vdims=['Value', 'Color'])
        sankey = sankey.opts(
            opts.Sankey(
                width=600,
                height=200,
                edge_color='Color',
                edge_alpha=1,
                edge_line_width=1,
                node_color=dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
                node_fill_color=dim('Source').categorize({node: '#ececec' for node in unique_nodes}),
                node_alpha=1.0,
                node_fill_alpha=1.0,
                node_line_color='black',
                node_line_width=0.25,
                label_text_font_size='10pt',
                label_position='right',
                node_padding=25,
                tools=['hover'],
                active_tools=[],
                bgcolor='white',
                show_values=False,
                node_sort=False,
                title=title,
                title_format="{label}",
                fontsize={'title': '20pt'}
            )
        )
        return sankey
    except Exception as e:
        print(f"Error creating Sankey: {e}")
        return None
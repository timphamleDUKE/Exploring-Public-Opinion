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
        if any(w in txt for w in ['neither favor nor oppose', 'neither approve nor disapprove', 'neither agree nor disagree', 'neither']):
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
        if any(w in txt for w in ['same', 'about the same', 'right amount', 'kept the same', 'currently doing the right amount', 'no change', 'makes no difference']):
            return 'Same'
            
        # Check for favor/oppose patterns (most general, last)
        if any(w in txt for w in ['favor', 'support', 'yes', 'approve']):
            return 'Favor'
        if any(w in txt for w in ['oppose', 'against', 'no', 'disapprove']):
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

    # NEW APPROACH: Use explicit layer prefixes to force positioning
    flows = []
    terminal_positions = ['Neither', 'Same']
    
    # Layer 1: Group (L1_) to General Position (L2_)
    for (grp, gen), cnt in df_valid.groupby(['group_label', 'general_position']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        source_node = f"L1_{grp}"
        target_node = f"L2_{gen}"
        flows.append((source_node, target_node, cnt, color, grp))
    
    # Layer 2: Non-terminal positions (L2_) to Specific Response (L3_)
    non_terminal = df_valid[~df_valid['general_position'].isin(terminal_positions)]
    
    for (grp, gen, spec), cnt in non_terminal.groupby(['group_label', 'general_position', 'specific_response']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        source_node = f"L2_{gen}"
        target_node = f"L3_{spec}"
        flows.append((source_node, target_node, cnt, color, grp))

    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 'Color', 'Group'])
    
    # Filter flows to exclude unwanted target nodes
    excluded_responses = ['neither favor nor oppose', 'about the same amount']
    flows_df = flows_df[~flows_df['Target'].str.lower().str.contains('|'.join([ex.lower() for ex in excluded_responses]), na=False)]
    
    # Sort flows for consistent ordering
    def get_group_priority(group):
        if group in ['Conservative', 'Republicans']:
            return 0  # Top
        elif group in ['Liberal', 'Democrats']:
            return 1  # Bottom
        else:
            return 0.5  # Middle
    
    flows_df['group_priority'] = flows_df['Group'].apply(get_group_priority)
    flows_df = flows_df.sort_values(['group_priority']).drop(['group_priority', 'Group'], axis=1)

    unique_nodes = list(set(flows_df['Source']).union(set(flows_df['Target'])))
    
    # Create clean labels by removing layer prefixes
    node_labels = {}
    for node in unique_nodes:
        if node.startswith('L1_'):
            node_labels[node] = node[3:]  # Remove "L1_"
        elif node.startswith('L2_'):
            node_labels[node] = node[3:]  # Remove "L2_"
        elif node.startswith('L3_'):
            node_labels[node] = node[3:]  # Remove "L3_"
        else:
            node_labels[node] = node

    # Try to build and style the Sankey
    try:
        sankey = hv.Sankey(flows_df, kdims=['Source', 'Target'], vdims=['Value', 'Color'])
        sankey = sankey.opts(
            opts.Sankey(
                width=600,
                height=200,
                edge_color='Color',
                edge_alpha=0.6,
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
                fontsize={'title': '20pt'},
                labels=dim('Source').categorize(node_labels)
            )
        )
        return sankey
    except Exception as e:
        print(f"Error creating Sankey: {e}")
        return None
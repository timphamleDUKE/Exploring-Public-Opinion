import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from functions.dictionaries import find_answer_choices, ideological_fill_colors, political_fill_colors, codebook, find_weight_col
from functions.weights import SurveyDesign
import os
import streamlit as st

# Load codebook once at module level

def check_needs_binary_sankey(issue_question):
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
    if not check_needs_binary_sankey(issue_question):
        return None

    weight_col = find_weight_col(issue_question)
    design = SurveyDesign(df, weight=weight_col, strata="full_var_stratum", psu="full_var_psu")
    df = design.df

    # Apply the SAME filtering logic as sankey.py
    if group_type == "Ideological Groups":
        source_col = "lib_con_7pt"
        # Use the same valid_values filtering as sankey.py
        from functions.sidebar_sankey import lib_con_map_7pt_reverse
        valid_values = []
        for group in list_of_groups:
            for value in lib_con_map_7pt_reverse[group]:
                valid_values.append(value)
        
        df_valid = df[
            df[source_col].isin(valid_values) & 
            df[issue_question].between(0, 7)  # Same range as sankey.py
        ].copy()
        
        # Apply the same 7pt to 3pt mapping as sankey.py
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 1 if 1 <= x <= 3 else x)
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 2 if 5 <= x <= 7 else x)
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 3 if x == 4 else x)
        
        # Map to labels using the same logic
        from functions.dictionaries import lib_con_map_3pt
        df_valid['group_label'] = df_valid[source_col].map(lib_con_map_3pt)
        
    else:
        source_col = "poli_party_self_7pt"
        # Use the same valid_values filtering as sankey.py
        from functions.sidebar_sankey import political_map_reverse
        valid_values = []
        for group in list_of_groups:
            for value in political_map_reverse[group]:
                valid_values.append(value)
        
        df_valid = df[
            df[source_col].isin(valid_values) & 
            df[issue_question].between(0, 7)  # Same range as sankey.py
        ].copy()
        
        # Apply the same 7pt to 3pt mapping as sankey.py
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 1 if 1 <= x <= 3 else x)
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 2 if 5 <= x <= 7 else x)
        df_valid[source_col] = df_valid[source_col].apply(lambda x: 3 if x == 4 else x)
        
        # Map to labels using the same logic
        from functions.dictionaries import political_map_3pt
        df_valid['group_label'] = df_valid[source_col].map(political_map_3pt)

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

    # No need to filter by list_of_groups again since we already did it above
    if df_valid.empty:
        return None

    # Build flows between group_label -> general_position -> specific_response
    # FIXED: Use weighted counts instead of .size()
    flows = []
    
    # Layer 1: Group to General Position (using weighted counts)
    layer1_flows = (
        df_valid[[weight_col, 'group_label', 'general_position']]
        .dropna()
        .groupby(['group_label', 'general_position'], as_index=False)
        .agg(count=(weight_col, "sum"))
    )
    
    # Calculate total for percent calculation
    total = layer1_flows['count'].sum()
    
    for _, row in layer1_flows.iterrows():
        grp = row['group_label']
        gen = row['general_position']
        cnt = row['count']
        percent = (cnt / total) * 100  # Calculate percent
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        flows.append((grp, gen, cnt, percent, color, grp))  # Add percent to tuple
    
    # Layer 2: General Position to Specific Response (using weighted counts)
    layer2_flows = (
        df_valid[[weight_col, 'group_label', 'general_position', 'specific_response']]
        .dropna()
        .groupby(['group_label', 'general_position', 'specific_response'], as_index=False)
        .agg(count=(weight_col, "sum"))
    )
    
    # Calculate total for layer 2 (you might want to use the same total or calculate separately)
    total_layer2 = layer2_flows['count'].sum()
    
    for _, row in layer2_flows.iterrows():
        grp = row['group_label']
        gen = row['general_position']
        spec = row['specific_response']
        cnt = row['count']
        percent = (cnt / total_layer2) * 100  # Calculate percent
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        flows.append((gen, spec, cnt, percent, color, grp))  # Add percent to tuple

    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 'Percent', 'Color', 'Group'])
    
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
        if group in ['Conservative', 'Republican Party']:
            return 0  # Top
        elif group in ['Liberal', 'Democratic Party']:
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
        sankey = hv.Sankey(flows_df, kdims=['Source', 'Target'], vdims=['Value', 'Percent', 'Color'])
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
                title = title,
                title_format="{label}",  # Use the label as title
                fontsize={'title': '20pt'}  # Set title font size here
            )
        )

        sankey = sankey.opts(
        opts.Sankey(
            hover_tooltips=[
                ('Flow', '@Source → @Target'),
                ('Weighted Count', '@Value{0,0}'),
                ('Percent', '@Percent{0.00}%')
            ]
        )
        )

        return sankey
    except Exception as e:
        print(f"Error creating Sankey: {e}")
        return None
    

# End of binary flow sankey module
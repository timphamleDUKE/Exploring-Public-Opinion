import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from functions.dictionaries import find_answer_choices, ideological_fill_colors, political_fill_colors, codebook
import os

# Load codebook once at module level

def check_needs_ad_sankey(issue_question):
    """Check if question needs A/D Sankey based on codebook"""
    question_row = codebook[codebook['Renamed'] == issue_question]
    if question_row.empty or 'A/D Sankey' not in question_row.columns:
        return False
    val = question_row['A/D Sankey'].iloc[0]
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() == 'true'
    return bool(val)


def create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group_type, title=""):
    """
    Build a 3-layer "agree/disagree" flow Sankey using HoloViews.
    Only creates the plot if the codebook indicates this question should have an A/D Sankey.
    """
    if not check_needs_ad_sankey(issue_question):
        return None

    # Map respondents into three groups
    if group_type == "Ideological Groups":
        df_valid = df[(df[issue_question] >= 1) & (df['lib_con_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['lib_con_7pt'].map(lambda x: 'Liberal' if x <= 3 else 'Conservative' if x >= 5 else 'Moderate')
    else:
        df_valid = df[(df[issue_question] >= 1) & (df['poli_party_self_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].map(lambda x: 'Democratic Party' if x <= 3 else 'Republican Party' if x >= 5 else 'Independent')

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

    # Categorize into general buckets
    def categorize(val):
        txt = answer_choice_map.get(val, f"Response {val}").lower()
        if any(w in txt for w in ['more', 'great deal more', 'little more']):
            return 'More'
        if any(w in txt for w in ['less', 'great deal less', 'little less']):
            return 'Less'
        if any(w in txt for w in ['same', 'about the same', 'right amount']):
            return 'Same'
        if any(w in txt for w in ['neither favor nor oppose', 'neither']):
            return 'Neither'
        if any(w in txt for w in ['favor', 'support', 'agree', 'yes']):
            return 'Favor'
        if any(w in txt for w in ['oppose', 'against', 'disagree', 'no']):
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
        flows.append((grp, gen, cnt, color))
    # Layer 2: General Position to Specific Response (exclude 'Neither')
    for (grp, gen, spec), cnt in df_valid[df_valid['general_position'] != 'Neither']\
                                       .groupby(['group_label', 'general_position', 'specific_response']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') else political_fill_colors).get(grp, '#ccc')
        flows.append((gen, spec, cnt, color))

    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 'Color'])
    
    # Create ordered node lists for proper positioning
    # Define the order for each layer
    group_nodes = list_of_groups  # First layer: group labels
    general_position_nodes = ['Favor', 'Neither', 'Oppose']  # Second layer: centered Neither
    specific_response_nodes = sorted([node for node in set(flows_df['Target']) 
                                    if node not in group_nodes and node not in general_position_nodes])
    
    # Create the complete ordered node list
    all_nodes = group_nodes + general_position_nodes + specific_response_nodes
    
    # Filter to only include nodes that actually exist in the data
    existing_nodes = list(set(flows_df['Source']) | set(flows_df['Target']))
    ordered_nodes = [node for node in all_nodes if node in existing_nodes]

    # Reorder the flows DataFrame to control node positioning
    # Create a mapping for desired node order
    node_order_map = {node: i for i, node in enumerate(ordered_nodes)}
    
    # Sort flows by the desired node order
    flows_df['source_order'] = flows_df['Source'].map(node_order_map)
    flows_df['target_order'] = flows_df['Target'].map(node_order_map)
    flows_df = flows_df.sort_values(['source_order', 'target_order']).drop(['source_order', 'target_order'], axis=1)

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
                node_color=dim('Source').categorize({n: '#ececec' for n in ordered_nodes}),
                node_fill_color=dim('Source').categorize({n: '#ececec' for n in ordered_nodes}),
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
                node_sort=False,  # Set to False and rely on data ordering
                title = title,
                title_format="{label}",  # Use the label as title
                fontsize={'title': '20pt'}  # Set title font size here
            )
        )
        return sankey
    except Exception as e:
        print(f"Error creating Sankey: {e}")
        return None

# End of agree/disagree sankey module
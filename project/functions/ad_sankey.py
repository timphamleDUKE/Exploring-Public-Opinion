import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from functions.dictionaries import (
    find_answer_choices, 
    ideological_fill_colors, 
    political_fill_colors, 
    codebook
)

def check_needs_binary_sankey(issue_question):
    """Check if question needs Binary Sankey based on manual overrides and codebook"""
    
    # Manual overrides - these take precedence over everything else
    manual_binary_allowed = {
        # Questions that should definitely have Binary Flow
        'children_immigrants': True,  # Immigration question with clear opposing sides
        'birthright_citizenship': True,
        'mexico_wall': True,
        'ukraine_russia': True,
        'israel': True,
        'palestine_aid': True,
        'israel_palestine': True,
        'gaza_protests': True,
        'death_penalty': True,
        'voting_id': True,
        'voting_felons': True,
        'journalists': True,
        'climate_inc_temps': True,
        'paid_leave': True,
        'transgender_bathrooms': True,
        'transgender_sports': True,
        'transgender_military': True,
        'lgbt_discrimination': True,
        'lgbt_adoption': True,
        'gay_marriage': True,
        'affirmative_action': True,
        'gun_background_checks': True,
        'gun_ban_assault_rifles': True,
        'vaccines_schools': True,
        'climate_regulate_emissions': True,
        'free_trade': True,
        'dei': True,
        'import_limits': True,  # Missing question
        'us_world_involvement': True,  # Should have binary flow
        'hiring_black': True,  # Should have binary flow
        'gov_involvement': True,  # Should have binary flow
        'gov_regulation': True,  # Should have binary flow
        'income_inequality': True,  # Should have binary flow
        'equal_opportunity': True,  # Should have binary flow
        'gender_roles': True,  # Should have binary flow
        'opioid_epidemic': True,  # Should have binary flow
        'diversity': True,  # Should have binary flow
        'budget_healthcare': True,  # Should have binary flow
        'vaccines': True,  # Should have binary flow
        'sexual_harassment': True,  # Should have binary flow
        'colleges_run': True,  # Should have binary flow
        'immigration_levels': True,  # Should have binary flow
        'immigration_economy': True,  # Should have binary flow
        'immigration_crime': True,  # Should have binary flow
        # Budget questions - all should have binary flow
        'budget_social_security': True,
        'budget_public_schools': True,
        'budget_border_security': True,
        'budget_crime': True,
        'budget_welfare': True,
        'budget_highways': True,
        'budget_aid_poor': True,
        'budget_environment': True,
    }
    
    manual_binary_blocked = {
        # Only block questions that truly shouldn't have Binary Flow
        # (Keep this minimal - most questions should follow codebook)
    }
    
    # Check manual overrides first
    if issue_question in manual_binary_blocked:
        return False
    if issue_question in manual_binary_allowed:
        return True
    
    # Fall back to codebook 
    question_row = codebook[codebook['Renamed'] == issue_question]
    if question_row.empty or 'A/D Sankey' not in question_row.columns:
        return False
    val = question_row['A/D Sankey'].iloc[0]
    
    # Check if codebook says False
    if isinstance(val, bool) and not val:
        return False
    if isinstance(val, str) and val.strip().lower() == 'false':
        return False
    
    # For questions not in manual lists, use codebook value
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() == 'true'
    
    return False


def create_binary_flow_sankey_holoviews(df, issue_question, list_of_groups, 
                                        group_type, title=""):
    """
    Build a 3-layer "binary flow" Sankey using HoloViews.
    Only creates the plot if the codebook indicates this question should 
    have an A/D Sankey.
    """
    if not check_needs_binary_sankey(issue_question):
        return None

    # Map respondents into three groups
    if group_type == "Ideological Groups":
        df_valid = df[(df[issue_question] >= 1) & 
                      (df['lib_con_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['lib_con_7pt'].map(
            lambda x: 'Liberal' if x <= 3 else 
                     'Conservative' if x >= 5 else 'Moderate'
        )
    else:
        df_valid = df[(df[issue_question] >= 1) & 
                      (df['poli_party_self_7pt'] >= 1)].copy()
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].map(
            lambda x: 'Democrats' if x <= 3 else 
                     'Republicans' if x >= 5 else 'Independents'
        )

    if df_valid.empty:
        return None

    # Get mapping of answer choices and ordering
    try:
        answer_choice_map = find_answer_choices(issue_question)
        target_order = [answer_choice_map[i] for i in 
                       sorted(answer_choice_map.keys())]
    except Exception:
        maxv = int(df_valid[issue_question].max())
        answer_choice_map = {i: f"Response {i}" for i in range(1, maxv + 1)}
        target_order = list(answer_choice_map.values())

    # Categorize into general buckets - comprehensive pattern matching
    def categorize(val):
        txt = answer_choice_map.get(val, f"Response {val}").lower()
        
        # Check for "neither" first (most specific)
        if any(w in txt for w in ['neither favor nor oppose', 'neither approve nor disapprove', 'neither']):
            return 'Neither'
        
        # Special handling for immigration questions
        if 'immigrant' in txt:
            if 'sent back' in txt:
                return 'Sent Back'
            elif 'allowed to live' in txt or 'live & work' in txt:
                return 'Gets to Stay'
        
        # Israel/Palestine question - special handling
        if 'side' in txt and ('israeli' in txt or 'palestinian' in txt):
            if 'israeli' in txt:
                return 'Side with Israel'
            elif 'palestinian' in txt:
                return 'Side with Palestine'
            elif 'both equally' in txt:
                return 'Both Equally'
            elif 'neither' in txt:
                return 'Neither Side'
        
        # LGBT adoption question - special handling
        if 'permitted to adopt' in txt or 'adopt' in txt:
            if 'should be permitted' in txt or 'permitted to adopt' in txt:
                return 'Should Adopt'
            elif 'should not be permitted' in txt or 'not be permitted' in txt:
                return 'Should Not Adopt'
        
        # Government involvement questions
        if 'less government' in txt or 'less gov' in txt:
            return 'Less Government'
        elif 'more things that government' in txt or 'more gov should' in txt:
            return 'More Government'
        
        # Hiring/preferential treatment questions
        if 'preferential hiring' in txt:
            if 'for preferential' in txt:
                return 'For Hiring'
            elif 'against preferential' in txt:
                return 'Against Hiring'
        
        # Sexual harassment attention question
        if 'too far' in txt:
            return 'Gone Too Far'
        elif 'about right' in txt:
            return 'About Right'
        elif 'not' in txt and ('far enough' in txt or 'enough' in txt):
            return 'Not Far Enough'
        
        # Benefits vs risks (vaccines)
        if 'benefits' in txt and 'outweigh' in txt:
            return 'Benefits Outweigh'
        elif 'risks' in txt and 'outweigh' in txt:
            return 'Risks Outweigh'
        elif 'no difference' in txt:
            return 'No Difference'
        
        # Good/Bad scales
        if any(w in txt for w in ['extremely good', 'moderately good', 'slightly good']):
            return 'Good'
        elif any(w in txt for w in ['extremely bad', 'moderately bad', 'slightly bad']):
            return 'Bad'
        elif 'neither good nor bad' in txt:
            return 'Neither Good Nor Bad'
        
        # Better/Worse/No difference scales
        if any(w in txt for w in ['much better', 'somewhat better', 'slightly better', 'a lot better', 'a little better']):
            return 'Better'
        elif any(w in txt for w in ['much worse', 'somewhat worse', 'slightly worse', 'a lot worse', 'a little worse']):
            return 'Worse'
        elif 'makes no difference' in txt or 'no difference' in txt:
            return 'No Difference'
        
        # Approve/Disapprove patterns
        if any(w in txt for w in ['approve very strongly', 'approve somewhat strongly', 'approve not very strongly', 'approve a lot', 'approve a moderate', 'approve a little']):
            return 'Approve'
        elif any(w in txt for w in ['disapprove not very strongly', 'disapprove somewhat strongly', 'disapprove strongly', 'disapprove a lot', 'disapprove a moderate', 'disapprove a little']):
            return 'Disapprove'
        elif 'neither approve nor disapprove' in txt:
            return 'Neither'
        
        # Agree/Disagree patterns
        if any(w in txt for w in ['agree strongly', 'strongly agree', 'agree somewhat', 'somewhat agree']):
            return 'Agree'
        elif any(w in txt for w in ['disagree strongly', 'strongly disagree', 'disagree somewhat', 'somewhat disagree']):
            return 'Disagree'
        elif 'neither agree nor disagree' in txt:
            return 'Neither'
        elif 'agree' in txt and 'disagree' not in txt:
            return 'Agree'
        elif 'disagree' in txt:
            return 'Disagree'
        
        # Increase/Decrease patterns
        if any(w in txt for w in ['increase', 'increased', 'more', 'great deal more', 'moderate amount more', 'little more', 'somewhat more']):
            return 'More'
        elif any(w in txt for w in ['decrease', 'decreased', 'less', 'great deal less', 'moderate amount less', 'little less', 'somewhat less']):
            return 'Less'
        elif any(w in txt for w in ['same', 'kept the same', 'left the same', 'about the same', 'right amount', 'currently doing the right amount']):
            return 'Same'
        elif 'no change' in txt:
            return 'Same'
        
        # For/Against patterns
        if any(w in txt for w in ['strongly for', 'not strongly for']):
            return 'For'
        elif any(w in txt for w in ['strongly against', 'not strongly against']):
            return 'Against'
        
        # Favor/Oppose patterns (most general, should be last)
        if any(w in txt for w in ['favor', 'support', 'yes']):
            return 'Favor'
        elif any(w in txt for w in ['oppose', 'against', 'no']):
            return 'Oppose'
        
        return 'Other'

    df_valid['general_position'] = df_valid[issue_question].map(categorize)
    df_valid['specific_response'] = df_valid[issue_question].map(
        answer_choice_map
    )

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
    
    # Layer 1: Group to General Position - ALL positions get flows
    for (grp, gen), cnt in df_valid.groupby(['group_label', 
                                           'general_position']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') 
                else political_fill_colors).get(grp, '#ccc')
        flows.append((grp, gen, cnt, color, grp))  # Add group info for sorting
    
    # Layer 2: General Position to Specific Response 
    # CRITICAL FIX: Only non-Neither and non-Same positions flow to specific responses
    terminal_positions = ['Neither', 'Same']
    non_terminal = df_valid[~df_valid['general_position'].isin(terminal_positions)]
    
    for (grp, gen, spec), cnt in non_terminal.groupby(['group_label', 
                                                      'general_position', 
                                                      'specific_response']).size().items():
        color = (ideological_fill_colors if group_type.startswith('Ideological') 
                else political_fill_colors).get(grp, '#ccc')
        flows.append((gen, spec, cnt, color, grp))  # Add group info for sorting
    
    # SIMPLE FIX: Add minimal dummy flows from terminal positions to force them to middle
    for pos in terminal_positions:
        if pos in df_valid['general_position'].values:
            flows.append((pos, f"{pos}__END", 0.0001, '#ffffff', 'dummy'))

    flows_df = pd.DataFrame(flows, columns=['Source', 'Target', 'Value', 
                                           'Color', 'Group'])
    
    # Filter flows to exclude unwanted target nodes (additional cleanup)
    excluded_responses = ['neither favor nor oppose', 'about the same amount']
    flows_df = flows_df[~flows_df['Target'].str.lower().isin(
        [ex.lower() for ex in excluded_responses]
    )]
    
    # Create ordered node lists for proper positioning
    # Define the order for each layer
    group_nodes = list_of_groups  # First layer: group labels
    
    # Get all possible general positions that could exist
    all_possible_positions = [
        'Favor', 'Neither', 'Oppose', 'Agree', 'Disagree', 'More', 'Same', 'Less',
        'Sent Back', 'Gets to Stay',  # Immigration
        'Side with Israel', 'Side with Palestine', 'Both Equally', 'Neither Side',  # Israel/Palestine
        'Should Adopt', 'Should Not Adopt',  # LGBT adoption
        'Less Government', 'More Government',  # Government involvement
        'For Hiring', 'Against Hiring',  # Preferential hiring
        'Gone Too Far', 'About Right', 'Not Far Enough',  # Sexual harassment
        'Benefits Outweigh', 'Risks Outweigh', 'No Difference',  # Vaccines
        'Good', 'Bad', 'Neither Good Nor Bad',  # Good/Bad scales
        'Better', 'Worse',  # Better/Worse scales
        'Approve', 'Disapprove',  # Approve/Disapprove
        'For', 'Against'  # For/Against
    ]
    
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
    specific_response_nodes = [
        resp for resp in processed_target_order
        if resp in set(flows_df['Target']) 
        and resp not in group_nodes 
        and resp not in general_position_nodes
        and resp.lower() not in [ex.lower() for ex in excluded_responses]
    ]
    
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
    flows_df = flows_df.sort_values(['target_order', 'group_priority', 
                                    'source_order']).drop(['source_order', 
                                                          'target_order', 
                                                          'group_priority', 
                                                          'Group'], axis=1)

    unique_nodes = list(set(flows_df['Source']).union(set(flows_df['Target'])))

    # Hide the dummy END node labels but keep all nodes gray
    # Also wrap long text labels
    def wrap_text(text, max_length=25):
        """Wrap text at word boundaries"""
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
    
    node_labels = {}
    for node in unique_nodes:
        if '__END' in node:
            node_labels[node] = ''  # Empty string to hide __END labels
        else:
            node_labels[node] = wrap_text(node)

    # Try to build and style the Sankey
    try:
        sankey = hv.Sankey(flows_df, kdims=['Source', 'Target'], 
                          vdims=['Value', 'Color'])
        sankey = sankey.opts(
            opts.Sankey(
                width=600,
                height=200,
                edge_color='Color',
                edge_alpha=0.6,
                edge_line_width=1,
                node_color=dim('Source').categorize({
                    node: '#ececec' for node in unique_nodes 
                    if node != 'Same__END'
                }),
                node_fill_color=dim('Source').categorize({
                    node: '#ececec' for node in unique_nodes 
                    if node != 'Same__END'
                }),
                node_fill_alpha=1.0,
                node_line_color='black',
                node_line_width=0.25,
                label_text_font_size='10pt',
                label_position='right',
                node_padding=80,
                tools=['hover'],
                active_tools=[],
                bgcolor='white',
                show_values=False,
                node_sort=False,
                title=title,
                title_format="{label}",
                fontsize={'title': '20pt'},
                labels=dim('index').categorize(node_labels)
            )
        )

        return sankey
    except Exception as e:
        print(f"Error creating Sankey: {e}")
        return None
import pandas as pd
import holoviews as hv
from functions.dictionaries import find_answer_choices, ideological_fill_colors, political_fill_colors

def create_agree_disagree_sankey_holoviews(df, issue_question, list_of_groups, group_type):
    """
    Build a 3-layer “agree/disagree” flow Sankey using HoloViews.
    """
    # filter & map to 3-pt group
    if group_type == "Ideological Groups":
        df_valid = df[(df[issue_question] >= 1) & (df['lib_con_7pt'] >= 1)].copy()
        def map3(x):
            if x in [1,2,3]: return 'Liberal'
            if x in [5,6,7]: return 'Conservative'
            if x == 4:       return 'Moderate'
        df_valid['group_label'] = df_valid['lib_con_7pt'].map(map3)
    else:
        df_valid = df[(df[issue_question] >= 1) & (df['poli_party_self_7pt'] >= 1)].copy()
        def map3(x):
            if x in [1,2,3]: return 'Democratic Party'
            if x in [5,6,7]: return 'Republican Party'
            if x == 4:       return 'Independent'
        df_valid['group_label'] = df_valid['poli_party_self_7pt'].map(map3)

    if df_valid.empty:
        return None

    # get response labels
    try:
        resp_lbls = find_answer_choices(issue_question)
    except:
        maxv = int(df_valid[issue_question].max())
        resp_lbls = {i: f"Response {i}" for i in range(1, maxv+1)}

    def categorize(val):
        text = resp_lbls.get(val, f"Response {val}").lower()
        if any(w in text for w in ['favor','support','agree','yes']):
            return "Favor"
        if any(w in text for w in ['oppose','against','disagree','no']):
            return "Oppose"
        return "Neither"

    df_valid['general_position'] = df_valid[issue_question].map(categorize)
    df_valid['specific_response'] = df_valid[issue_question].map(resp_lbls)
    df_valid = df_valid[df_valid['group_label'].isin(list_of_groups)]
    if df_valid.empty:
        return None

    # build flows
    flows = []
    # layer 1 → 2
    g2g = df_valid.groupby(['group_label','general_position']).size().reset_index(name='count')
    for _,r in g2g.iterrows():
        src = r['group_label']; tgt = r['general_position']; cnt = r['count']
        # pick color by src
        if group_type=="Ideological Groups":
            color = ideological_fill_colors.get(src, '#ececec')
        else:
            color = political_fill_colors.get(src, '#ececec')
        flows.append((src, tgt, cnt, color))

    # layer 2 → 3
    g2s = df_valid.groupby(['group_label','general_position','specific_response'])\
                  .size().reset_index(name='count')
    for _,r in g2s.iterrows():
        src = r['general_position']; tgt = r['specific_response']; cnt = r['count']
        # use same color as their original group
        grp = r['group_label']
        if group_type=="Ideological Groups":
            color = ideological_fill_colors.get(grp, '#ececec')
        else:
            color = political_fill_colors.get(grp, '#ececec')
        flows.append((src, tgt, cnt, color))

    flows_df = pd.DataFrame(flows, columns=['Source','Target','Value','Color'])
    nodes = list(set(flows_df['Source']) | set(flows_df['Target']))

    sankey = hv.Sankey(flows_df, kdims=['Source','Target'], vdims=['Value','Color'])\
              .opts(
                  width=900, height=600,
                  edge_color='Color', edge_alpha=1,
                  node_color='Source', cmap=['#ececec'],
                  label_text_font_size='11pt',
                  tools=['hover'], show_values=False
              )
    return sankey

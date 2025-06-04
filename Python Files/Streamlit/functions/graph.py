import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from functions.dictionaries import group_by_dic_reverse
from functions.weights import ces_calc_weights, anes_calc_weights_complex

def display_chart(df, question, groups, study):
    for group in groups:
        st.plotly_chart(bar_graph_go(df, question, group, study), use_container_width=True)

def bar_graph_go(df, question, group, study):
    
    if study == "CES":
        grouped = ces_calc_weights(df, question, group)
    elif study == "ANES":
        grouped = anes_calc_weights_complex(df, question, group)
    
    # Debug output
    st.write("Data being plotted:")
    st.write(grouped)
    
    # Clean the data
    grouped = grouped.dropna(subset=['proportion'])
    grouped = grouped[grouped['proportion'] >= 0]
    grouped['response'] = grouped['response'].astype(str)
    grouped['group'] = grouped['group'].astype(str)
    grouped = grouped.sort_values(['group', 'response']).reset_index(drop=True)
    
    # Create figure using graph_objects for more control
    fig = go.Figure()
    
    # Get unique responses and groups
    unique_responses = sorted(grouped['response'].unique())
    unique_groups = sorted(grouped['group'].unique())
    
    # Define colors for each response
    colors = px.colors.qualitative.Set1[:len(unique_responses)]
    
    # Add a trace for each response category
    for i, response in enumerate(unique_responses):
        response_data = grouped[grouped['response'] == response]
        
        # Create arrays for x and y values
        x_values = []
        y_values = []
        
        for group_val in unique_groups:
            group_subset = response_data[response_data['group'] == group_val]
            if len(group_subset) > 0:
                x_values.append(group_subset['proportion'].iloc[0])
                y_values.append(group_val)
            else:
                x_values.append(0)
                y_values.append(group_val)
        
        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            name=f'Response {response}',
            orientation='h',
            marker_color=colors[i % len(colors)],
            text=[f'{val:.1%}' if val > 0.05 else '' for val in x_values],  # Show percentage if > 5%
            textposition='inside'
        ))
    
    # Update layout with all settings at once
    fig.update_layout(
        title=f"Proportional Distribution of {question} by {group_by_dic_reverse.get(group, group)}",
        title_font_size=16,
        title_font_color='white',
        
        # Force stacked bars
        barmode='stack',
        
        # Axes
        xaxis=dict(
            title='Proportion',
            tickformat='.0%',
            range=[0, 1],
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)',
            color='white'
        ),
        yaxis=dict(
            title=group_by_dic_reverse.get(group, group),
            autorange='reversed',  # Reverse to match CES chart
            gridcolor='rgba(128,128,128,0.2)',
            zerolinecolor='rgba(128,128,128,0.2)',
            color='white'
        ),
        
        # Styling
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        
        # Legend
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02,
            font_color='white'
        ),
        
        # Margins
        margin=dict(l=50, r=150, t=80, b=50)
    )
    
    # Debug output
    st.write(f"Final barmode: {fig.layout.barmode}")
    
    return fig
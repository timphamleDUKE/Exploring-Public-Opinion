import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from functions.dictionaries import *
from functions.weights import get_anes_weighted_density_data  # Import our weights module

def densityGraph(df, question, groups, use_weights=True, weight_method='bootstrap'):
    """
    Create density graph with optional ANES survey weights
    
    Parameters:
    -----------
    df : pandas.DataFrame
        ANES dataframe
    question : str
        Question/variable name for thermometer ratings
    groups : list
        List of party groups to include
    use_weights : bool
        Whether to apply survey weights (default: True)
    weight_method : str
        Method for applying weights ('replication', 'bootstrap', or 'simple')
    """

    # Make party labels
    df["party"] = df["poli_party_reg"].map({
        1: "Democratic Party",
        2: "Republican Party",
        4: "None/Independent Party"
    })

    # Filter the valid data
    df = df[
        (df["party"].isin(groups)) &
        (df[question] >= 0) &
        (df[question] <= 100)
    ]

    fig = go.Figure()

    if use_weights:
        # Use weighted density estimation
        try:
            plotting_data = get_anes_weighted_density_data(
                df, question, groups, group_var='party', weight_method=weight_method, random_state = 12345
            )
            
            # Add weighted KDE traces for each party
            for party in groups:
                if party in plotting_data:
                    x_range = plotting_data[party]['x_range']
                    y_values = plotting_data[party]['y_values']
                    
                    # Add filled trace
                    fig.add_trace(go.Scatter(
                        x=x_range,
                        y=y_values,
                        mode="lines",
                        name=f"{party}",
                        line=dict(color=colors[party], width=2),
                        fill="tozeroy",
                        fillcolor=fill_colors.get(party, 'rgba(128, 128, 128, 0.3)')
                    ))
            
            title_suffix = f"(Survey-Weighted using {weight_method.title()} Method)"
            
        except Exception as e:
            st.warning(f"Error applying survey weights: {e}. Falling back to unweighted analysis.")
            use_weights = False
    
    if not use_weights:
        # Original unweighted approach
        for party in groups:
            values = df[df["party"] == party][question].dropna().values
            
            if len(values) > 0:  # Check if we have data
                # Compute KDE
                kde = gaussian_kde(values)
                x_range = np.linspace(0, 100, 500)
                y_values = kde(x_range)

                # Add filled trace
                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=y_values,
                    mode="lines",
                    name=party,
                    line=dict(color=colors[party], width=2),
                    fill="tozeroy",
                    fillcolor=fill_colors.get(party, 'rgba(128, 128, 128, 0.3)')
                ))
        
        title_suffix = " (Unweighted)"

    list_groups_joined = ", ".join(groups)

    # Layout settings
    fig.update_layout(
        # title=f"Density Plot of {question} Thermometer Ratings<br>{title_suffix}",
        title = description_map[question],
        xaxis_title="Thermometer Rating (0–100)",
        yaxis_title="Density",
        xaxis=dict(tickmode="linear", tick0=0, dtick=20),
        hovermode="x unified",
        template="simple_white"
    )

    return fig

# Additional function for comparing weighted vs unweighted
def densityGraphComparison(df, question, groups, weight_method='replication'):
    """
    Create side-by-side comparison of weighted vs unweighted density plots
    """
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Unweighted Density")
        fig_unweighted = densityGraph(df, question, groups, use_weights=False)
        st.plotly_chart(fig_unweighted, use_container_width=True)
    
    with col2:
        st.subheader("Survey-Weighted Density")
        fig_weighted = densityGraph(df, question, groups, use_weights=True, weight_method=weight_method)
        st.plotly_chart(fig_weighted, use_container_width=True)
    
    return fig_unweighted, fig_weighted
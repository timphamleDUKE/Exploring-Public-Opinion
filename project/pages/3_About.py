import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as patches

def create_radial_language_plot(languages_data, title="LOC of Popular Programming Languages in CRAN Packages"):
    """
    Create a radial plot for Streamlit display
    
    Parameters:
    languages_data: dict with language names as keys and LOC counts as values
    title: string for plot title
    
    Returns:
    matplotlib figure object for st.pyplot()
    """
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # Define colors for each language (similar to the original)
    colors = {
        'R': '#4A90A4',      # Teal/Blue
        'C': '#F4A261',      # Orange
        'C++': '#E76F51',    # Red/Coral
        'Java': '#9D4EDD',   # Purple
        'JavaScript': '#E63946',  # Pink/Red
        'Python': '#2A9D8F', # Green
        'Ruby': '#264653',   # Dark teal
        'SQL': '#2A9D8F',    # Green
        'Assembly': '#F4A261', # Orange
        'Go': '#00ADD8',     # Go blue
        'Rust': '#000000',   # Black
        'Swift': '#FA7343',  # Orange
        'Kotlin': '#7F52FF', # Purple
        'TypeScript': '#3178C6', # Blue
        'PHP': '#777BB4'     # Purple
    }
    
    # Fallback colors for languages not in the predefined list
    default_colors = plt.cm.Set3(np.linspace(0, 1, 20))
    
    # Calculate proportions and angles
    total_loc = sum(languages_data.values())
    proportions = {lang: loc/total_loc for lang, loc in languages_data.items()}
    
    # Create the radial lines extending from center
    num_packages = 300  # Total packages
    angles = np.linspace(0, 2*np.pi, num_packages, endpoint=False)
    
    # Draw radial lines
    for i, angle in enumerate(angles):
        # Assign each line to a language based on proportions
        cumulative = 0
        line_lang = list(languages_data.keys())[0]  # default to first language
        for lang, prop in proportions.items():
            cumulative += prop
            if i/len(angles) <= cumulative:
                line_lang = lang
                break
        
        # Get color for this language
        if line_lang in colors:
            line_color = colors[line_lang]
        else:
            # Use hash of language name to get consistent color
            color_idx = hash(line_lang) % len(default_colors)
            line_color = default_colors[color_idx]
        
        # Draw line from center to outer edge
        r_start = 0.1
        r_end = 1.0
        ax.plot([angle, angle], [r_start, r_end], 
                color=line_color, alpha=0.7, linewidth=0.8)
    
    # Get top languages for central circles
    sorted_languages = sorted(languages_data.items(), key=lambda x: x[1], reverse=True)
    top_languages = sorted_languages[:min(5, len(sorted_languages))]
    
    # Predefined positions for circles (you can adjust these)
    circle_positions = [
        (0, 0),           # Center for largest
        (np.pi/4, 0.4),   # Top right
        (3*np.pi/4, 0.4), # Top left  
        (5*np.pi/4, 0.4), # Bottom left
        (7*np.pi/4, 0.4)  # Bottom right
    ]
    
    # Add circles for top languages
    for i, (lang, loc) in enumerate(top_languages):
        if i < len(circle_positions):
            # Calculate circle size based on LOC
            max_loc = top_languages[0][1]
            circle_size = np.sqrt(loc / max_loc) * 0.2 + 0.05
            
            # Get position
            theta, r = circle_positions[i]
            
            # Get color
            if lang in colors:
                circle_color = colors[lang]
            else:
                color_idx = hash(lang) % len(default_colors)
                circle_color = default_colors[color_idx]
            
            # Create circle patch
            circle = Circle((0, 0), circle_size, color=circle_color, alpha=0.8)
            
            # Transform and add circle
            t = ax.transData.transform_point((theta, r))
            circle.center = ax.transData.inverted().transform(t)
            ax.add_patch(circle)
            
            # Add label with better text color logic
            text_color = 'white' if lang in ['R', 'Java', 'Ruby'] else 'black'
            ax.text(theta, r, f'{lang}\n{loc:,}', 
                    ha='center', va='center', 
                    fontsize=10, fontweight='bold',
                    color=text_color)
    
    # Add smaller language labels around the perimeter
    remaining_langs = [item for item in sorted_languages if item not in top_languages]
    for i, (lang, loc) in enumerate(remaining_langs[:10]):  # Limit to avoid overcrowding
        angle = 2 * np.pi * i / len(remaining_langs[:10])
        
        # Adjust rotation for readability
        rotation = np.degrees(angle)
        if angle > np.pi/2 and angle < 3*np.pi/2:
            rotation += 180
            
        ax.text(angle, 1.15, f'{lang}\n{loc:,}', 
                ha='center', va='center', fontsize=8,
                rotation=rotation)
    
    # Customize the plot
    ax.set_ylim(0, 1.3)
    ax.set_title(title + '\nRadial visualization of lines of code by programming language',
                 pad=30, fontsize=14, fontweight='bold')
    
    # Remove radial labels and grid
    ax.set_rticks([])
    ax.set_thetagrids([])
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    
    # Make background transparent for better Streamlit integration
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    plt.tight_layout()
    return fig

# Streamlit app example
def main():
    st.title("Programming Languages Visualization")
    st.write("Interactive radial plot showing lines of code distribution")
    
    # Sample data - replace with your actual data
    default_data = {
        'R': 4138399,
        'C': 3118724,
        'C++': 2496350,
        'JavaScript': 624326,
        'Java': 295194,
        'Assembly': 148202,
        'Python': 115484,
        'SQL': 2411,
        'Ruby': 195,
        'Go': 50000,
        'Rust': 25000
    }
    
    # Allow users to modify data in sidebar
    st.sidebar.header("Customize Data")
    
    # Create input fields for each language
    languages_data = {}
    for lang, default_value in default_data.items():
        languages_data[lang] = st.sidebar.number_input(
            f"{lang} (LOC)", 
            min_value=0, 
            value=default_value,
            step=1000
        )
    
    # Option to add new language
    new_lang = st.sidebar.text_input("Add new language:")
    if new_lang:
        new_loc = st.sidebar.number_input(f"{new_lang} (LOC)", min_value=0, value=10000, step=1000)
        languages_data[new_lang] = new_loc
    
    # Filter out zero values
    languages_data = {k: v for k, v in languages_data.items() if v > 0}
    
    # Create and display the plot
    if languages_data:
        fig = create_radial_language_plot(languages_data)
        st.pyplot(fig)
        
        # Display summary statistics
        st.subheader("Summary Statistics")
        total_loc = sum(languages_data.values())
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Lines of Code", f"{total_loc:,}")
            st.metric("Number of Languages", len(languages_data))
        
        with col2:
            top_lang = max(languages_data.items(), key=lambda x: x[1])
            st.metric("Top Language", f"{top_lang[0]} ({top_lang[1]:,} LOC)")
            avg_loc = total_loc / len(languages_data)
            st.metric("Average LOC per Language", f"{avg_loc:,.0f}")
        
        # Show data table
        st.subheader("Data Table")
        sorted_data = sorted(languages_data.items(), key=lambda x: x[1], reverse=True)
        
        for i, (lang, loc) in enumerate(sorted_data, 1):
            percentage = (loc / total_loc) * 100
            st.write(f"{i}. **{lang}**: {loc:,} LOC ({percentage:.1f}%)")
    
    else:
        st.error("Please add at least one language with LOC > 0")

# Simple function for direct use
def display_radial_plot(languages_dict):
    """
    Simple function to display the radial plot in Streamlit
    
    Usage:
    display_radial_plot({'Python': 100000, 'R': 200000, 'C++': 150000})
    """
    fig = create_radial_language_plot(languages_dict)
    st.pyplot(fig)
    return fig

if __name__ == "__main__":
    main()

# Example usage in a Streamlit script:

import streamlit as st

# Your data
languages = {
    'R': 4138399,
    'C': 3118724,
    'C++': 2496350,
    'Python': 115484,
    'JavaScript': 624326
}

# Display the plot
st.title("My CRAN Package Analysis")
st.write("Here's the radial visualization of programming languages:")

fig = create_radial_language_plot(languages)
st.pyplot(fig)

# Or use the simple function:
# display_radial_plot(languages)

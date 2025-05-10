# Import required libraries
import streamlit as st
import pandas as pd
import os

# Function to load processed EV data
def load_data():
    # Check if cache file exists first
    if not os.path.exists('cache/processed_ev_data.parquet'):
        st.error("Processed data not found. Please run data processing first.")
        st.stop()  # Halt app execution if data missing
    
    # Return loaded parquet file
    return pd.read_parquet('cache/processed_ev_data.parquet')

# Main application function
def main():
    # Configure page settings
    st.set_page_config(
        page_title="EV Analysis Dashboard", 
        layout="wide",
        page_icon="🚗"
    )
    
    # Set title and description
    st.title("📊 Electric Vehicle Population Analysis")
    st.markdown("Explore electric vehicle registration trends across different states.")
    
    try:
        # Load the EV data
        df = load_data()
        
        # ===== SIDEBAR CONTROLS =====
        st.sidebar.header("Data Filters")
        
        # State selection dropdown
        selected_state = st.sidebar.selectbox(
            "Select State",
            options=sorted(df['State'].unique()),
            index=0  # Default to first state
        )
        
        # Year range slider with dynamic defaults
        min_year = int(df['Model Year'].min())
        max_year = int(df['Model Year'].max())
        year_range = st.sidebar.slider(
            "Model Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(max(min_year, 2015), min(max_year, 2023)),  # Smart defaults
            step=1
        )
        
        # Show record count in sidebar
        st.sidebar.metric("Vehicles Shown", len(filtered_df))
        
        # ===== MAIN DASHBOARD =====
        # Create two columns for layout
        col1, col2 = st.columns(2)
        
        # ---- COLUMN 1: MAP VISUALIZATION ----
        with col1:
            st.subheader("Geospatial Distribution")
            
            # Prepare map data with required column names
            map_df = filtered_df[['Latitude', 'Longitude']] \
                .dropna() \
                .rename(columns={
                    'Latitude': 'latitude', 
                    'Longitude': 'longitude'
                })
            
            # Show map if data exists, else show warning
            if not map_df.empty:
                st.map(map_df, zoom=6, use_container_width=True)
            else:
                st.warning("No location data for selected filters")
        
        # ---- COLUMN 2: MANUFACTURER CHART ----
        with col2:
            st.subheader("Top 10 Manufacturers")
            if not filtered_df.empty:
                # Get top 10 makes by count
                top_makes = filtered_df['Make'].value_counts().nlargest(10)
                st.bar_chart(top_makes)
            else:
                st.warning("No manufacturer data available")
        
        # ---- TIME SERIES CHART ----
        st.subheader("Historical Adoption Trends")
        if not filtered_df.empty:
            # Group by year and count vehicles
            yearly_data = filtered_df.groupby('Model Year') \
                .size() \
                .reset_index(name='Count')
            st.line_chart(yearly_data.set_index('Model Year'))
        else:
            st.warning("No historical data available")
            
    except Exception as e:
        # Show any errors that occur
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# Run the app when executed directly
if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import os
import altair as alt  # For better chart control

def load_data():
    # Load processed EV data from cache
    if not os.path.exists('cache/processed_ev_data.parquet'):
        st.error("Error: Processed data not found. Please run data processing first.")
        st.stop()
    return pd.read_parquet('cache/processed_ev_data.parquet')

def main():
    # Configure page settings
    st.set_page_config(page_title="EV Analysis", layout="wide")
    st.title("📊 Electric Vehicle Population Analysis")
    
    try:
        # Load data with error handling
        df = load_data()
        
        # ===== SIDEBAR FILTERS =====
        st.sidebar.header("Filters")
        
        # State selection with all states option
        all_states = ['All States'] + sorted(df['State'].unique().tolist())
        selected_state = st.sidebar.selectbox("Select State", all_states)
        
        # Year range slider that adapts to data availability
        valid_years = df['Model Year'].dropna().unique()
        if len(valid_years) > 0:
            min_year, max_year = int(min(valid_years)), int(max(valid_years))
            year_range = st.sidebar.slider(
                "Model Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(max(min_year, 2015), min(max_year, 2023))
            )
        else:
            st.warning("No valid model years found in data")
            year_range = (2015, 2023)
        
        # Apply filters
        if selected_state == 'All States':
            filtered_df = df[df['Model Year'].between(*year_range)]
        else:
            filtered_df = df[
                (df['State'] == selected_state) & 
                (df['Model Year'].between(*year_range))
            ]
        
        # Show record count
        st.sidebar.metric("Vehicles Matching Filters", len(filtered_df))
        
        # ===== MAIN DASHBOARD =====
        col1, col2 = st.columns(2)
        
        # Map Visualization (Column 1)
        with col1:
            st.subheader("Geospatial Distribution")
            
            # Check if we have location data
            has_coords = filtered_df[['Latitude', 'Longitude']].notnull().all(axis=1)
            
            if has_coords.any():
                map_df = filtered_df[has_coords][['Latitude', 'Longitude']]\
                    .rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
                
                # Dynamic zoom based on number of points
                zoom = 6 if len(map_df) > 100 else 8 if len(map_df) > 10 else 10
                st.map(map_df, zoom=zoom, use_container_width=True)
                
                if len(map_df) < len(filtered_df):
                    st.info(f"Showing {len(map_df)} of {len(filtered_df)} records with valid coordinates")
            else:
                st.warning("No location data available for selected filters")
                st.info("Try adjusting filters or check data processing steps")
        
        # Manufacturer Distribution (Column 2)
        with col2:
            st.subheader("Top Manufacturers")
            if not filtered_df.empty:
                make_counts = filtered_df['Make'].value_counts()
                top_makes = make_counts.nlargest(10)
                
                if not top_makes.empty:
                    st.bar_chart(top_makes)
                    st.caption(f"Total manufacturers: {len(make_counts)}")
                else:
                    st.warning("No manufacturer data available")
            else:
                st.warning("No vehicles match selected filters")
        
        # Time Series Analysis (Full Width)
        st.subheader("Historical Adoption Trends")
        if not filtered_df.empty:
            # Group by year and count vehicles
            yearly_data = filtered_df.groupby('Model Year').size().reset_index(name='Count')
            
            # Convert Model Year to string to prevent comma formatting
            yearly_data['Model Year'] = yearly_data['Model Year'].astype(int).astype(str)
            
            # Create Altair chart for better formatting control
            chart = alt.Chart(yearly_data).mark_line(point=True).encode(
                x=alt.X('Model Year:O', title='Model Year', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Count:Q', title='Number of Vehicles'),
                tooltip=['Model Year', 'Count']
            ).properties(
                height=400,
                width=800
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No data available for trend analysis")

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()
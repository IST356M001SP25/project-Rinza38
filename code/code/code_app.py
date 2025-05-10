import streamlit as st
import pandas as pd

def load_data():
    return pd.read_parquet('cache/processed_ev_data.parquet')

def main():
    st.set_page_config(page_title="EV Analysis", layout="wide")
    st.title("📊 Electric Vehicle Population Analysis")
    
    # Load data with caching
    df = load_data()
    
    # Sidebar controls
    st.sidebar.header("Filters")
    selected_state = st.sidebar.selectbox("Select State", df['State'].unique())
    year_range = st.sidebar.slider("Model Year Range", 
                                   int(df['Model Year'].min()),
                                   int(df['Model Year'].max()),
                                   (2015, 2023))
    
    # Filter data
    filtered_df = df[
        (df['State'] == selected_state) &
        (df['Model Year'].between(*year_range))
    ]
    
    # Rename columns for Streamlit map compatibility
    map_df = filtered_df[['Latitude', 'Longitude']].dropna().rename(
        columns={'Latitude': 'latitude', 'Longitude': 'longitude'}
    )
    
    # Main dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geospatial Distribution")
        st.map(map_df, zoom=6, use_container_width=True)
    
    with col2:
        st.subheader("Manufacturer Distribution")
        top_makes = filtered_df['Make'].value_counts().nlargest(10)
        st.bar_chart(top_makes)

    # Time series analysis
    st.subheader("Historical Adoption Trends")
    yearly_data = filtered_df.groupby('Model Year').size().reset_index(name='Count')
    st.line_chart(yearly_data.set_index('Model Year'))

if __name__ == "__main__":
    main()

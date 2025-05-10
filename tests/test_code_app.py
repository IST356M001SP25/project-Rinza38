import pytest
import pandas as pd
from unittest.mock import patch
from code.code_app import load_data

@pytest.fixture
def sample_processed_data():
    # Mock processed data for testing
    return pd.DataFrame({
        'State': ['WA', 'WA', 'CA', 'WA'],
        'Model Year': [2015, 2016, 2017, 2023],
        'Make': ['TESLA', 'NISSAN', 'CHEVROLET', 'TESLA'],
        'Latitude': [47.1, 47.2, 34.1, 47.3],
        'Longitude': [-122.1, -122.2, -118.1, -122.3]
    })

def test_load_data(sample_processed_data):
    # Test that load_data() reads from correct parquet file
    with patch('code.code_app.pd.read_parquet') as mock_read:
        mock_read.return_value = sample_processed_data
        df = load_data()
        
        # Verify parquet file was read
        mock_read.assert_called_once_with('cache/processed_ev_data.parquet')
        
        # Verify return type and content
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert set(df['State'].unique()) == {'WA', 'CA'}

def test_filtering_logic(sample_processed_data):
    # Test the state/year filtering logic used in the app
    filtered = sample_processed_data[
        (sample_processed_data['State'] == 'WA') &
        (sample_processed_data['Model Year'].between(2015, 2020))
    ]
    
    # Verify filtering results
    assert len(filtered) == 2
    assert all(filtered['State'] == 'WA')
    assert all(filtered['Model Year'].between(2015, 2020))
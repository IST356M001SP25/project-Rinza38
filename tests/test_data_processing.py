import pytest
import pandas as pd
from code.data_processing import EVDataProcessor

def test_processor_initialization(processor):
    assert isinstance(processor, EVDataProcessor)
    assert processor.df is None

def test_load_data(processor, sample_data):
    df = processor.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == len(sample_data)
    assert 'Vehicle Location' in df.columns

def test_parse_geopoint(processor):
    test_cases = [
        ("POINT (-122.123 47.456)", (47.456, -122.123)),
        ("invalid", (None, None)),
        ("POINT (invalid)", (None, None)),
        (None, (None, None)),
        ("", (None, None))
    ]
    
    for input_val, expected in test_cases:
        result = processor._parse_geopoint(input_val)
        assert result == expected

def test_transform_data(processed_data):
    df = processed_data
    required_columns = {'Make', 'Model', 'Model Year', 'Electric Range', 'Latitude', 'Longitude'}
    assert required_columns.issubset(set(df.columns))
    
    # Test numeric conversion
    assert pd.api.types.is_numeric_dtype(df['Model Year'])
    assert pd.api.types.is_numeric_dtype(df['Electric Range'])
    
    # Test text cleaning
    sample_make = df['Make'].iloc[0]
    assert sample_make == sample_make.upper()
    
    sample_model = df['Model'].iloc[0]
    assert sample_model == sample_model.title()
    
    # Test column drops
    dropped_columns = ['VIN (1-10)', 'DOL Vehicle ID', 'Vehicle Location']
    for col in dropped_columns:
        assert col not in df.columns

def test_save_processed_data(processor, processed_data, tmp_path):
    test_output = tmp_path / "test_output.parquet"
    processor.save_processed_data(str(test_output))
    assert test_output.exists()
    
    # Verify can load the saved data
    loaded = pd.read_parquet(test_output)
    assert not loaded.empty
    assert len(loaded) == len(processed_data)
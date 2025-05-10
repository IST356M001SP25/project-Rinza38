import pytest
import pandas as pd
from code.data_processing import EVDataProcessor

def test_processor_initialization(processor):
    # Test EVDataProcessor initialization
    assert isinstance(processor, EVDataProcessor)
    assert processor.df is None  # Should start with no data loaded

def test_load_data(processor, sample_data):
    # Test data loading functionality
    df = processor.load_data()
    
    # Verify DataFrame properties
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == len(sample_data)
    assert 'Vehicle Location' in df.columns  # Verify key column exists

def test_parse_geopoint(processor):
    # Test geographic point parsing
    test_cases = [
        ("POINT (-122.123 47.456)", (47.456, -122.123)),  # Valid point
        ("invalid", (None, None)),  # Invalid format
        ("POINT (invalid)", (None, None)),  # Invalid coordinates
        (None, (None, None)),  # None input
        ("", (None, None))  # Empty string
    ]
    
    # Test all cases
    for input_val, expected in test_cases:
        result = processor._parse_geopoint(input_val)
        assert result == expected

def test_transform_data(processed_data):
    # Test data transformation pipeline
    df = processed_data
    
    # Verify required columns exist
    required_columns = {'Make', 'Model', 'Model Year', 'Electric Range', 'Latitude', 'Longitude'}
    assert required_columns.issubset(set(df.columns))
    
    # Test numeric conversions
    assert pd.api.types.is_numeric_dtype(df['Model Year'])
    assert pd.api.types.is_numeric_dtype(df['Electric Range'])
    
    # Test text cleaning
    sample_make = df['Make'].iloc[0]
    assert sample_make == sample_make.upper()  # Makes should be uppercase
    
    sample_model = df['Model'].iloc[0] 
    assert sample_model == sample_model.title()  # Models should be title case
    
    # Verify columns were dropped
    dropped_columns = ['VIN (1-10)', 'DOL Vehicle ID', 'Vehicle Location']
    for col in dropped_columns:
        assert col not in df.columns

def test_save_processed_data(processor, processed_data, tmp_path):
    # Test saving processed data
    test_output = tmp_path / "test_output.parquet"
    processor.save_processed_data(str(test_output))
    
    # Verify file was created
    assert test_output.exists()
    
    # Verify saved data can be loaded and matches original
    loaded = pd.read_parquet(test_output)
    assert not loaded.empty
    assert len(loaded) == len(processed_data)
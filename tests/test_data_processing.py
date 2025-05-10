import pytest
import pandas as pd
from code.data_processing import EVDataProcessor  # Adjust import path as needed

# Test Fixtures
@pytest.fixture
def processor():
    # Fixture providing an initialized EVDataProcessor instance
    return EVDataProcessor()

@pytest.fixture
def sample_data():
    # Fixture providing sample raw data that matches the expected input format
    return pd.DataFrame([
        {
            "VIN (1-10)": "1234567890",
            "Make": "TESLA",
            "Model": "model 3",
            "Model Year": "2020",
            "Electric Range": "250",
            "Vehicle Location": "POINT (-122.123 47.456)"
        },
        {
            "VIN (1-10)": "ABCDEFGHIJ",
            "Make": "chevrolet",
            "Model": "BOLT EV",
            "Model Year": "2019",
            "Electric Range": "238",
            "Vehicle Location": "POINT (-118.243 34.052)"
        },
        {
            "VIN (1-10)": "0987654321",
            "Make": "NISSAN",
            "Model": "leaf",
            "Model Year": "2021",
            "Electric Range": "149",
            "Vehicle Location": "invalid_location"
        }
    ])

@pytest.fixture
def processed_data(processor, sample_data):
    # Fixture providing processed data by running transform_data() on sample data
    processor.df = sample_data
    return processor.transform_data()

# Test Cases
def test_processor_initialization(processor):
    # Test that the processor initializes correctly
    assert isinstance(processor, EVDataProcessor)
    assert processor.df is None

def test_load_data(processor, sample_data):
    # Test loading data into the processor
    processor.df = sample_data  # Simulate loading data
    assert isinstance(processor.df, pd.DataFrame)
    assert not processor.df.empty
    assert len(processor.df) == 3  # Should match our 3 test records
    assert 'Vehicle Location' in processor.df.columns

def test_parse_geopoint(processor):
    # Test the private _parse_geopoint method
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
    # Test that data transformation produces correct output
    df = processed_data
    required_columns = {'Make', 'Model', 'Model Year', 'Electric Range', 'Latitude', 'Longitude'}
    assert required_columns.issubset(set(df.columns))
    
    # Test data types
    assert pd.api.types.is_numeric_dtype(df['Model Year'])
    assert pd.api.types.is_numeric_dtype(df['Electric Range'])
    
    # Test text cleaning
    assert df['Make'].iloc[0] == 'TESLA'
    assert df['Model'].iloc[0] == 'Model 3'
    
    # Test coordinate parsing
    assert df['Latitude'].iloc[0] == 47.456
    assert df['Longitude'].iloc[0] == -122.123

def test_save_processed_data(processor, processed_data, tmp_path):
    # Test saving processed data to file
    test_output = tmp_path / "test_output.parquet"
    
    # Set the processed data in the processor
    processor.df = processed_data
    
    # Save the data - this will fail if method doesn't accept path
    processor.save_processed_data(str(test_output))
    
    # Verify file was created
    assert test_output.exists()
    
    # Verify file contents
    loaded = pd.read_parquet(test_output)
    assert not loaded.empty
    assert len(loaded) == 3
    assert 'Make' in loaded.columns
    assert loaded['Make'].iloc[0] == 'TESLA'
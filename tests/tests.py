import pytest
import pandas as pd
import os

@pytest.fixture
def sample_data_path():
    # Path to test CSV data file
    return os.path.join(os.path.dirname(__file__), 'test_data/sample_ev_data.csv')

@pytest.fixture
def sample_data(sample_data_path):
    # Load sample data from CSV
    return pd.read_csv(sample_data_path)

@pytest.fixture
def processor(sample_data_path):
    # Initialize EVDataProcessor with test data path
    return EVDataProcessor(sample_data_path)

@pytest.fixture
def processed_data(processor):
    # Return processed test data
    processor.load_data()
    return processor.transform_data()
import pytest
import pandas as pd
import os
from code.data_processing import EVDataProcessor

@pytest.fixture
def sample_data_path():
    return os.path.join(os.path.dirname(__file__), 'test_data/sample_ev_data.csv')

@pytest.fixture
def sample_data(sample_data_path):
    return pd.read_csv(sample_data_path)

@pytest.fixture
def processor(sample_data_path):
    return EVDataProcessor(sample_data_path)

@pytest.fixture
def processed_data(processor):
    processor.load_data()
    return processor.transform_data()
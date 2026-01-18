import pandas as pd
import pytest
from src.preprocessing import clean_data, get_pipeline
from src.config import ID_COLUMN

def test_clean_data():
    df = pd.DataFrame({
        ID_COLUMN: ['1', '2'],
        'TotalCharges': ['100', ' '],
        'Churn': ['Yes', 'No']
    })
    
    cleaned = clean_data(df)
    
    assert ID_COLUMN not in cleaned.columns
    assert pd.api.types.is_numeric_dtype(cleaned['TotalCharges'])
    assert cleaned['TotalCharges'].iloc[1] == 0

def test_pipeline_creation():
    pipeline = get_pipeline(['tenure'], ['Partner'])
    assert pipeline is not None

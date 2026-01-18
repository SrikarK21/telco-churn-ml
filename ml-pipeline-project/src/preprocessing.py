import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from src.config import ID_COLUMN, TARGET_COLUMN, RANDOM_STATE, TEST_SIZE

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning before splitting.
    """
    df = df.copy()
    
    # Drop ID column
    if ID_COLUMN in df.columns:
        df = df.drop(columns=[ID_COLUMN])
        
    # 'TotalCharges' is object but should be numeric. It contains ' ' for new customers.
    if 'TotalCharges' in df.columns:
        # Force coerce to NaN for non-numeric, then fill with 0
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
        
    return df

def get_pipeline(numeric_features, categorical_features):
    """
    Returns the Scikit-Learn preprocessing pipeline.
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor

def prepare_data(df: pd.DataFrame):
    """
    Cleans data, separates features and target, and splits into train/test.
    """
    df = clean_data(df)
    
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    
    # Encode target (Yes/No -> 1/0)
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    # Identify feature types
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, numeric_features, categorical_features

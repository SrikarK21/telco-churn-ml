import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.config import MODEL_PATH, METRICS_PATH, RANDOM_STATE
from src.data_loader import load_data
from src.preprocessing import prepare_data, get_pipeline
from src.evaluate import calculate_metrics, save_metrics

def train():
    print("Loading data...")
    df = load_data()
    
    print("Preprocessing data...")
    X_train, X_test, y_train, y_test, num_features, cat_features = prepare_data(df)
    
    print("Building pipeline...")
    preprocessor = get_pipeline(num_features, cat_features)
    
    # Random Forest Classifier
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE))
    ])
    
    print("Training model...")
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    
    metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
    print(f"Metrics: {metrics}")
    
    # Save artifacts
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    save_metrics(metrics, METRICS_PATH)
    
if __name__ == "__main__":
    train()

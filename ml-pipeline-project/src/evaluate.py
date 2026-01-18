import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from pathlib import Path

def calculate_metrics(y_true, y_pred, y_pred_proba=None):
    """
    Calculates classification metrics.
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred)
    }
    
    if y_pred_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_pred_proba)
        
    return metrics

def save_metrics(metrics: dict, save_path: Path):
    """
    Saves metrics to a JSON file.
    """
    with open(save_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {save_path}")

def plot_confusion_matrix(y_true, y_pred, save_path: Path = None):
    """
    Plots and optionally saves confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

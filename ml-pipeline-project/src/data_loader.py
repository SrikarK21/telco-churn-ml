import requests
import pandas as pd
from pathlib import Path
import sys

# Add project root to path to ensure imports work when running as script
sys.path.append(str(Path(__file__).parent.parent))

from src.config import RAW_DATA_PATH, DATA_URL

def download_data(url: str, save_path: Path):
    """Downloads data from a URL to a local path."""
    if save_path.exists():
        print(f"Data already exists at {save_path}")
        return

    print(f"Downloading data from {url}...")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Data saved to {save_path}")
    except Exception as e:
        print(f"Error downloading data: {e}")
        raise

def load_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Loads raw data from CSV."""
    if not path.exists():
        download_data(DATA_URL, path)
    
    df = pd.read_csv(path)
    print(f"Loaded data with shape: {df.shape}")
    return df

if __name__ == "__main__":
    load_data()

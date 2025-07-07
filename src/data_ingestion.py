import pandas as pd
import os

def ingest_data(input_path: str, output_path: str):
    df = pd.read_csv(input_path, nrows=50000)  # Sample subset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    ingest_data("data/raw/uber.csv", "data/processed/cleaned.csv")

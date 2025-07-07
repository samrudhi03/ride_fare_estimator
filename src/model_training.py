import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

def train_model(train_path: str, model_path: str):
    X_train = pd.read_csv(train_path.replace('.csv', '_X.csv'))
    y_train = pd.read_csv(train_path.replace('.csv', '_y.csv'))

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train.values.ravel())

    os.makedirs(os.path.dirname(model_path), exist_ok=True)  # <-- Add this line
    joblib.dump(model, model_path)

if __name__ == "__main__":
    train_model("data/processed/train.csv", "model/model.pkl")


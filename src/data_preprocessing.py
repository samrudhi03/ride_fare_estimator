import pandas as pd
import os
from sklearn.model_selection import train_test_split

def preprocess(input_path: str, train_path: str, test_path: str):
    df = pd.read_csv(input_path)
    df.dropna(inplace=True)
    df = df[(df['fare_amount'] > 0) & (df['passenger_count'] > 0)]
    df = df[(df['pickup_latitude'].between(-90, 90)) & (df['pickup_longitude'].between(-180, 180))]
    df = df[(df['dropoff_latitude'].between(-90, 90)) & (df['dropoff_longitude'].between(-180, 180))]

    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day'] = df['pickup_datetime'].dt.dayofweek

    X = df[['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count', 'hour', 'day']]
    y = df['fare_amount']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    X_train.to_csv(train_path.replace('.csv', '_X.csv'), index=False)
    y_train.to_csv(train_path.replace('.csv', '_y.csv'), index=False)
    X_test.to_csv(test_path.replace('.csv', '_X.csv'), index=False)
    y_test.to_csv(test_path.replace('.csv', '_y.csv'), index=False)

if __name__ == "__main__":
    preprocess("data/processed/cleaned.csv", "data/processed/train.csv", "data/processed/test.csv")

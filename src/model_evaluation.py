import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score

def evaluate_model(test_path: str, model_path: str):
    X_test = pd.read_csv(test_path.replace('.csv', '_X.csv'))
    y_test = pd.read_csv(test_path.replace('.csv', '_y.csv'))

    model = joblib.load(model_path)
    preds = model.predict(X_test)

    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}")

if __name__ == "__main__":
    evaluate_model("data/processed/test.csv", "model/model.pkl")

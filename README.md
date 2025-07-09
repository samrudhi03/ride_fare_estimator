# Ride Fare Estimator

A machine learning project to predict ride fares using Random Forest regression. This project includes data preprocessing, model training, evaluation, and is built with MLOps best practices using DVC and Docker for versioning and reproducibility.

## Overview
Preprocessed raw ride data for feature engineering and cleaning.

Built a Random Forest regression model to predict ride fares.

Evaluated the model performance using RMSE and R² score.

Applied MLOps tools including DVC for data and model version control.

Containerized the application using Docker for easy deployment and scalability.

Organized modular codebase with clear separation for ingestion, preprocessing, model training, and evaluation.

## Technologies Used
Python (Pandas, NumPy, scikit-learn)

Random Forest Regression

Model Evaluation: RMSE, R² score

MLOps Tools: DVC (Data Version Control), Docker

FastAPI / Streamlit for app deployment

## Model Evaluation
The model was evaluated using Root Mean Squared Error (RMSE) and R² score.

The Random Forest model demonstrated strong predictive accuracy after thorough preprocessing.

Evaluation scripts are in src/model_evaluation.py.

## How to Run

Clone the repository:

git clone <your-repo-url>
cd ride-fare-estimator
Set up virtual environment and install dependencies:


python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Run DVC pipeline to pull data and models:

dvc pull
dvc repro

## Launch the app:

uvicorn app.main:app --reload

streamlit run app/app.py




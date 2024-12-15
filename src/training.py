import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
import mlflow.sklearn

def train():
    # Enable MLFlow auto-logging
    mlflow.autolog()

    # Start an MLFlow experiment
    with mlflow.start_run():
        # Load dataset
        df = pd.read_csv(r"D:\\Semester VII\\MLOps\\Class-Activity-7\\airflow_pipeline\\dags\\src\\datasets\\processed_data.csv")
        X = df[["Humidity (%)", "Wind Speed (m/s)", "Cloud Cover (%)", "Precipitation (mm)"]]
        y = df[["Temperature (°C)"]]

        # Initialize and train the model
        md = LinearRegression()
        md.fit(X, y)

        # Log parameters and metrics manually if needed
        mlflow.log_param("features", ["Humidity (%)", "Wind Speed (m/s)", "Cloud Cover (%)", "Precipitation (mm)"])
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("r2_score", md.score(X, y))

        # Save the model as a pickle file (optional)
        model_path = r"D:\\Semester VII\\MLOps\\Class-Activity-7\\models\\model.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(md, f)

        # Log the model with MLFlow
        mlflow.sklearn.log_model(
            sk_model=md,
            artifact_path="sklearn-model",
            registered_model_name="Temperature_Predictor_2"
        )

        print("Model training and logging complete.")

if __name__ == "__main__":
    train()

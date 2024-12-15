import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data():
    df = pd.read_csv(r"D:\\Semester VII\\MLOps\\Class-Activity-7\\airflow_pipeline\\dags\\src\\datasets\\data.csv")
    # df = pd.read_csv(r"/opt/airflow/dags/src/datasets/data.csv", header=None)

    df.ffill(inplace=True)

    scaler = StandardScaler()
    df[["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Precipitation (mm)", "Cloud Cover (%)"]] = scaler.fit_transform(df[["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Precipitation (mm)", "Cloud Cover (%)"]])

    # df.to_csv(r"/opt/airflow/dags/src/datasets/processed_data.csv", index=False)
    df.to_csv(r"D:\\Semester VII\\MLOps\\Class-Activity-7\\airflow_pipeline\\dags\\src\\datasets\\processed_data.csv", index=False)

if __name__ == "__main__":
    preprocess_data()

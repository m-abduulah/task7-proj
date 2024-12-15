import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data():
    df = pd.read_csv(r"/opt/airflow/dags/src/datasets/data.csv", header=None)
    df.columns = ["Temp", "Humid", "Wind Sp", "Weather Cond"]

    df.ffill(inplace=True)

    scaler = StandardScaler()
    df[["Temp", "Humid", "Wind Sp"]] = scaler.fit_transform(df[["Temp", "Humid", "Wind Sp"]])

    df.to_csv(r"/opt/airflow/dags/src/datasets/processed_data.csv", index=False)

if __name__ == "__main__":
    preprocess_data()

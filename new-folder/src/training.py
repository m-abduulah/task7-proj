import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

def train():
    df = pd.read_csv(r"D:\Fast NU\7th semester (pro max plus) shit\MLOps\Class-Activity-7\datasets\processed_data.csv")
    X = df[["Humid", "Wind Sp"]]
    y = df["Temp"]

    md = LinearRegression()
    md.fit(X, y)

    with open(r"D:\Fast NU\7th semester (pro max plus) shit\MLOps\Class-Activity-7\models\model.pkl", "wb") as f:
        pickle.dump(md, f)

if __name__ == "__main__":
    train()

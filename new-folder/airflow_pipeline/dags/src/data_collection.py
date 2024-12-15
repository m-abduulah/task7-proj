import requests
import pandas as pd
from datetime import datetime

API_KEY = "740ef5627c7474d84c79e24d7645480b"
API_KEY = ""
CITY = "Islamabad"
BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&APPID={API_KEY}"

def fetch_data():


response = requests.get(BASE_URL)
data = response.json()

data = {
"Temp": data["main"]["temp"],
"Humid": data["main"]["humidity"],
"Wind Sp": data["wind"]["speed"],
"Weather Cond": data["weather"][0]["description"],
}

df = pd.DataFrame([data])
df.to_csv(r"D:\Fast NU\7th semester (pro max plus) shit\MLOps\Class-Activity-7\datasets\data.csv", index=False, header=False)

if __name__ == "__main__":
fetch_data()

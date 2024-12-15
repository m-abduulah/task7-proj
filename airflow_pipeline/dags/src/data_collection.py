import requests
import pandas as pd
from datetime import datetime, timedelta

# Define API-related constants
API_KEY = "0d76dda9ef654579a70fd451a1fcafb3"  # Insert your Weatherbit API key
CITY_NAME = "London"
LATITUDE = 35.7721  # City latitude
LONGITUDE = -78.63861  # City longitude
API_ENDPOINT = "https://api.weatherbit.io/v2.0/history/daily"


def fetch_data():
    """
    Fetch historical weather data for the past year from the Weatherbit API.
    """
    # Determine the date range (1 year back from today)
    today = datetime.now()
    one_year_ago = today - timedelta(days=50)

    # Placeholder for daily weather data
    collected_data = []

    # Loop through each day in the date range
    current_day = one_year_ago
    while current_day < today:
        # Format dates as strings in YYYY-MM-DD
        start_date = current_day.strftime("%Y-%m-%d")
        next_date = (current_day + timedelta(days=1)).strftime("%Y-%m-%d")

        # Configure query parameters
        query_parameters = {
            "lat": LATITUDE,
            "lon": LONGITUDE,
            "start_date": start_date,
            "end_date": next_date,
            "key": API_KEY,
        }

        # Request weather data from the API
        response = requests.get(API_ENDPOINT, params=query_parameters)

        if response.status_code == 200:
            weather_response = response.json()

            # Ensure the response contains data
            if "data" in weather_response and weather_response["data"]:
                weather_entry = weather_response["data"][0]
                daily_weather = {
                    "Date": start_date,
                    "Temperature (\u00b0C)": weather_entry.get("temp"),
                    "Max Temperature (\u00b0C)": weather_entry.get("max_temp"),
                    "Min Temperature (\u00b0C)": weather_entry.get("min_temp"),
                    "Humidity (%)": weather_entry.get("rh"),
                    "Wind Speed (m/s)": weather_entry.get("wind_spd"),
                    "Precipitation (mm)": weather_entry.get("precip", 0),
                    "Cloud Cover (%)": weather_entry.get("clouds", 0),
                }
                collected_data.append(daily_weather)
                # print(f"Data recorded for {start_date}")
            else:
                print(f"No weather data available for {start_date}")
        else:
            print(f"Error fetching data for {start_date}: {response.status_code} - {response.text}")

        # Proceed to the next day
        current_day += timedelta(days=1)

    # Export the collected data to a CSV file
    if collected_data:
        weather_df = pd.DataFrame(collected_data)

        # Specify the output file path
        # to_csv(r"/opt/airflow/dags/src/datasets/data.csv", index=False, header=False)
        weather_df.to_csv(r"D:\\Semester VII\\MLOps\\Class-Activity-7\\airflow_pipeline\\dags\\src\\datasets\\data.csv", index=False)
        print("Weather data successfully saved to the CSV file.")
    else:
        print("No weather data retrieved.")


if __name__ == "__main__":
    fetch_data()
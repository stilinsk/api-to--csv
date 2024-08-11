import json
import csv
from datetime import datetime
import requests
import time

# List of cities
city_names = [
    'Nairobi', 'London', 'Kampala', 'Thika', 'Beijing',
    'New York', 'Paris', 'Tokyo', 'Sydney', 'Moscow',
    'Berlin', 'Madrid', 'Rome', 'Los Angeles', 'Chicago',
    'Toronto', 'Vancouver', 'Dubai', 'Singapore', 'Hong Kong',
    'Bangkok', 'Istanbul', 'Cairo', 'Johannesburg', 'Buenos Aires',
    'Lagos', 'Lima', 'Mumbai', 'Delhi', 'Shanghai',
    'Seoul', 'Mexico City', 'Jakarta', 'Rio de Janeiro', 'Sao Paulo',
    'Karachi', 'Manila', 'Tehran', 'Baghdad', 'Dhaka',
    'Kinshasa', 'Casablanca', 'Algiers', 'Accra'
]

base_url = 'https://api.openweathermap.org/data/2.5/weather?q='

# Read the API key from the file
with open("credentials.txt", 'r') as f:
    api_key = f.read().strip()  # .strip() to remove any trailing newline characters

def kelvin_to_celsius(temp_in_kelvin):
    temp_in_celsius = temp_in_kelvin - 273.15
    return temp_in_celsius

def etl_weather_data(url):
    r = requests.get(url)
    data = r.json()

    if r.status_code == 200:
        city = data["name"]
        weather_description = data["weather"][0]['description']
        temp_celsius = kelvin_to_celsius(data["main"]["temp"])
        feels_like_celsius = kelvin_to_celsius(data["main"]["feels_like"])
        min_temp_celsius = kelvin_to_celsius(data["main"]["temp_min"])
        max_temp_celsius = kelvin_to_celsius(data["main"]["temp_max"])
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

        transformed_data = {
            "city": city,
            "description": weather_description,
            "temperature": temp_celsius,
            "feelsLike": feels_like_celsius,
            "minimumTemp": min_temp_celsius,
            "maximumTemp": max_temp_celsius,
            "pressure": pressure,
            "humidity": humidity,
            "windSpeed": wind_speed,
            "timeRecorded": time_of_record.isoformat(),
            "sunrise": sunrise_time.isoformat(),
            "sunset": sunset_time.isoformat()
        }
        
        return transformed_data
    else:
        print(f"Failed to get weather data for {url}. Error: {data['message']}")
        return None

def main():
    # Define the CSV file name
    csv_file = "weather_data.csv"
    
    # Write the header once
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "city", "description", "temperature", "feelsLike", "minimumTemp",
            "maximumTemp", "pressure", "humidity", "windSpeed",
            "timeRecorded", "sunrise", "sunset"
        ])
        writer.writeheader()

    curr_time = datetime.now()

    while (datetime.now() - curr_time).seconds < 300:
        for city in city_names:
            full_url = base_url + city + "&APPID=" + api_key
            try:
                weather_data = etl_weather_data(full_url)
                if weather_data:
                    # Append the weather data to the CSV file
                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=weather_data.keys())
                        writer.writerow(weather_data)

                    print(f"Recorded weather data for {weather_data['city']} to CSV")

                # Wait for 5 seconds before the next request
                time.sleep(5)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

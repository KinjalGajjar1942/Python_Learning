import requests
import json

# 1. Your API key + city
API_KEY = "01d13a26795f49f0ab060631252509"  
CITY = "Ahmedabad"    
URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"

try:
    # 2. Call API
    response = requests.get(URL, timeout=5)
    response.raise_for_status()

    # 3. Convert to JSON
    weather_data = response.json()

    # 4. Save full response to file
    with open("weatherapi.json", "w") as f:
        json.dump(weather_data, f, indent=4)

    print("Weather data saved to weatherapi.json")

    # 5. Read it back
    with open("weatherapi.json", "r") as f:
        data = json.load(f)

    # 6. Extract temp & humidity
    temp = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    wind_degree = data["current"]["wind_degree"]

    print(f"🌡 Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Degree: {wind_degree}°")

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except KeyError:
    print("Error extracting temperature/humidity. Check API response.")

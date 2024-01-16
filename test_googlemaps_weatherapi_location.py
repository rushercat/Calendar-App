import tkinter as tk
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city + ',' + country)
        if location:
            return location.latitude, location.longitude
        else:
            print("No location found for the provided city and country.")
            return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

def weather(city, country):
    lat, lon = get_coordinates(city, country)
    if lat is None or lon is None:
        print("Could not find coordinates for the given city and country.")
        return

    try:
        response = requests.get("https://api.weatherapi.com/v1/current.jason", params={
            "key": "c6030ed1293e48eb91e170829233012",
            "q": f"{lat},{lon}"
        })
        response.raise_for_status()
        data = response.json()

        window = tk.Tk()
        window.title("Weather Information")

        weather_label = tk.Label(window, text=f"Weather in {city}, {country}: {data['current']['condition']['text']}")
        weather_label.pack()

        window.mainloop()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 403  :
            print("Access to the weather API is forbidden. Please check your API key and permissions.")
        else:
            print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")

# Get user input for city and country
city = input("Enter city: ")
country = input("Enter country: ")

# Call the weather function with user input
weather(city, country)

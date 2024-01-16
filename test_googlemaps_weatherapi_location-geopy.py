import tkinter as tk
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges
from requests.exceptions import HTTPError

def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city + ',' + country)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def weather(city, country):
    lat, lon = get_coordinates(city, country)
    if lat is None or lon is None:
        print("Coordinates could not be found.")
        return

    try:
        response = requests.get("https://api.weatherapi.com/v1/current.json", params={
            "key": "c6030ed1293e48eb91e170829233012",
            "q": f"{lat},{lon}"
        })
        response.raise_for_status()
        data = response.json()
        # Rest of the code to process weather data...
        
        # Create a Tkinter window
        window = tk.Tk()
        window.title("Weather Information")
        
        # Display the weather information in a label
        weather_label = tk.Label(window, text=f"Weather in {city}, {country}: {data['current']['condition']['text']}")
        weather_label.pack()
        
        # Run the Tkinter event loop
        window.mainloop()
    except HTTPError as http_err:
        if http_err.response.status_code == 403:
            print("Access to the weather API is forbidden.")
        else:
            print(f"An HTTP error occurred: {http_err}")
    except Exception as e:
        if str(e) == "Non-successful status code 403":
            print("Access to the weather API is forbidden.")
        else:
            print(f"An error occurred: {e}")

# Get user input for city and country
city = input("Enter city: ")
country = input("Enter country: ")

# Call the weather function with user input
weather(city, country)


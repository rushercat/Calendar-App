# updatet version of testView2
# The new feature is a complete new version of the day view with an integrated database from the event view. The day view is now able to show all events of a specific day and delete them.

import sqlite3
import tkinter as tk
from tkinter import ttk
import calendar
import json
import requests
from PIL import ImageTk, Image
from io import BytesIO
import boto3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from requests.exceptions import HTTPError
from datetime import datetime
from functools import partial 

def initialize_or_add_event(event_name=None, event_description=None, event_location=None, event_duration=None, event_participants=None, event_priority=None, event_date=None, start_time=None, end_time=None):
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS events (
        event_name TEXT,
        event_description TEXT,
        event_location TEXT,   
        event_duration INTEGER,
        event_participants INTEGER,
        event_priority INTEGER,
        event_date TEXT,
        start_time TEXT,
        end_time TEXT
    )""")

    start_time_val = start_time if start_time else None  
    end_time_val = end_time if end_time else None  

    if all([event_name, event_description, event_location, event_duration, event_participants, event_priority, event_date]): 
        cursor.execute('''
        INSERT INTO events (event_name, event_description, event_location, event_duration, event_participants, event_priority, event_date, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_name, event_description, event_location, event_duration, event_participants, event_priority, event_date, start_time_val, end_time_val))

    conn.commit()
    conn.close()



# Function to add event from the GUI
def add_event(event_name, event_description, event_location, event_duration, event_participants, event_priority, event_date, start_time=None, end_time=None):
    # Convert date from DD.MM.YYYY to YYYY-MM-DD for database compatibility
    start_time_value = None if start_time == '' else start_time
    end_time_value = None if end_time == '' else end_time

    # Convert date to YYYY-MM-DD format
    day, month, year = event_date.split('.')
    formatted_event_date = f"{year}-{month}-{day}"

    # Insert into the database
    initialize_or_add_event(
        event_name,
        event_description,
        event_location,
        event_duration,
        event_participants,
        event_priority,
        formatted_event_date,
        start_time_value,
        end_time_value
    )
    
    print("Event added successfully.")
    
    # Automatically switch to the day view of the added event
    # Ensure that yearGlobal and monthGlobal are updated if the event is in a different month/year
    global yearGlobal, monthGlobal
    yearGlobal, monthGlobal = int(year), int(month)

    # Call show_day_view with the correct day parameter
    show_day_view(int(day))

    # Refresh the right box with the latest upcoming events
    populate_upcoming_events()


def show_event_view():
    global event_name_entry, event_description_entry, event_location_entry, event_duration_entry, event_participants_entry, event_priority_entry, event_date_entry, start_time_entry, end_time_entry

    view_header_label.config(text="Event View")
    for widget in middle_box.winfo_children():
        widget.destroy()

    labels = ["Event Name", "Event Description", "Event Location", "Event Duration", "Event Participants", "Event Priority", "Event Date (DD.MM.YYYY)", "Start Time (HH:MM)", "End Time (HH:MM)"]
    entries = []
    for row, label_text in enumerate(labels):
        label = tk.Label(middle_box, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(middle_box)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        entries.append(entry)

    event_name_entry, event_description_entry, event_location_entry, event_duration_entry, event_participants_entry, event_priority_entry, event_date_entry, start_time_entry, end_time_entry = entries

    add_event_button = tk.Button(middle_box, text='Add Event', command=lambda: add_event(
        event_name_entry.get(), 
        event_description_entry.get(), 
        event_location_entry.get(), 
        event_duration_entry.get(), 
        event_participants_entry.get(), 
        event_priority_entry.get(), 
        event_date_entry.get(),
        start_time_entry.get(),
        end_time_entry.get()
    ))
    add_event_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")






# Global variables
monthGlobal = 2
yearGlobal = 2024
currentView = "month"
def next_month():
    global monthGlobal, yearGlobal
    if monthGlobal == 12:
        monthGlobal = 1
        yearGlobal += 1
    else:
        monthGlobal += 1
    populate_month(monthGlobal, yearGlobal)


def previous_month():
    global monthGlobal, yearGlobal
    if monthGlobal == 1:
        monthGlobal = 12
        yearGlobal -= 1
    else:
        monthGlobal -= 1
    populate_month(monthGlobal, yearGlobal)

def resize(event):
    # Resize logic here
    pass

def number_to_month(number):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    if number >= 1 and number <= 12:
        return months[number - 1]
    else:
        return None

def populate_month(month, year):
    # Update the global variables
    global monthGlobal, yearGlobal, currentView
    monthGlobal = month
    yearGlobal = year

    # Set the current view to month
    currentView = "month"
    month_name = number_to_month(month)
    view_header_label.config(text=str(month_name) + ", " + str(yearGlobal))


    # Clear content frame
    for widget in middle_box.winfo_children():
        widget.destroy()

    # Draw month view
    cal = calendar.monthcalendar(year, month)

    # Get the current day
    current_day = calendar.datetime.date.today().day
    current_month = calendar.datetime.date.today().month
    current_year = calendar.datetime.date.today().year

    # Create a 8x8 grid view
    for row in range(8):
        middle_box.grid_rowconfigure(row, weight=1)  # Set row weight to 1
        for col in range(7):
            middle_box.grid_columnconfigure(col, weight=1)  # Set column weight to 1
            if row == 0 and col == 0:
                day_label = tk.Label(middle_box, text=str("<"))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
                day_label.bind("<Button-1>", lambda event: previous_month())  # Bind the click event to the show_day_view function with the respective day as a parameter
            elif row == 0 and col == 1:
                day_label = tk.Label(middle_box, text=str(">"))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
                day_label.bind("<Button-1>", lambda event: next_month())  # Bind the click event to the show_day_view function with the respective day as a parameter   
            # insert the first row with the days
            elif row == 0:
                pass
            elif row == 1:
                days = ["M", "T", "W", "T", "F", "S", "S"]
                day_label = tk.Label(middle_box, text=str(days[col]))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell

            else:
                # Create a label widget for each day in the calendar
                try:
                    day = cal[row-2][col]
                    if day != 0:
                        day_label = tk.Label(middle_box, text=str(day))
                        day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
                        day_label.bind("<Button-1>", lambda event, day=day: show_day_view(day))  # Bind the click event to the show_day_view function with the respective day as a parameter

                        # Color the current day
                        if day == current_day and monthGlobal == current_month and yearGlobal == current_year:
                            day_label.config(bg="lightblue")  # Set the background color to red for the current day
                except IndexError:
                    print("IndexError: cal[{}][{}]".format(row, col))




# Function to get coordinates based on city and country
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

# Function to get weather information and display it
def fetch_weather():
    city = city_entry.get()
    country = country_entry.get()
    lat, lon = get_coordinates(city, country)
    if lat is None or lon is None:
        weather_label.config(text="Coordinates could not be found.")
        return

    try:
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=9f81700dee234f0a829113545241501&q={lat},{lon}")
        response.raise_for_status()
        data = response.json()

        condition = data['current']['condition']['text']
        icon_url = 'https:' + data['current']['condition']['icon']
        temp = data['current']['temp_c']
        name = data['location']['name']
        country = data['location']['country']

        icon_response = requests.get(icon_url)
        icon_data = icon_response.content
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)

        weather_label.config(text=f"Weather in {name}, {country}: {temp}°C, {condition}", image=icon_photo, compound='top')
        weather_label.image = icon_photo
    except requests.exceptions.RequestException as e:
        weather_label.config(text=f"Error fetching weather data: {e}")


def delete_event(event_name, event_date):
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event_name = ? AND event_date = ?", (event_name, event_date))
    conn.commit()
    conn.close()
    print(f"Deleted event '{event_name}' on {event_date}.")


def show_day_view(day):
    global currentView, monthGlobal, yearGlobal
    currentView = "day"
    # Ensure the date format matches the database format
    selected_date = f"{yearGlobal}-{monthGlobal:02d}-{day:02d}"
    view_header_label.config(text=f"{day}. {number_to_month(monthGlobal)}, {yearGlobal}")
    
    # Clear previously displayed widgets
    for widget in middle_box.winfo_children():
        widget.destroy()

    # Add "Add Event" button to day view
    add_event_button = tk.Button(middle_box, text="Add Event", command=show_event_view)
    add_event_button.pack(pady=10)

    # Connect to the database and fetch events for the selected date
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    query = """
    SELECT event_name, event_description, event_location, event_participants, event_priority, event_date, start_time, end_time
    FROM events
    WHERE event_date = ?
    ORDER BY event_priority DESC, CASE WHEN start_time IS NULL THEN 1 ELSE 0 END, start_time
    """
    cursor.execute(query, (selected_date,))
    events = cursor.fetchall()

    # Display events, handling None start and end times
    if events:
        for event in events:
            start_time_display = "Start Time: Not specified" if event[6] is None else f"Start Time: {event[6]}"
            end_time_display = "End Time: Not specified" if event[7] is None else f"End Time: {event[7]}"
            
            event_info = f"Name: {event[0]}\nDescription: {event[1]}\nLocation: {event[2]}\nParticipants: {event[3]}\nPriority: {event[4]}\nDate: {event[5]}\n{start_time_display}\n{end_time_display}"
            event_frame = tk.Frame(middle_box)
            event_frame.pack(fill='x', padx=5, pady=5, anchor="w")
            tk.Label(event_frame, text=event_info, justify="left").pack(side="left")
            
            delete_btn = tk.Button(event_frame, text="Delete", command=lambda e=event: delete_event_and_refresh_view(e[0], e[5], day))
            delete_btn.pack(side="right")
            
            ttk.Separator(middle_box).pack(fill='x', padx=5, pady=5)
    else:
        no_events_label = tk.Label(middle_box, text="No events for this day.")
        no_events_label.pack(padx=10, pady=5)
    
    conn.close()


def delete_event_and_refresh_view(event_name, event_date, day):
    delete_event(event_name, event_date)
    show_day_view(day)


def edit_event_with_fetch(event_name, event_date):
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT event_description, start_time, end_time FROM events WHERE event_name = ? AND event_date = ?", (event_name, event_date))
    event_data = cursor.fetchone()  # Fetch the rest of the event details
    conn.close()

    if event_data:
        # Pass the retrieved event data to the edit_event function
        edit_event(event_name, event_date, event_data[0], event_data[1], event_data[2]) 
    else:
        print("Event not found!")

def edit_event(event_name, event_date, event_description=None, event_start_time=None, event_end_time=None):
    def update_event():
        # Get new values from edit_window entries
        new_event_name = edit_name_entry.get()
        new_event_date = edit_date_entry.get()
        new_event_description = edit_description_entry.get()
        new_event_start_time = edit_start_time_entry.get()
        new_event_end_time = edit_end_time_entry.get()

        # Validation (optional, but recommended)
        if not new_event_date:  # Check if the date is empty
            print("Please enter a valid date.")
            return

        # Database update logic (using your database interaction code)
        conn = sqlite3.connect('event_database.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE events
            SET event_name = ?,
                event_description = ?,
                event_date = ?,
                start_time = ?,
                end_time = ?
            WHERE event_name = ? AND event_date = ?
        """, (new_event_name, new_event_description, new_event_date, new_event_start_time, new_event_end_time, event_name, event_date))
        conn.commit()
        conn.close()

        # GUI Update logic (refresh views after changes)
        if currentView == "day":
            day, month, year = new_event_date.split('.')
            show_day_view(int(day))
        populate_upcoming_events()

        # Close the edit window
        edit_window.destroy()

    # Create a pop-up window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Event")

    # Frame to group widgets for better organization
    content_frame = tk.Frame(edit_window, padx=5, pady=5)
    content_frame.pack(fill='both', expand=True) 

    # Labels and entry fields for editable attributes
    tk.Label(content_frame, text="Event Name:").grid(row=0, column=0)
    edit_name_entry = tk.Entry(content_frame)
    edit_name_entry.insert(0, event_name) 
    edit_name_entry.grid(row=0, column=1)

    tk.Label(content_frame, text="Event Date (DD.MM.YYYY):").grid(row=1, column=0)
    edit_date_entry = tk.Entry(content_frame)
    edit_date_entry.insert(0, event_date)
    edit_date_entry.grid(row=1, column=1)

    tk.Label(content_frame, text="Event Description:").grid(row=2, column=0)
    edit_description_entry = tk.Entry(content_frame)
    edit_description_entry.insert(0, event_description)
    edit_description_entry.grid(row=2, column=1)

    tk.Label(content_frame, text="Start Time (HH:MM):").grid(row=3, column=0)
    edit_start_time_entry = tk.Entry(content_frame)
    edit_start_time_entry.insert(0, event_start_time or "")
    edit_start_time_entry.grid(row=3, column=1)

    tk.Label(content_frame, text="End Time (HH:MM):").grid(row=4, column=0)
    edit_end_time_entry = tk.Entry(content_frame)
    edit_end_time_entry.insert(0, event_end_time or "")
    edit_end_time_entry.grid(row=4, column=1)

    # Button Frame
    # Button Frame - Adjusted to fit into the grid system
    button_frame = tk.Frame(content_frame)
# Place the button_frame in the next row after the last entry, spanning across two columns.
    button_frame.grid(row=5, column=0, columnspan=2, pady=5)

# Add the Update button
    update_button = tk.Button(button_frame, text="Change", command=update_event)
    update_button.pack(side=tk.LEFT)  # Use pack inside the button_frame, but ensure button_frame is correctly placed using grid.



def populate_upcoming_events():
    # Clear the right box first
    for widget in right_box.winfo_children():
        widget.destroy()

    # Get today's date in the format stored in your database
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Connect to the database
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()

    # Fetch upcoming events, sorted by date and start time
    cursor.execute("""
        SELECT event_name, event_description, event_date, start_time
        FROM events
        WHERE event_date >= ?
        ORDER BY event_date ASC, start_time ASC
    """, (today_date,))

    # Fetch all matching records
    upcoming_events = cursor.fetchall()

    # Display upcoming events
    for event in upcoming_events:
        event_date_str = datetime.strptime(event[2], "%Y-%m-%d").strftime("%d.%m.%Y")  # Format date
        start_time_display = event[3] if event[3] else "Time Not Specified"

        event_frame = tk.Frame(right_box)
        event_frame.pack(fill='x', expand=True, padx=5, pady=2)

        tk.Label(event_frame, text=f"Name: {event[0]}, Date: {event_date_str}, Start: {start_time_display}\nDesc: {event[1]}", wraplength=250, justify="left", anchor="nw").pack(side="left", fill='x', expand=True)

        # Assuming you have the full event data in a tuple called 'event_data' 
        edit_button = tk.Button(event_frame, text="Edit", command=lambda e=event: edit_event_with_fetch(e[0], e[2]))
        edit_button.pack(side="right", padx=2)




# Function to switch to the month view
def switch_to_month_view():
    if currentView != "month":
        populate_month(monthGlobal, yearGlobal)

def switch_to_day_view():
    if currentView != "day":
        show_day_view(1)

def switch_to_event_view():
    if currentView != "event":
        show_event_view()

# Create the main window
root = tk.Tk()

# Create the main header
header_frame = tk.Frame(root, bd=2, relief=tk.SOLID, bg="lightblue")
header_frame.pack(fill=tk.X)

header_text = "Calendar Application"
header_label = tk.Label(header_frame, text=header_text, font=("Arial", 16, "bold"))
header_label.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X)

# Add view switch buttons to the main header
month_button = tk.Button(header_frame, text="Month View", command=switch_to_month_view)
month_button.pack(side=tk.LEFT, padx=10, pady=10)

day_button = tk.Button(header_frame, text="Day View", command=switch_to_day_view)
day_button.pack(side=tk.LEFT, padx=10, pady=10)

event_button = tk.Button(header_frame, text="Event View", command=switch_to_event_view)
event_button.pack(side=tk.LEFT, padx=10, pady=10)

# Add additional header for view indication
view_header_text = "Current View: " + currentView.capitalize()
view_header_label = tk.Label(root, text=view_header_text, font=("Arial", 12), bd=2, relief=tk.SOLID, bg="lightgreen")
view_header_label.pack(fill=tk.X)

# Create left, middle, and right boxes
left_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="blue")
left_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
left_box.configure(highlightbackground="darkblue", highlightcolor="blue", highlightthickness=2)

middle_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="Grey")
middle_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
middle_box.configure(highlightbackground="Black", highlightcolor="Black", highlightthickness=2)


right_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="lightgreen")
right_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
right_box.configure(highlightbackground="lightgreen", highlightcolor="red", highlightthickness=2)

# GUI code (root, header_frame, header_label, view_header_label, left_box, middle_box, right_box)

# Weather input fields and button
weather_frame = tk.Frame(left_box)
weather_frame.pack(pady=10)

city_label = tk.Label(weather_frame, text="City:")
city_label.grid(row=0, column=0)
city_entry = tk.Entry(weather_frame)
city_entry.grid(row=0, column=1)

country_label = tk.Label(weather_frame, text="Country:")
country_label.grid(row=1, column=0)
country_entry = tk.Entry(weather_frame)
country_entry.grid(row=1, column=1)

fetch_weather_button = tk.Button(weather_frame, text="Fetch Weather", command=fetch_weather)
fetch_weather_button.grid(row=2, column=0, columnspan=2)

weather_label = tk.Label(left_box, text="Weather Information")
weather_label.pack()

# Example usage
# To initialize the database or table without adding an event, simply call the function without arguments.
initialize_or_add_event()

# Bind resize event
root.bind("<Configure>", resize)

# Call populate_month initially
populate_month(monthGlobal, yearGlobal)

# Call the function to initially populate the right box
populate_upcoming_events()
# Start the main event loop
root.mainloop()



populate_month(monthGlobal, yearGlobal)
root.mainloop()
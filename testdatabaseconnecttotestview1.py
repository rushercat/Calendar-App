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
import mysql.connector


def create_database():
    
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_name TEXT,
        event_description TEXT,
        event_location TEXT,
        event_duration TEXT,
        event_participants INTEGER,
        event_priority INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def add_event_to_database(event_name, event_description, event_location, event_duration, event_participants, event_priority):
    
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO events (event_name, event_description, event_location, event_duration, event_participants, event_priority)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (event_name, event_description, event_location, event_duration, event_participants, event_priority))
    cursor.execute("SELECT * FROM events")

    
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        print(row[4])
        print(row[5])
    conn.commit()
    conn.close()




# Global variables
monthGlobal = 12
yearGlobal = 2023
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



#Wetter API
def weather(lat,lon,):
    Response = requests.get("https://api.weatherapi.com/v1/current.json?key=c6030ed1293e48eb91e170829233012&q="+str(lat)+","+str(lon))
    #51.508669,-0.082512
    print(Response.json())
    condition = Response.json()['current']['condition']['text']
    icon = 'https:' + str(Response.json()['current']['condition']['icon'])
    temp = Response.json()['current']['temp_c']
    name = Response.json()['location']['name']
    country = Response.json()['location']['country']
    response = requests.get(icon)
    icon_data = response.content

    # Create an image from the icon data
    icon_image = Image.open(BytesIO(icon_data))

    # Resize the image if needed
    #icon_image = icon_image.resize((50, 50))

    # Convert the image to Tkinter-compatible format
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Create a label to display the image
    #icon_label = tk.Label(left_box, image=icon_photo)
    #icon_label.pack()

    # Keep a reference to the image to prevent it from being garbage collected
    #icon_label.image = icon_photo

    # Clear content frame
    for widget in left_box.winfo_children():
        widget.destroy()

    # Draw day view
    # Create a 3x10 grid view
    for row in range(4):
        left_box.grid_rowconfigure(row, weight=1)  # Set row weight to 1
        for col in range(1):
            left_box.grid_columnconfigure(col, weight=1)  # Set column weight to 1
            if row == 0:
                day_label = tk.Label(left_box, text=str(name)+", "+str(country))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            elif row == 1:
                day_label = tk.Label(left_box, text=str(temp)+"°C")
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            elif row == 2:
                day_label = tk.Label(left_box, text=str(condition))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            elif row == 3:
                day_label = tk.Label(left_box, image=icon_photo)
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")#
                #day_label.pack()
                day_label.image = icon_photo


def show_day_view(day): 
    # Update the global variables
    global currentView, monthGlobal, yearGlobal
    currentView = "day"

    view_header_label.config(text=str(day) + ". " + str(number_to_month(monthGlobal)) + ", " + str(yearGlobal))

    # Clear content frame
    for widget in middle_box.winfo_children():
        widget.destroy()

    # Draw day view 
    # Create a 3x10 grid view
    for row in range(10):
        middle_box.grid_rowconfigure(row, weight=1)  # Set row weight to 1
        for col in range(3):
            middle_box.grid_columnconfigure(col, weight=1)  # Set column weight to 1
            
            if col == 0:
                day_label = tk.Label(middle_box, text=str(row + 9) + ":00")
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
def show_event_view():
    # Update the global variables
    global currentView
    currentView = "event"
    view_header_label.config(text="Event View")
    
    # Clear content frame
    for widget in middle_box.winfo_children():
        widget.destroy()

    # Draw event view
    # Create a 2x10 grid view
    for row in range(7):
        middle_box.grid_rowconfigure(row, weight=1)  # Set row weight to 1
        for col in range(2):
            middle_box.grid_columnconfigure(col, weight=1)  # Set column weight to 1
            if col == 0 and row < 6:
                content = ["Event Name", "Event Description", "Event Location", "Event Duration", "Event Participants", "Event Priority"]
                day_label = tk.Label(middle_box, text=str(content[row]))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
            else:
                if row == 6 and col == 0:
                    print('reach the button')
                    button = tk.Button(middle_box, text='Add Event', command=lambda: add_event(event_name_entry.get(), event_description_entry.get(), event_location_entry.get(), event_duration_entry.get(), event_participants_entry.get(), event_priority_entry.get()))
                    button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                    
                    # Entry fields for event details
                    event_name_entry = tk.Entry(middle_box)
                    event_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
                    
                    event_description_entry = tk.Entry(middle_box)
                    event_description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
                    
                    event_location_entry = tk.Entry(middle_box)
                    event_location_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
                    
                    event_duration_entry = tk.Entry(middle_box)
                    event_duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
                    
                    event_participants_entry = tk.Entry(middle_box)
                    event_participants_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
                    
                    event_priority_entry = tk.Entry(middle_box)
                    event_priority_entry.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
'''
def show_event_view():
    # Update the global variables
    global currentView
    currentView = "event"
    view_header_label.config(text="Event View")
    
    # Clear content frame
    for widget in middle_box.winfo_children():
        widget.destroy()

    # Draw event view
    # Create a 2x10 grid view
    for row in range(7):
        middle_box.grid_rowconfigure(row, weight=1)  # Set row weight to 1
        for col in range(2):
            middle_box.grid_columnconfigure(col, weight=1)  # Set column weight to 1
            if col == 0 and row < 6:
                content = ["Event Name", "Event Description", "Event Location", "Event Duration", "Event Participants", "Event Priority"]
                day_label = tk.Label(middle_box, text=str(content[row]))
                day_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
            else:
                if row == 6 and col == 0:
                    print('reach the button')
                    button = tk.Button(middle_box, text='Add Event', command=add_event)
                    button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                elif row == 6 and col == 1:
                    pass
                else:
                    entry = tk.Entry(middle_box)
                    entry.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use sticky="nsew" to fill the entire cell
  '''              
def add_event(event_name, event_description, event_location, event_duration, event_participants, event_priority):
    # TODO implement functionality to add an event (to the database)
    print("Added event")
    add_event_to_database(event_name, event_description, event_location, event_duration, event_participants, event_priority)
   
def switch_to_month_view():
    if currentView != "month":
        populate_month(monthGlobal, yearGlobal)

def switch_to_day_view():
    if currentView != "day":
        show_day_view(1)

def switch_to_event_view():
    if currentView != "event":
        show_event_view()
'''
def create_table():
    # AWS RDS configuration
    rds_endpoint = 'database-1.czoa4ea2w8xs.eu-central-1.rds.amazonaws.com'
    db_name = 'database-1'
    db_username = 'kvboxberg@gmx.de'
    db_password = 'Wolfram99'

    # Connect to the RDS instance
    client = boto3.client('rds-data')

    # SQL statement to create the table
    sql_statement = 
        CREATE TABLE user (
            id int NOT NULL AUTO_INCREMENT,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL,
            password varchar(255) NOT NULL,
            status varchar(255) NOT NULL,
            PRIMARY KEY (id)
        )
          
         

    # Execute the SQL statement
    response = client.execute_statement(
        resourceArn=rds_endpoint,
        secretArn='your_secret_arn',
        database=db_name,
        sql=sql_statement,
        parameters=[]
    )
    
    # Print the response
    print(response)
    '''    
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
left_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="lightblue")
left_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
left_box.configure(highlightbackground="lightblue", highlightcolor="red", highlightthickness=2)

middle_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="lightyellow")
middle_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
middle_box.configure(highlightbackground="lightyellow", highlightcolor="lightyellow", highlightthickness=2)

right_box = tk.Frame(root, bd=2, relief=tk.SOLID, bg="lightgreen")
right_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
right_box.configure(highlightbackground="lightgreen", highlightcolor="red", highlightthickness=2)

create_database()
#root = tk.Tk()
# Bind resize event
root.bind("<Configure>", resize)

# Call populate_month initially
populate_month(monthGlobal, yearGlobal)

weather(51.13819451525496,1.2872157194039093)

# Start the main event loop
root.mainloop()



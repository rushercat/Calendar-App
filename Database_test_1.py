
import sqlite3
import tkinter as tk
from tkinter import ttk
#py -m pip install (tkcalendar)
def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('event_database.db')
    # Create a cursor object
    cursor = conn.cursor()
    # Create table
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
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def add_event(event_name, event_description, event_location, event_duration, event_participants, event_priority):
    # Connect to the database
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    # Insert a new event
    cursor.execute('''
    INSERT INTO events (event_name, event_description, event_location, event_duration, event_participants, event_priority)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (event_name, event_description, event_location, event_duration, event_participants, event_priority))
    # Commit and close
    conn.commit()
    conn.close()
    # Refresh the GUI
    refresh_gui()

def print_database():
    # Connect to the database
    conn = sqlite3.connect('event_database.db')
    cursor = conn.cursor()
    # Retrieve all events from the database
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    # Close the connection
    conn.close()
    # Create a GUI window
    window = tk.Tk()
    window.title("Event Database")
    # Create a treeview to display the events
    tree = ttk.Treeview(window)
    tree["columns"] = ("name", "description", "location", "duration", "participants", "priority")
    tree.heading("name", text="Event Name")
    tree.heading("description", text="Description")
    tree.heading("location", text="Location")
    tree.heading("duration", text="Duration")
    tree.heading("participants", text="Participants")
    tree.heading("priority", text="Priority")
    # Insert the events into the treeview
    for event in events:
        tree.insert("", "end", values=event)
    tree.pack()
    # Run the GUI event loop
    window.mainloop()

def refresh_gui(window):
    # Clear the GUI window
    for widget in window.winfo_children():
        widget.destroy()
    # Print the contents of the database
    print_database()

# Example usage
create_database()
add_event('Concert', 'Music event', 'Central Park', '2 hours', 500, 1)



def refresh_gui(window):
    # Clear the GUI window
    for widget in window.winfo_children():
        widget.destroy()
    # Print the contents of the database
    print_database()

# Example usage
create_database()
add_event('Concert', 'Music event', 'Central Park', '2 hours', 500, 1)

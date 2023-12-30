import tkinter as tk
from tkinter import Label
from _tkinter import TclError
from datetime import datetime
import calendar

def create_monthly_calendar():
    # Create a tkinter window
    window = tk.Tk()

    def resize_window(event):
        # Update the size of the window
        window.geometry(f"{event.width}x{event.height}")

        # Update the size of the calendar box
        calendar_box.config(width=event.width, height=event.height)

    # Enable window resizing
    window.bind("<Configure>", resize_window)

    # Get the current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Create a calendar instance
    cal = calendar.monthcalendar(year, month)

    # Create a label for the month and year
    month_label = Label(window, text=calendar.month_name[month] + " " + str(year))
    month_label.pack()

    # Create a frame for the calendar box
    calendar_box = tk.Frame(window, borderwidth=1, relief="solid")
    calendar_box.pack(expand=True, fill=tk.BOTH)

    def update_calendar():
        # Clear the existing calendar
        for widget in calendar_box.winfo_children():
            widget.destroy()

        # Create a new calendar instance
        new_cal = calendar.monthcalendar(year, month)

        # Update the month and year label if it exists
        if month_label.winfo_exists():
            month_label.config(text=calendar.month_name[month] + " " + str(year))

        # Create a grid layout for the calendar
        for week in new_cal:
            for day in week:
                # Create a frame for each day
                frame = tk.Frame(calendar_box, width=100, height=100, borderwidth=1, relief="solid")
                frame.grid(row=new_cal.index(week), column=week.index(day), sticky="nsew")

                # Configure frame to scale with window size
                frame.grid_propagate(False)

                # Create a label for the day
                label = tk.Label(frame, text=str(day))
                label.pack()

                # Create a text box for events
                textbox = tk.Text(frame, height=3, width=10)
                textbox.pack()

    def prev_month():
        nonlocal month, year
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        update_calendar()

    def next_month():
        nonlocal month, year
        month += 1
        if month == 13:
            month = 1
            year += 1
        update_calendar()

    # Create a frame for the calendar elements
    calendar_elements_frame = tk.Frame(calendar_box)
    calendar_elements_frame.pack(expand=True, fill=tk.BOTH)

    # Create buttons for changing the month
    prev_button = tk.Button(calendar_elements_frame, text="Prev", command=prev_month)
    prev_button.pack(side=tk.LEFT)

    next_button = tk.Button(calendar_elements_frame, text="Next", command=next_month)
    next_button.pack(side=tk.RIGHT)

    # Run the tkinter event loop
    update_calendar()
    window.mainloop()

create_monthly_calendar()

import tkinter as tk
import calendar

# global variables
monthGlobal = 12
yearGlobal = 2023
currentView = "month"

def resize(event):
    canvas.delete("border")
    canvas.create_rectangle(2, 2, event.width-2, event.height-2, outline="black", tags="border")
    inner_box_size = min(event.width, event.height) * 0.75
    inner_box_x = (event.width - inner_box_size) // 2
    inner_box_y = (event.height - inner_box_size) // 2
    canvas.create_rectangle(inner_box_x, inner_box_y, inner_box_x + inner_box_size, inner_box_y + inner_box_size, outline="orange", tags="border")
       

    def populate_month(month, year):
        # update the global variables
        global monthGlobal, yearGlobal, currentView
        monthGlobal = month
        yearGlobal = year

        # set the current view to month
        currentView = "month"

         # Clear existing grid
        canvas.delete("grid")

        # Calculate cell size
        cell_size = inner_box_size // 7

        # creation of the grid layout

        # Draw grid lines
        for x1 in range(8):
            for y1 in range(8):
                x = inner_box_x + x1 * cell_size
                canvas.create_line(x, inner_box_y, x, inner_box_y + inner_box_size, tags="grid")
                y = inner_box_y + y1 * cell_size
                canvas.create_line(inner_box_x, y, inner_box_x + inner_box_size, y, tags="grid")

        # Write day names in the top row
        actions = ["Previous", "Next", "December", "_", "Previous", "2023", "Next"]
        for i, action in enumerate(actions):
            if i < 2:
                button = tk.Button(canvas, text=action)
                x = inner_box_x + i * cell_size + cell_size // 2
                y = inner_box_y + cell_size // 2
                canvas.create_window(x, y, window=button, tags="grid")
            else:
                x = inner_box_x + i * cell_size + cell_size // 2
                y = inner_box_y + cell_size // 2
                canvas.create_text(x, y, text=action, tags="grid")

        # Write day names in the top row
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            x = inner_box_x + i * cell_size + cell_size // 2
            y = inner_box_y + cell_size // 2 + cell_size
            canvas.create_text(x, y, text=day, tags="grid")

        # back to the old method

        # Clear existing day labels
        canvas.delete("day_label")

        # Get the calendar for the specified month and year
        cal = calendar.monthcalendar(year, month)

        # Calculate cell size
        cell_size = inner_box_size // 7

        # Populate the grid with day labels
        for row in range(6):
            for col in range(7):
                day = cal[row][col]
                if day != 0:
                    x = inner_box_x + col * cell_size + cell_size // 2
                    y = inner_box_y + (row + 1) * cell_size + cell_size // 2 + cell_size
                    day_label = canvas.create_text(x, y, text=str(day), tags="day_label")
                    canvas.tag_bind(day_label, "<Button-1>", lambda event, day=day: show_day_view(day))

    def show_day_view(day):
        # update the global variables
        global currentView
        currentView = "day"

        # Remove the monthly calendar view
        canvas.delete("border")
        canvas.delete("grid")
        canvas.delete("day_label")

        # Create the day view box
        day_view_box = canvas.create_rectangle(2, 2, canvas.winfo_width()-2, canvas.winfo_height()-2, outline="orange", tags="border")

        # Create the header
        header_box = canvas.create_rectangle(2, 2, canvas.winfo_width()-2, 32, fill="orange", outline="orange", tags="header")

        # Create the text containing day, month, and year
        date_text = str(day) + " " + str(monthGlobal) + " " + str(yearGlobal)
        date_label = canvas.create_text(canvas.winfo_width() // 2, 16, text=date_text, font=("Arial", 24), tags="header")

        # Create the back button
        back_button = tk.Button(canvas, text="Back", command=lambda: populate_month(monthGlobal, yearGlobal))
        canvas.create_window(canvas.winfo_width() - 32, 16, window=back_button, tags="header")

    # Call the function to populate December 2023
    populate_month(12, 2023)

root = tk.Tk()

# Create the top bar
top_bar = tk.Frame(root, bg="orange", height=30)
top_bar.pack(fill=tk.X)

# Add the title to the top bar
title_label = tk.Label(top_bar, text="Calendar App", fg="white", bg="orange")
title_label.pack()

# Create the canvas
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Configure>", resize)

root.mainloop()
root.geometry("200x200")

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Configure>", resize)

root.mainloop()

# Import the tkinter library
from tkinter import *
import time

# Create an instance of the canvas
win = Tk()

# Select the title of the window
win.title("tutorialspoint.com")

# Define the geometry of the window
win.geometry("600x400")


# Define the clock which
def clock():
    hh = time.strftime("%I")
    mm = time.strftime("%M")
    ss = time.strftime("%S")
    day = time.strftime("%A")
    ap = time.strftime("%p")
    time_zone = time.strftime("%Z")
    my_lab.config(text=hh + ":" + mm + ":" + ss)
    my_lab.after(1000, clock)

    my_lab1.config(text=time_zone + " " + day)


# Update the Time

# Creating the label with text property of the clock
my_lab = Label(win, text="", font=("sans-serif", 56), fg="red")
my_lab.pack(pady=20)
my_lab1 = Label(win, text="", font=("Helvetica", 20), fg="blue")
my_lab1.pack(pady=10)

# Calling the clock function
clock()
# Keep Running the window

win.mainloop()

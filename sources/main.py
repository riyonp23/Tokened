import socket
from sys import exit

import customtkinter as ctk
import pymongo.errors
from plyer import notification
from pymongo import MongoClient

import env
from account import accountPage
from addEvent import eventPage
from help import helpPage
from login import loginPage
from report import reportPage
from signup import signUpPage
from student import studentDashboard
from teacher import teacherDashboard


# Checks for Internet Connection
def check_internet():
    try:
        host = socket.gethostbyname("www.google.com")
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


# Database Link
if check_internet():
    try:
        cluster = MongoClient(env.dbLink)
        db = cluster["Tokened"]
        student = db["student"]
        teacher = db["teacher"]
        events = db["events"]
        student_events = db["student_events"]
    except pymongo.errors.ConnectionFailure as e:
        notification.notify(
            title="MongoDB Error",  # Sends notification if there is a database error
            message="Could not connect to MongoDB: %s" % e,
            app_name="Tokened",
            app_icon=env.img[2],
            timeout=10
        )
        exit()
else:
    notification.notify(  # Sends notification, if there is no internet
        title="No Internet Connection",
        message="Please check your internet connection and try again.",
        app_name="Tokened",
        app_icon=env.img[2],
        timeout=10
    )
    exit()


class App(ctk.CTk):  # Used https://pythonprogramming.net/change-show-new-frame-tkinter/ as template
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        ctk.set_appearance_mode("dark")  # creates default appearance mode
        ctk.set_default_color_theme("dark-blue")  # creates theme for application
        self.title("Tokened")  # sets application title
        self.geometry("800x500")  # sets application size
        self.resizable(False, False)  # makes application non-realizable
        self.iconbitmap(env.img[2])  # sets icon for application
        self.update_idletasks()

        # sets frame for application
        container = ctk.CTkFrame(self, height=800, width=500)

        container.pack(side="top", fill="both", expand=True)

        # configures grid to design window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (loginPage, signUpPage, studentDashboard, teacherDashboard, eventPage, reportPage, helpPage,
                  accountPage):  # All pages listed here
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Starts on Login Page
        self.show_frame(loginPage)

    # function to switch pages
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":  # Runs the window
    app = App()
    app.mainloop()

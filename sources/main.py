import customtkinter as ctk
from pymongo import MongoClient

import env
from addEvent import eventPage
from help import helpPage
from login import loginPage
from report import reportPage
from signup import signUpPage
from student import student

# Database Link
cluster = MongoClient(env.dbLink)
db = cluster["Tokened"]
collection = db["userInfo"]
events = db["events"]


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

        for F in (loginPage, signUpPage, student, eventPage, reportPage, helpPage):  # All pages listed here
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

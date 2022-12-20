import customtkinter as ctk
import re


def show_frame(self):
    from login import loginPage
    frame = self.frames[loginPage]
    # raises the current frame to the top
    frame.tkraise()


high_schools = ["Alonso High School",    "Bloomingdale High School",    "Brandon High School",    "Chamberlain High School",    "East Bay High School",    "Freedom High School",    "Gaither High School",    "Hillsborough High School",    "Jefferson High School",    "King High School",    "Leto High School",    "Middleton High School",    "Newsome High School",    "Plant High School",    "Robinson High School",    "Sickles High School",    "Spoto High School",    "Strawberry Crest High School",    "Tampa Bay Tech High School",    "Wharton High School"]


def createAccount(self, controller):
    from main import collection
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # To check for valid email
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "" or self.conpasswordEntry.get() == "" or self.schoolbox.get() == "schools":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
    if self.passwordEntry.get() != self.conpasswordEntry.get():
        self.errorMessage.configure(text="Error: Passwords Don't Match")
        return
    self.errorMessage.configure(text="")
    if not re.fullmatch(regex, self.emailEntry.get()):
        self.errorMessage.configure(text="Error: Invalid Email")
        return
    email = self.emailEntry.get()
    password = self.conpasswordEntry.get()
    school = self.schoolbox.get()
    self.emailEntry.delete(0, ctk.END)
    self.passwordEntry.delete(0, ctk.END)
    self.conpasswordEntry.delete(0, ctk.END)
    self.schoolbox.set("schools")
    info = {"email": email, "password": password, "school": school}
    collection.insert_one(info)
    show_frame(controller)


class signUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.titleLabel = ctk.CTkLabel(self, text="Tokened")
        self.titleLabel.place(relx=0.47, rely=0.2)

        self.emailEntry = ctk.CTkEntry(self, placeholder_text="email", width=200)
        self.emailEntry.place(relx=0.38, rely=0.28)

        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.passwordEntry.place(relx=0.38, rely=0.38)

        self.conpasswordEntry = ctk.CTkEntry(self, placeholder_text="confirm password", width=200, show="\u2022")
        self.conpasswordEntry.place(relx=0.38, rely=0.48)

        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.4, rely=0.64)

        self.schoolbox = ctk.CTkOptionMenu(self, values=high_schools, width=200, dropdown_fg_color="#343638", bg_color="#343638", fg_color="#343638", button_color="#343638", dynamic_resizing=False)
        self.schoolbox.place(relx=0.38, rely=0.58)
        self.schoolbox.set("schools")

        self.createButton = ctk.CTkButton(self, text="Create", width=190, height=30, command=lambda: createAccount(self, controller))
        self.createButton.place(relx=0.385, rely=0.7)

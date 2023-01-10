import customtkinter as ctk
import re
from PIL import Image
import env


def show_frame(self, controller):
    from login import loginPage
    frame = controller.frames[loginPage]
    # raises the current frame to the top
    frame.tkraise()
    self.fnameEntry.delete(0, ctk.END)
    self.fnameEntry.configure(placeholder_text="first name")
    self.lnameEntry.delete(0, ctk.END)
    self.lnameEntry.configure(placeholder_text="last name")
    self.emailEntry.delete(0, ctk.END)
    self.emailEntry.configure(placeholder_text="email")
    self.passwordEntry.delete(0, ctk.END)
    self.passwordEntry.configure(placeholder_text="password")
    self.conpasswordEntry.delete(0, ctk.END)
    self.conpasswordEntry.configure(placeholder_text="confirm password")
    self.schoolbox.set("school")
    self.gradebox.set("grade")
    self.passwordEntry.configure(show="\u2022")
    self.conpasswordEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")


def createAccount(self, controller):
    from main import collection
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email
    self.errorMessage.place(relx=0.44)
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "" or self.conpasswordEntry.get() == "" or self.schoolbox.get() == "school" or self.fnameEntry.get() == "" or self.lnameEntry.get() == "" or self.gradebox.get() == "grade":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
    if not re.fullmatch(regex, self.emailEntry.get()):
        self.errorMessage.configure(text="Error: Invalid Email")
        return
    if self.passwordEntry.get() != self.conpasswordEntry.get():
        self.errorMessage.configure(text="Error: Passwords Don't Match")
        self.errorMessage.place(relx=0.4)
        self.passwordEntry.delete(0, ctk.END)
        self.conpasswordEntry.delete(0, ctk.END)
        return
    self.errorMessage.configure(text="")
    fName = self.fnameEntry.get()
    lName = self.lnameEntry.get()
    grade = self.gradebox.get()
    email = self.emailEntry.get()
    password = self.conpasswordEntry.get()
    school = self.schoolbox.get()
    if collection.find_one({"email": email}):
        self.errorMessage.configure(text="Error: Email Already Inuse")
        self.errorMessage.place(relx=0.42)
        self.passwordEntry.delete(0, ctk.END)
        self.conpasswordEntry.delete(0, ctk.END)
        return
    self.emailEntry.delete(0, ctk.END)
    self.passwordEntry.delete(0, ctk.END)
    self.conpasswordEntry.delete(0, ctk.END)
    self.schoolbox.set("schools")
    info = {"first_name": fName, "last_name": lName, "grade": grade, "email": email, "password": password, "school": school}
    collection.insert_one(info)
    show_frame(self, controller)


class signUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # self.titleLabel = ctk.CTkLabel(self, text="Tokened")
        # self.titleLabel.place(relx=0.47, rely=0.2)

        self.fnameEntry = ctk.CTkEntry(self, placeholder_text="first name", width=80)
        self.fnameEntry.place(relx=0.38, rely=0.28)

        self.lnameEntry = ctk.CTkEntry(self, placeholder_text="last name", width=100)
        self.lnameEntry.place(relx=0.505, rely=0.28)

        self.gradebox = ctk.CTkOptionMenu(self, values=env.grade, width=200, dropdown_fg_color="#343638",
                                          bg_color="#343638", fg_color="#343638", button_color="#343638",
                                          dynamic_resizing=False, text_color="gray")
        self.gradebox.place(relx=0.38, rely=0.38)
        self.gradebox.set("grade")

        self.emailEntry = ctk.CTkEntry(self, placeholder_text="email", width=200)
        self.emailEntry.place(relx=0.38, rely=0.48)

        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.passwordEntry.place(relx=0.38, rely=0.58)

        self.conpasswordEntry = ctk.CTkEntry(self, placeholder_text="confirm password", width=200, show="\u2022")
        self.conpasswordEntry.place(relx=0.38, rely=0.68)

        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.44, rely=0.84)

        self.schoolbox = ctk.CTkOptionMenu(self, values=env.high_schools, width=200, dropdown_fg_color="#343638",
                                           bg_color="#343638", fg_color="#343638", button_color="#343638",
                                           dynamic_resizing=False, text_color="gray")
        self.schoolbox.place(relx=0.38, rely=0.78)
        self.schoolbox.set("school")

        self.createButton = ctk.CTkButton(self, text="Create", width=190, height=30,
                                          command=lambda: createAccount(self, controller))
        self.createButton.place(relx=0.385, rely=0.9)

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121", command=lambda: show_frame(self, controller))
        self.backButton.place(relx=0, rely=0)

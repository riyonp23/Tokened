import customtkinter as ctk
import re
from PIL import Image
import env


def show_frame(self, controller):
    from login import loginPage
    frame = controller.frames[loginPage]
    # raises the current frame to the top
    frame.tkraise()
    self.emailEntry.delete(0, ctk.END)
    self.passwordEntry.delete(0, ctk.END)
    self.conpasswordEntry.delete(0, ctk.END)
    self.schoolbox.set("school")
    self.passwordEntry.configure(show="\u2022")
    self.conpasswordEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")


def createAccount(self, controller):
    from main import collection
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email
    self.errorMessage.place(relx=0.44)
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "" or self.conpasswordEntry.get() == "" or self.schoolbox.get() == "school":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
    if self.passwordEntry.get() != self.conpasswordEntry.get():
        self.errorMessage.configure(text="Error: Passwords Don't Match")
        self.errorMessage.place(relx=0.4)
        self.passwordEntry.delete(0, ctk.END)
        self.conpasswordEntry.delete(0, ctk.END)
        return
    self.errorMessage.configure(text="")
    if not re.fullmatch(regex, self.emailEntry.get()):
        self.errorMessage.configure(text="Error: Invalid Email")
        return
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
    info = {"email": email, "password": password, "school": school}
    collection.insert_one(info)
    show_frame(self, controller)


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
        self.errorMessage.place(relx=0.44, rely=0.64)

        self.schoolbox = ctk.CTkOptionMenu(self, values=env.high_schools, width=200, dropdown_fg_color="#343638", bg_color="#343638", fg_color="#343638", button_color="#343638", dynamic_resizing=False)
        self.schoolbox.place(relx=0.38, rely=0.58)
        self.schoolbox.set("school")

        self.createButton = ctk.CTkButton(self, text="Create", width=190, height=30, command=lambda: createAccount(self, controller))
        self.createButton.place(relx=0.385, rely=0.7)

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]), size=(25,25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25, hover_color="#212121", command=lambda: show_frame(self, controller))
        self.backButton.place(relx=0, rely=0)

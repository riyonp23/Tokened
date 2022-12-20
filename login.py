import customtkinter as ctk
import re
from signup import signUpPage


def show_frame(self):
    from student import student
    frame = self.frames[student]
    # raises the current frame to the top
    frame.tkraise()


def loginSuccess(self, controller):
    from main import collection
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
    if not re.fullmatch(regex, self.emailEntry.get()):
        self.errorMessage.configure(text="Error: Invalid Email")
        return
    self.errorMessage.configure(text="")
    email = self.emailEntry.get()
    password = self.passwordEntry.get()
    get = {"email": email, "password": password}
    if not collection.find_one(get) is None:
        show_frame(controller)
        return
    else:
        self.errorMessage.configure(text="Error: Email & Password is Incorrect")
        return


class loginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.titleLabel = ctk.CTkLabel(self, text="Tokened")
        self.titleLabel.place(relx=0.47, rely=0.2)

        self.emailEntry = ctk.CTkEntry(self, placeholder_text="email", width=200)
        self.emailEntry.place(relx=0.38, rely=0.38)

        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.passwordEntry.place(relx=0.38, rely=0.48)

        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.385, rely=0.54)

        self.loginButton = ctk.CTkButton(self, text="Login", width=190, height=30, command=lambda: loginSuccess(self, controller))
        self.loginButton.place(relx=0.385, rely=0.6)

        self.signButton = ctk.CTkButton(self, text="Sign Up", width=190, height=30,
                                        command=lambda: controller.show_frame(signUpPage))
        self.signButton.place(relx=0.385, rely=0.7)

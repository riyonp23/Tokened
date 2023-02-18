import re
import secrets
import smtplib
import ssl
import string
from email.message import EmailMessage

import customtkinter as ctk
from PIL import Image

import env
from signup import signUpPage


# Function to switch pages
def show_frame(self, controller, page):
    frame = controller.frames[page]
    frame.tkraise()
    self.emailEntry.delete(0, ctk.END)
    self.passwordEntry.delete(0, ctk.END)
    self.passwordEntry.configure(placeholder_text="password")
    self.passwordEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")


# initializes all variables
first_name = ""
last_name = ""
grade = ""
school = ""
email = ""
password = ""
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email


# allows users to reset password
# composes email to reset
def resetPassword(window):
    from main import student, teacher
    if window.emailEntry.get() == "":
        window.info.configure(text="Error: Enter Email", text_color="red")
        window.info.place(relx=0.37)
        return
    if not re.fullmatch(regex, window.emailEntry.get()):
        window.info.configure(text="Error: Invalid Email", text_color="red")
        window.info.place(relx=0.37)
        return
    window.info.configure(text="ⓘ Enter The Email Associated With Your Account", text_color="white")
    window.info.place(relx=0.15, rely=0.52)
    resemail = window.emailEntry.get()
    get = {"email": resemail}
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd_length = 5
    if not student.find_one(get) is None:
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))
        em = EmailMessage()
        em['From'] = "riyonpraveen23@gmail.com"
        em['To'] = str(resemail)
        em['Subject'] = "Tokened Password Reset"
        content = "Your Temporary Tokened Password Is: " + pwd + "\nMake Sure to Change Your Password From The Settings Tab"
        em.set_content(content)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login("riyonpraveen23@gmail.com", env.emailPass)
            smtp.sendmail("riyonpraveen23@gmail.com", str(resemail), em.as_string())

        student.update_one({"email": resemail}, {"$set": {"password": pwd}})
        window.info.configure(text="ⓘ Sent New Password To " + resemail, text_color="green")
        window.restButton.configure(state="disabled")
        return
    elif not teacher.find_one(get) is None:
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))
        em = EmailMessage()
        em['From'] = "riyonpraveen23@gmail.com"
        em['To'] = str(resemail)
        em['Subject'] = "Tokened Password Reset"
        content = "Your Temporary Tokened Password Is: " + pwd + "\nMake Sure to Change Your Password From The Account Settings Page"
        em.set_content(content)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login("riyonpraveen23@gmail.com", env.emailPass)
            smtp.sendmail("riyonpraveen23@gmail.com", str(resemail), em.as_string())

        teacher.update_one({"email": resemail}, {"$set": {"password": pwd}})
        window.info.configure(text="ⓘ Sent New Password To " + resemail, text_color="green")
        window.restButton.configure(state="disabled")
        return
    else:
        window.info.configure(text="Error: No Email Found", text_color="red")
        window.info.place(relx=0.35)
        return


# creates forgot password window to enter email
def forgotPassword(self):
    window = ctk.CTkToplevel(self)
    window.geometry("400x200")
    window.title("Tokened - Forgot Password")
    window.resizable(False, False)
    window.grab_set()
    window.iconbitmap(env.img[2])

    window.title = ctk.CTkLabel(window, text="Reset Password", font=("courier new", 18)).place(relx=0.31)
    window.info = ctk.CTkLabel(window, text="ⓘ Enter The Email Associated With Your Account", font=("courier new", 12))
    window.info.place(relx=0.13, rely=0.52)
    window.emailEntry = ctk.CTkEntry(window, placeholder_text="email", width=200)
    window.emailEntry.place(relx=0.26, rely=0.4)

    window.restButton = ctk.CTkButton(window, text="Reset", width=190, height=30, command=lambda: resetPassword(window))
    window.restButton.place(relx=0.27, rely=0.68)


# uses email to obtain information for the account
def obtainUserinfo():
    from main import student, teacher
    global first_name, last_name, grade, school, email
    get = {"email": email}
    user = None
    if not student.find_one(get) is None:
        user = student.find_one(get)
    elif not teacher.find_one(get) is None:
        user = teacher.find_one(get)
    first_name = user['first_name']
    last_name = user['last_name']
    grade = user['grade']
    school = user['school']


# Method to make login process and check for valid user information
def loginSuccess(self, controller):
    from main import student, teacher
    from student import studentDashboard, updatelb, updatepoints, updateupcoming, changeText
    from teacher import teacherDashboard, changeTextT, updateeventsT, updateupcomingT
    global email, password
    self.errorMessage.place(relx=0.44)
    # error message if all text fields are not filled
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
    # error message if email is not a valid email
    if not re.fullmatch(regex, self.emailEntry.get()):
        self.passwordEntry.delete(0, ctk.END)
        self.errorMessage.configure(text="Error: Invalid Email")
        return
    self.errorMessage.configure(text="")
    email2 = self.emailEntry.get()
    password2 = self.passwordEntry.get()
    email = str(email2)
    password = str(password2)
    get = {"email": email2, "password": password2}
    # obtains user info if login is successful
    if not student.find_one(get) is None:  # checks if it's a student login
        obtainUserinfo()
        changeText()
        updatelb()
        updatepoints()
        updateupcoming()
        show_frame(self, controller, studentDashboard)
        return
    elif not teacher.find_one(get) is None:  # checks if it's a teacher login
        obtainUserinfo()
        changeTextT()
        updateeventsT()
        updateupcomingT()
        show_frame(self, controller, teacherDashboard)
        return
    # error message if password or email is incorrect
    else:
        self.passwordEntry.delete(0, ctk.END)
        self.errorMessage.configure(text="Error: Email & Password is Incorrect")
        self.errorMessage.place(relx=0.38)
        return


# initializes frame and places widgets on the window
class loginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # displays logo
        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[3]), light_image=Image.open(env.img[3]),
                                      size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0.288, rely=-0.15)

        # places email and password text entry fields
        self.emailEntry = ctk.CTkEntry(self, placeholder_text="email", width=200)
        self.emailEntry.place(relx=0.38, rely=0.38)

        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.passwordEntry.place(relx=0.38, rely=0.48)

        #  places error message
        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.44, rely=0.54)

        # places forgot password button, login button, and sign-up button
        self.forgotPassIcon = ctk.CTkImage(dark_image=Image.open(env.img[1]), light_image=Image.open(env.img[1]),
                                           size=(18, 18))
        self.forgotPassButton = ctk.CTkButton(self, image=self.forgotPassIcon, width=18, height=18, text="",
                                              fg_color="#292929", hover_color="#212121",
                                              command=lambda: forgotPassword(self))
        self.forgotPassButton.place(relx=0.63, rely=0.485)

        self.loginButton = ctk.CTkButton(self, text="Login", width=190, height=30,
                                         command=lambda: loginSuccess(self, controller))
        self.loginButton.place(relx=0.385, rely=0.6)

        self.signButton = ctk.CTkButton(self, text="Sign Up", width=190, height=30,
                                        command=lambda: show_frame(self, controller, signUpPage))
        self.signButton.place(relx=0.385, rely=0.7)

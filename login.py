import customtkinter as ctk
import re
from signup import signUpPage
from PIL import Image
from email.message import EmailMessage
import ssl
import smtplib
import secrets
import string
import env


def show_frame(self, controller, page):
    frame = controller.frames[page]
    # raises the current frame to the top
    frame.tkraise()
    self.emailEntry.delete(0, ctk.END)
    self.emailEntry.configure(placeholder_text="email")
    self.passwordEntry.delete(0, ctk.END)
    self.passwordEntry.configure(placeholder_text="password")
    self.passwordEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")


first_name = ""
last_name = ""
grade = ""
school = ""
email = ""
password = ""
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email


def resetPassword(window):
    from main import collection
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
    if not collection.find_one(get) is None:
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))
        print(pwd)
        em = EmailMessage()
        em['From'] = "riyonpraveen23@gmail.com"
        em['To'] = str(resemail)
        em['Subject'] = "Tokened Password Reset"
        content = "Your Temporary Tokened Password Is: " + pwd + "\nMake Sure to Change Your Password From The Settings Tab"
        em.set_content(content)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login("riyonpraveen23@gmail.com", "hehqoffjbvpusibe")
            smtp.sendmail("riyonpraveen23@gmail.com", str(resemail), em.as_string())

        collection.update_one({"email": resemail}, {"$set": {"password": pwd}})
        window.info.configure(text="ⓘ Sent New Password To " + resemail, text_color="green")
        window.restButton.configure(state="disabled")
        return
    else:
        window.info.configure(text="Error: No Email Found", text_color="red")
        window.info.place(relx=0.35)
        return


def forgotPassword(self):
    window = ctk.CTkToplevel(self)
    window.geometry("400x200")
    window.title("Tokened - Forgot Password")
    window.resizable(False, False)
    window.grab_set()
    window.iconbitmap(env.img[5])

    window.title = ctk.CTkLabel(window, text="Reset Password", font=("Garamond", 20)).place(relx=0.36)
    window.info = ctk.CTkLabel(window, text="ⓘ Enter The Email Associated With Your Account", font=("Garamond", 14))
    window.info.place(relx=0.15, rely=0.52)
    window.emailEntry = ctk.CTkEntry(window, placeholder_text="email", width=200)
    window.emailEntry.place(relx=0.26, rely=0.4)

    window.restButton = ctk.CTkButton(window, text="Reset", width=190, height=30, command=lambda: resetPassword(window))
    window.restButton.place(relx=0.27, rely=0.68)


def obtainUserinfo():
    from main import collection
    from student import changeText
    global first_name, last_name, grade, school, email
    get = {"email": email}
    user = collection.find_one(get)
    first_name = user['first_name']
    last_name = user['last_name']
    grade = user['grade']
    school = user['school']
    changeText()


def loginSuccess(self, controller):
    from main import collection
    from student import student
    global email, password
    self.errorMessage.place(relx=0.44)
    if self.emailEntry.get() == "" or self.passwordEntry.get() == "":
        self.errorMessage.configure(text="Error: Fill All Fields")
        return
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
    if not collection.find_one(get) is None:
        obtainUserinfo()
        show_frame(self, controller, student)
        return
    else:
        self.passwordEntry.delete(0, ctk.END)
        self.errorMessage.configure(text="Error: Email & Password is Incorrect")
        self.errorMessage.place(relx=0.38)
        return


class loginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[6]), light_image=Image.open(env.img[6]), size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0.288, rely=-0.15)

        self.emailEntry = ctk.CTkEntry(self, placeholder_text="email", width=200)
        self.emailEntry.place(relx=0.38, rely=0.38)

        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.passwordEntry.place(relx=0.38, rely=0.48)

        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.44, rely=0.54)

        self.forgotPassIcon = ctk.CTkImage(dark_image=Image.open(env.img[1]), light_image=Image.open(env.img[1]), size=(18, 18))
        self.forgotPassButton = ctk.CTkButton(self, image=self.forgotPassIcon, width=18, height=18, text="", fg_color="#292929", hover_color="#212121", command=lambda: forgotPassword(self))
        self.forgotPassButton.place(relx=0.63, rely=0.485)

        self.loginButton = ctk.CTkButton(self, text="Login", width=190, height=30, command=lambda: loginSuccess(self, controller))
        self.loginButton.place(relx=0.385, rely=0.6)

        self.signButton = ctk.CTkButton(self, text="Sign Up", width=190, height=30,
                                        command=lambda: show_frame(self, controller, signUpPage))
        self.signButton.place(relx=0.385, rely=0.7)


import re

import customtkinter as ctk
from PIL import Image

import env


# function to switch page to login screen and clears all entries
def show_frame(self, controller):
    from login import loginPage
    frame = controller.frames[loginPage]
    # raises the current frame to the top
    frame.tkraise()
    self.fnameEntry.delete(0, ctk.END)
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
    self.gradebox.configure(state="normal")
    self.switchTeacher.deselect()
    self.passwordEntry.configure(show="\u2022")
    self.conpasswordEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")


# function to check if it is a teacher
def checkTeacher(self):
    status = self.switchTeacher.get()
    if status:
        self.errorMessage.configure(text="", text_color="red")
        dialog = ctk.CTkInputDialog(text="Type in 4 Digit Code:",
                                    title="Teacher Confirmation Check")  # Enter combination code
        dialog.iconbitmap(env.img[2])
        code = dialog.get_input()
        if code == "0000":  # code for demo purpose is 0000, in real life situations it would be randomly generated
            if not self.gradebox.get() == "Teacher":
                self.gradebox.set("Teacher")
                self.gradebox.configure(state="disabled")
            self.errorMessage.place(relx=0.46)
            self.errorMessage.configure(text="Success", text_color="green")
            return
        else:
            self.errorMessage.place(relx=0.43)
            self.errorMessage.configure(text="Error: Incorrect Code")
            self.gradebox.set("grade")
            self.gradebox.configure(state="normal")
            self.switchTeacher.deselect()


# function to create new user account and stores it in the database mongoDB
def createAccount(self, controller):
    from main import student, teacher
    from student import updatelb
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # To check for valid email
    self.errorMessage.configure(text_color="red")
    self.errorMessage.place(relx=0.44)
    # Error messages response
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
    fName = self.fnameEntry.get()  # Gets user input from first name box
    lName = self.lnameEntry.get()  # Gets user input from last name box
    grade = self.gradebox.get()  # Gets user input from grade box
    email = self.emailEntry.get()  # Gets user input from email  box
    password = self.conpasswordEntry.get()  # Gets user input from password box
    school = self.schoolbox.get()  # Gets user input from school box
    if student.find_one({"email": email}) or teacher.find_one(
            {"email": email}):  # checks to see if email is already in use in the database
        self.errorMessage.configure(text="Error: Email Already Inuse")
        self.errorMessage.place(relx=0.42)
        self.passwordEntry.delete(0, ctk.END)
        self.conpasswordEntry.delete(0, ctk.END)
        return
    # Clear entries upon completion
    self.emailEntry.delete(0, ctk.END)
    self.passwordEntry.delete(0, ctk.END)
    self.conpasswordEntry.delete(0, ctk.END)
    self.schoolbox.set("schools")
    self.gradebox.set("grade")
    self.switchTeacher.deselect()
    info = {"first_name": fName, "last_name": lName, "grade": grade, "email": email, "password": password,
            "school": school, "points": 0}  # Takes all the info and stores it in a dictionary
    if grade == "Teacher":  # checks to see if it's a teacher or student
        teacher.insert_one(info)  # Inserts the new teacher into the database
    else:
        student.insert_one(info)  # Inserts the new student into the database
    updatelb()
    show_frame(self, controller)  # Switches to login page


# initializes frame and places widgets on the page
class signUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Places logo
        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[3]), light_image=Image.open(env.img[3]),
                                      size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0.288, rely=-0.22)

        # Places sign up entries and dropdowns
        self.fnameEntry = ctk.CTkEntry(self, placeholder_text="first name", width=80)
        self.fnameEntry.place(relx=0.38, rely=0.28)

        self.lnameEntry = ctk.CTkEntry(self, placeholder_text="last name", width=100)
        self.lnameEntry.place(relx=0.505, rely=0.28)

        self.gradebox = ctk.CTkOptionMenu(self, values=env.grades, width=200, dropdown_fg_color="#343638",
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
        self.errorMessage.place(relx=0.44, rely=0.87)

        self.schoolbox = ctk.CTkOptionMenu(self, values=env.high_schools, width=200, dropdown_fg_color="#343638",
                                           bg_color="#343638", fg_color="#343638", button_color="#343638",
                                           dynamic_resizing=False, text_color="gray")
        self.schoolbox.place(relx=0.38, rely=0.78)
        self.schoolbox.set("school")

        self.switchTeacher = ctk.CTkSwitch(master=self, text="Teacher", onvalue=True, offvalue=False,
                                           command=lambda: checkTeacher(self))
        self.switchTeacher.place(relx=0.44, rely=0.84)

        self.createButton = ctk.CTkButton(self, text="Create", width=190, height=30,
                                          command=lambda: createAccount(self, controller))
        self.createButton.place(relx=0.385, rely=0.92)

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121", command=lambda: show_frame(self, controller))
        self.backButton.place(relx=0, rely=0)

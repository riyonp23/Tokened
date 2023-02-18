import customtkinter as ctk
from PIL import Image

import env


def show_frame(self, controller, page):  # used to switch to next frame
    from login import grade
    from student import studentDashboard
    from teacher import teacherDashboard
    if grade == "Teacher" and page == studentDashboard:
        frame = controller.frames[teacherDashboard]
    else:
        frame = controller.frames[page]
    frame.tkraise()
    self.ogpassEntry.delete(0, ctk.END)  # deletes entry
    self.newpassEntry.delete(0, ctk.END)
    self.newconpassEntry.delete(0, ctk.END)
    self.schoolbox.set("school")
    self.gradebox.set("grade")
    self.errorMessage.configure(text="")
    self.errorMessage2.configure(text="")


# function to change password
def changepass(self):
    from main import student, teacher
    from login import email, grade
    self.errorMessage.configure(text_color="red")
    self.errorMessage.configure(font=("", 13))
    if self.ogpassEntry.get() == "" or self.newpassEntry.get() == "" or self.newconpassEntry.get() == "":
        self.errorMessage.place(relx=0.24)
        return self.errorMessage.configure(text="Error: Fill All Fields")
    if self.newpassEntry.get() != self.newconpassEntry.get():
        self.errorMessage.place(relx=0.22)
        return self.errorMessage.configure(text="Error: Passwords Don't Match", font=("", 13))
    if grade == "Teacher":  # Checks if it's a student or teacher
        user = teacher.find_one({"email": email})
    else:
        user = student.find_one({"email": email})
    ogpass = user['password']  # finds the user password from the datebase
    if not self.ogpassEntry.get() == ogpass:
        self.errorMessage.place(relx=0.24)
        return self.errorMessage.configure(text="Error: Invalid Password")
    self.errorMessage.configure(text="Successfully Reset Password", text_color="green", font=("", 13))
    self.errorMessage.place(relx=0.215)
    if grade == "Teacher":  # Checks if it's a student or teacher
        teacher.find_one_and_update({'email': email},
                                    {'$set': {
                                        "password": self.newconpassEntry.get()}})  # sets new password to datebase
    else:
        student.find_one_and_update({'email': email},
                                    {'$set': {
                                        "password": self.newconpassEntry.get()}})  # sets new password to datebase
    self.ogpassEntry.delete(0, ctk.END)  # deletes entry
    self.newpassEntry.delete(0, ctk.END)
    self.newconpassEntry.delete(0, ctk.END)


# allows user to change their grade and/or school
def changeschoolgrade(self):
    from main import student, teacher
    import login
    userschool = None
    usergrade = None
    self.errorMessage2.configure(text_color="red")
    self.errorMessage2.place(relx=0.56, rely=0.56)
    if self.schoolbox.get() == "school" and self.gradebox.get() == "grade":
        return self.errorMessage2.configure(text="Error: Please Fill One of the Options", text_color="red")
    if not self.schoolbox.get() == "school":  # Checking to see which option they picked
        userschool = self.schoolbox.get()
    if not self.gradebox.get() == "grade":
        usergrade = self.gradebox.get()
    if usergrade is not None:
        if login.grade == "Teacher":  # Teachers can't switch grades error
            self.gradebox.set("grade")
            self.schoolbox.set("school")
            return self.errorMessage2.configure(text="Error: Teachers Can't Switch Their Grades")
        student.find_one_and_update({'email': login.email},
                                    {'$set': {'grade': usergrade}})  # switches student grades & updates in database
        login.grade = usergrade
    if userschool is not None:
        if login.grade == "Teacher":
            teacher.find_one_and_update({'email': login.email}, {
                '$set': {'school': userschool}})  # switches teacher school & updates in database
        else:
            student.find_one_and_update({'email': login.email}, {
                '$set': {'school': userschool}})  # switches student school & updates in database
        login.school = userschool
    self.errorMessage2.place(relx=0.6)
    self.errorMessage2.configure(text="Successfully Updated", text_color="green")
    self.schoolbox.set("school")
    self.gradebox.set("grade")


# initializes frame for help page and places widgets
class accountPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import studentDashboard, menuOpen, logout
        from help import helpPage

        # title label
        self.titleLabel = ctk.CTkLabel(self, text="Tokened - Account Settings", font=("courier new", 30))
        self.titleLabel.place(relx=0.22, rely=0.05)

        # change password labels, buttons, and entries placed
        self.changeLabel = ctk.CTkLabel(self, text="Change Password", font=("courier new", 20))
        self.changeLabel.place(relx=0.16, rely=0.2)

        self.ogpassEntry = ctk.CTkEntry(self, placeholder_text="password", width=200, show="\u2022")
        self.ogpassEntry.place(relx=0.18, rely=0.3)

        self.newpassEntry = ctk.CTkEntry(self, placeholder_text="new password", width=200, show="\u2022")
        self.newpassEntry.place(relx=0.18, rely=0.4)

        self.newconpassEntry = ctk.CTkEntry(self, placeholder_text="confirm password", width=200,
                                            show="\u2022")
        self.newconpassEntry.place(relx=0.18, rely=0.5)

        self.errorMessage = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage.place(relx=0.18, rely=0.56)

        self.updatepasButton = ctk.CTkButton(self, text="Update", width=200, height=30,
                                             command=lambda: changepass(self))
        self.updatepasButton.place(relx=0.18, rely=0.61)

        # change school and/or grade label
        self.change2Label = ctk.CTkLabel(self, text="Change Information", font=("courier new", 20))
        self.change2Label.place(relx=0.53, rely=0.2)

        # places drop down menus for school and grade
        self.schoolbox = ctk.CTkOptionMenu(self, values=env.high_schools, width=200, dropdown_fg_color="#343638",
                                           bg_color="#343638", fg_color="#343638", button_color="#343638",
                                           dynamic_resizing=False, text_color="gray")
        self.schoolbox.place(relx=0.56, rely=0.3)
        self.schoolbox.set("school")

        self.gradebox = ctk.CTkOptionMenu(self, values=["9", "10", "11", "12"], width=200, dropdown_fg_color="#343638",
                                          bg_color="#343638", fg_color="#343638", button_color="#343638",
                                          dynamic_resizing=False, text_color="gray")
        self.gradebox.place(relx=0.56, rely=0.45)
        self.gradebox.set("grade")

        # places error message
        self.errorMessage2 = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage2.place(relx=0.56, rely=0.56)

        # places update button for updating grade and school
        self.updateboxButton = ctk.CTkButton(self, text="Update", width=200, height=30,
                                             command=lambda: changeschoolgrade(self))
        self.updateboxButton.place(relx=0.56, rely=0.61)

        # places author label
        self.authorLabel = ctk.CTkLabel(self, text="Riyon Praveen, Ignatius Martin, & Anay Patel © FBLA 2023",
                                        font=("courier new", 14))
        self.authorLabel.place(relx=0.23, rely=0.955)

        # places back button
        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121",
                                        command=lambda: show_frame(self, controller, studentDashboard))
        self.backButton.place(relx=0, rely=0)

        # initializes settings menu frame
        self.settingFrame = ctk.CTkCanvas(self, width=100, height=500, background="#212121", highlightthickness=0,
                                          borderwidth=0)

        # places menu button
        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        bg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self, True))
        self.menuButton.place(relx=0.95, rely=0)

        # places account settings button

        self.accountImage = ctk.CTkImage(dark_image=Image.open(env.img[12]), light_image=Image.open(env.img[12]),
                                         size=(29, 29))
        self.accountButton = ctk.CTkButton(self.settingFrame, image=self.accountImage, text="", width=25, height=25,
                                           fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                           command=lambda: show_frame(self, controller, accountPage))
        self.accountButton.place(relx=-0.015, rely=0.765)

        # places help button
        self.helpImage = ctk.CTkImage(dark_image=Image.open(env.img[11]), light_image=Image.open(env.img[11]),
                                      size=(28, 28))
        self.helpButton = ctk.CTkButton(self.settingFrame, image=self.helpImage, text="", width=25, height=25,
                                        fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                        command=lambda: show_frame(self, controller, helpPage))
        self.helpButton.place(relx=-0.015, rely=0.84)

        # places log out button
        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]),
                                        size=(37, 37))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=50,
                                          fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                          command=lambda: logout(self, controller, False))
        self.logoutButton.place(relx=-0.04, rely=0.91)

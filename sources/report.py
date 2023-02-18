import os
import random

import customtkinter as ctk
from PIL import Image

import env
from account import accountPage
from help import helpPage
from student import menuOpen, logout


def show_frame(self, controller, page):  # used to switch to next frame
    from student import menuClose
    from login import grade
    from student import studentDashboard
    from teacher import teacherDashboard
    if grade == "Teacher" and page == studentDashboard:
        frame = controller.frames[teacherDashboard]
    else:
        frame = controller.frames[page]
    # raises the current frame to the top
    frame.tkraise()
    menuClose(self, True)


# Initializes variable
topNameLabel = None
randNameLabel = None
rewardLabel = None
titleLabel = None
nameLabel = None
gradeLabel = None
upointLabel = None
classposLabel = None
bd = None
report = None


# Calculates the winners
def winners():
    from main import student
    from login import school
    global topNameLabel, randNameLabel, pointsLabel, rewardLabel
    sorted_data = student.find({'school': school}).sort(
        [("points", -1)])  # sorts database based on points in descending order
    data_array = list(sorted_data)  # turns sorted data into a list and assigns it to a variable

    topFirstName = str(data_array[0]["first_name"])  # Fetches first name of student with most points
    topLastName = str(data_array[0]["last_name"])  # Fetches last name of student with most points
    topPoints = str(data_array[0]["points"])  # Fetch points of student with most points

    # variable that contains the text to print full name of student with most points
    topName = "Most Points: " + topFirstName + " " + topLastName
    numItems = student.count_documents({'school': school})  # determines number of students in database
    randomRange = random.randint(0, numItems - 1)  # sets range of random numbers to include all students
    randomStudent = student.find({'school': school}).skip(randomRange).limit(1)[0]  # selects random student

    # formats random winner to printable format
    randStudentName = "Random Winner: " + randomStudent["first_name"] + " " + randomStudent["last_name"]
    # Set rewards depending on how many points a student has
    rewards = {0: "No Reward",
               200: "No Reward",
               400: "One Tardy Pass",
               1000: "Free Lunch for One Day",
               1600: "School Lanyard",
               1800: "School T-Shirt",
               2000: "School Hoodie",
               }
    schoolRewards = ["School T-shirt", "School Hoodie", "School Water Bottle", "School Pencil Case", "School Lanyard",
                     "School Keychain", "School Sticker"]
    randomRange2 = random.randint(0, len(schoolRewards) - 1)
    points = randomStudent['points']  # assigns amount of points a student has to a variable
    reward = "No Reward"  # sets default value to print "No Reward"
    for key in sorted(rewards.keys(), reverse=True):  # For every number in sorted rewards dictionary
        #  if the student has more points than the key value that the  loop is on, then assign that reward
        if points >= key:
            reward = rewards[key]
            break  # ends loop if reward has been assigned
    topNameLabel.configure(text=topName + "(School Backpack)")
    randNameLabel.configure(text=randStudentName + "(" + schoolRewards[randomRange2] + ")")
    rewardLabel.configure(text="Reward: " + reward)


# creates function for text file to show name and points for all students
def reportAll():
    from main import student, events
    from login import school
    reportName = []
    reportGrade = []
    reportPoint = []
    reportEventname = []
    reportEventdate = []
    for i in student.find({'school': school}).sort('points', -1):
        reportName.append(str(i['first_name'] + " " + i["last_name"]))
        reportGrade.append(i['grade'])
        reportPoint.append(str(i['points']))
    for i in events.find({'school': school}).sort('sortdate', 1):
        reportEventname.append(i['event'])
        reportEventdate.append(i['date'])
    path = "./assets/"

    with open(os.path.join(path, 'report.txt'), 'w') as f:
        f.write("Students - " + school + "\n\n")
        for i in range(len(reportName)):  # Writes information on all students in the same school
            f.write(
                "Name: " + reportName[i] + "\n" + " Grade: " + reportGrade[i] + "th" + "\n" + " Points: " + reportPoint[
                    i] + "\n\n")
        f.write("All Events - " + school + "\n\n")
        for i in range(len(reportEventname)):  # Writes information on all events in the same school
            f.write(
                "Event: " + reportEventname[i] + "\n" + " Date: " + reportEventdate[i] + "\n\n"
            )

    if os.path.exists(os.path.join(path, 'report.txt')):
        os.startfile(".\\assets\\report.txt")
    else:
        pass


# creates function to show the position of the student within his school
def updateUserinfo(teacher):
    from main import student
    from login import email, first_name, last_name, grade, school
    global titleLabel, nameLabel, gradeLabel, upointLabel, classposLabel, bd, topNameLabel, randNameLabel, rewardLabel, report
    titleLabel.configure(text="Quarter Report - " + school)
    if teacher:
        bd.place(relx=1)
        topNameLabel.place(relx=0.1, rely=0.23)
        randNameLabel.place(relx=0.1, rely=0.33)
        rewardLabel.place(relx=0.1, rely=0.42)
        report.place(relx=0.1, rely=0.5)
        return
    topNameLabel.place(relx=1)
    randNameLabel.place(relx=1)
    rewardLabel.place(relx=1)
    report.place(relx=1)
    bd.place(relx=0.28, rely=0.12)
    nameLabel.configure(text="Name: " + first_name + " " + last_name)
    gradeLabel.configure(text="Grade: " + grade + "th")
    user = student.find_one({'email': email})
    points = str(user['points'])
    upointLabel.configure(text="Points: " + points)
    studentName = []
    for i in student.find({'school': school}).sort('points', -1):
        studentName.append(i['first_name'])
    pos = studentName.index(first_name) + 1
    classposLabel.configure(text="Class Position: " + str(pos) + " out of " + str(len(studentName)))


# initializes frame for help page and places widgets
class reportPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import studentDashboard
        global topNameLabel, randNameLabel, rewardLabel, titleLabel, nameLabel, gradeLabel, upointLabel, classposLabel, bd, report

        # Title of the page
        titleLabel = ctk.CTkLabel(self, text="Quarter Report", font=("courier new", 25))
        titleLabel.place(relx=0.1, rely=0.03)

        bd = ctk.CTkFrame(self, width=400, height=200, bg_color="transparent", fg_color="transparent",
                          border_width=2, border_color="#212121")
        bd.place(relx=0.28, rely=0.12)

        self.bdtitle = ctk.CTkLabel(bd, text="Student Report", font=("courier new", 22))
        self.bdtitle.place(relx=0.27, rely=0.05)

        # places name, grade, points, and class position

        nameLabel = ctk.CTkLabel(bd, text="Name:", font=("courier new", 20))
        nameLabel.place(relx=0.05, rely=0.2)
        gradeLabel = ctk.CTkLabel(bd, text="Grade:", font=("courier new", 20))
        gradeLabel.place(relx=0.05, rely=0.4)
        upointLabel = ctk.CTkLabel(bd, text="Points:", font=("courier new", 20))
        upointLabel.place(relx=0.05, rely=0.6)
        classposLabel = ctk.CTkLabel(bd, text="Class Position:", font=("courier new", 20))
        classposLabel.place(relx=0.05, rely=0.8)

        # Displays the student with the most points and their reward
        topNameLabel = ctk.CTkLabel(self, text="Riyon Praveen" + " (Gift Basket)", font=("courier new", 20))
        topNameLabel.place(relx=0.1, rely=0.55)

        # Displays the student that was chosen randomly and their reward
        randNameLabel = ctk.CTkLabel(self, text="Ignatius Martin" + " (School Hoodie)", font=("courier new", 20))
        randNameLabel.place(relx=0.1, rely=0.65)

        # Displays the reward that the student recieved for their number of points
        rewardLabel = ctk.CTkLabel(self, text="Reward: " + "One Tardy Pass", font=("courier new", 20))
        rewardLabel.place(relx=0.1, rely=0.75)

        report = ctk.CTkLabel(self, text="View Reports of All", font=("courier new", 20), text_color="#1b70cf",
                              cursor="hand2")
        report.place(relx=0.1, rely=0.83)
        report.bind("<Button-1>", lambda e: reportAll())

        # places back button to return to dashboard
        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121",
                                        command=lambda: show_frame(self, controller, studentDashboard))
        self.backButton.place(relx=0, rely=0)

        # places author label
        self.authorLabel = ctk.CTkLabel(self, text="Riyon Praveen, Ignatius Martin, & Anay Patel © FBLA 2023",
                                        font=("courier new", 14))
        self.authorLabel.place(relx=0.23, rely=0.955)

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

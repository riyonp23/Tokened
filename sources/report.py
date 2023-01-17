import customtkinter as ctk
import random
from PIL import Image
import env
import os
from student import menuOpen, changepass, logout
from help import helpPage


def show_frame(self, controller, page):  # used to switch to next frame
    from student import menuClose
    frame = controller.frames[page]
    # raises the current frame to the top
    frame.tkraise()
    menuClose(self, True)


topNameLabel = None
randNameLabel = None
rewardLabel = None
titleLabel = None
nameLabel = None
gradeLabel = None
upointLabel = None
classposLabel = None


def winners():
    from main import collection
    from login import school
    global topNameLabel, randNameLabel, pointsLabel, rewardLabel
    sorted_data = collection.find({'school': school}).sort(
        [("points", -1)])  # sorts database based on points in descending order
    data_array = list(sorted_data)  # turns sorted data into a list and assigns it to a variable

    topFirstName = str(data_array[0]["first_name"])  # Fetches first name of student with most points
    topLastName = str(data_array[0]["last_name"])  # Fetches last name of student with most points
    topPoints = str(data_array[0]["points"])  # Fetch points of student with most points

    # variable that contains the text to print full name of student with most points
    topName = "Most Points: " + topFirstName + " " + topLastName
    numItems = collection.count_documents({'school': school})  # determines number of students in database
    randomRange = random.randint(0, numItems - 1)  # sets range of random numbers to include all students
    randomStudent = collection.find({'school': school}).skip(randomRange).limit(1)[0]  # selects random student

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


def reportAll():
    from main import collection
    from login import school
    reportName = []
    reportGrade = []
    reportPoint = []
    for i in collection.find({'school': school}).sort('points', -1):
        reportName.append(str(i['first_name'] + " " + i["last_name"]))
        reportGrade.append(i['grade'])
        reportPoint.append(str(i['points']))
    path = "./assets/"

    with open(os.path.join(path, 'report.txt'), 'w') as f:
        for i in range(len(reportName)):
            f.write(
                "Name: " + reportName[i] + "\n" + " Grade: " + reportGrade[i] + "th" + "\n" + " Points: " + reportPoint[
                    i] + "\n\n")

    if os.path.exists(os.path.join(path, 'report.txt')):
        os.startfile(".\\assets\\report.txt")
    else:
        pass


def updateUserinfo():
    from main import collection
    from login import email, first_name, last_name, grade, school
    global titleLabel, nameLabel, gradeLabel, upointLabel, classposLabel
    titleLabel.configure(text="Quarter Report - " + school)
    nameLabel.configure(text="Name: " + first_name + " " + last_name)
    gradeLabel.configure(text="Grade: " + grade + "th")
    user = collection.find_one({'email': email})
    points = str(user['points'])
    upointLabel.configure(text="Points: " + points)
    studentName = []
    for i in collection.find({'school': school}).sort('points', -1):
        studentName.append(i['first_name'])
    pos = studentName.index(first_name) + 1
    classposLabel.configure(text="Class Position: " + str(pos) + " out of " + str(len(studentName)))


class reportPage(ctk.CTkFrame):  # sets frame for report page
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import student
        global topNameLabel, randNameLabel, rewardLabel, titleLabel, nameLabel, gradeLabel, upointLabel, classposLabel

        # Title of the page
        titleLabel = ctk.CTkLabel(self, text="Quarter Report", font=("courier new", 25))
        titleLabel.place(relx=0.1, rely=0.03)

        self.bd = ctk.CTkFrame(self, width=400, height=200, bg_color="transparent", fg_color="transparent",
                               border_width=2, border_color="#212121")
        self.bd.place(relx=0.28, rely=0.12)

        self.bdtitle = ctk.CTkLabel(self.bd, text="Student Report", font=("courier new", 22))
        self.bdtitle.place(relx=0.27, rely=0.05)

        nameLabel = ctk.CTkLabel(self.bd, text="Name:", font=("courier new", 20))
        nameLabel.place(relx=0.05, rely=0.2)
        gradeLabel = ctk.CTkLabel(self.bd, text="Grade:", font=("courier new", 20))
        gradeLabel.place(relx=0.05, rely=0.4)
        upointLabel = ctk.CTkLabel(self.bd, text="Points:", font=("courier new", 20))
        upointLabel.place(relx=0.05, rely=0.6)
        classposLabel = ctk.CTkLabel(self.bd, text="Class Position:", font=("courier new", 20))
        classposLabel.place(relx=0.05, rely=0.8)

        alignx = 0.1  # same x-value for all labels so they all align

        # Displays the student with the most points and their reward
        topNameLabel = ctk.CTkLabel(self, text="Riyon Praveen" + " (Gift Basket)", font=("courier new", 20))
        topNameLabel.place(relx=alignx, rely=0.55)

        # Displays the student that was chosen randomly and their reward
        randNameLabel = ctk.CTkLabel(self, text="Ignatius Martin" + " (School Hoodie)", font=("courier new", 20))
        randNameLabel.place(relx=alignx, rely=0.65)

        # Displays the reward that the student recieved for their number of points
        rewardLabel = ctk.CTkLabel(self, text="Reward: " + "One Tardy Pass", font=("courier new", 20))
        rewardLabel.place(relx=alignx, rely=0.75)

        self.report = ctk.CTkLabel(self, text="View Reports of All", font=("courier new", 20), text_color="#1b70cf",
                                   cursor="hand2")
        self.report.place(relx=alignx, rely=0.83)
        self.report.bind("<Button-1>", lambda e: reportAll())

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121", command=lambda: show_frame(self, controller, student))
        self.backButton.place(relx=0, rely=0)
        # runs function
        self.settingFrame = ctk.CTkCanvas(self, width=160, height=500, background="#212121", highlightthickness=0,
                                          borderwidth=0)

        self.labeltest = ctk.CTkLabel(self.settingFrame, text="Settings", font=("courier new", 15))
        self.labeltest.place(relx=0.24, rely=0.12)

        self.ogpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="password", width=100, show="\u2022")
        self.ogpassEntry.place(relx=0.16, rely=0.2)

        self.newpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="new password", width=100, show="\u2022")
        self.newpassEntry.place(relx=0.16, rely=0.3)

        self.newconpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="confirm password", width=100,
                                            show="\u2022")
        self.newconpassEntry.place(relx=0.16, rely=0.4)

        self.errorMessage = ctk.CTkLabel(self.settingFrame, text="", text_color="red")
        self.errorMessage.place(relx=0.16, rely=0.46)

        self.saveButton = ctk.CTkButton(self.settingFrame, text="Save", width=40, height=10, fg_color="#212121",
                                        bg_color="#212121", hover_color="#292929", command=lambda: changepass(self))
        self.saveButton.place(relx=0.34, rely=0.52)

        self.helpImage = ctk.CTkImage(dark_image=Image.open(env.img[11]), light_image=Image.open(env.img[11]),
                                      size=(20, 20))
        self.helpButton = ctk.CTkButton(self.settingFrame, image=self.helpImage, text="", width=25, height=25,
                                        fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                        command=lambda: show_frame(self, controller, helpPage))
        self.helpButton.place(relx=0.79, rely=0.87)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        bg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self, True))
        self.menuButton.place(relx=0.95, rely=0)

        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]),
                                        size=(25, 25))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=25,
                                          fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                          command=lambda: logout(self, controller, True))
        self.logoutButton.place(relx=0.78, rely=0.93)

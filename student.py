import customtkinter as ctk
from PIL import Image
import env

#finish upcoming events at the bottom
#make menu look better
#add help button to menu
#add help screen
#select random winner


def show_frame(self, controller, page):
    frame = controller.frames[page]
    # raises the current frame to the top
    frame.tkraise()


welcomeLabel = None


def changeText():
    from login import first_name
    global welcomeLabel
    welcomeLabel.configure(text="Welcome, " + first_name)


def toaddEvents(self, controller):
    from addEvent import eventPage, updateevents
    updateevents()
    show_frame(self, controller, eventPage)


frame = None
pointsLabel = None
pointsFrame = None
num_holder = {}
name_holder = {}
grade_holder = {}
points_holder = {}


def updatelb():
    from main import collection
    from login import school
    global frame, num_holder, name_holder, grade_holder, points_holder
    lbStudentName = []
    lbStudentGrade = []
    lbStudentPoints = []
    for i in collection.find({'school': school}).sort('points', -1):  # add school filter
        lbStudentName.append(str(i['first_name'] + " " + i["last_name"]))
        lbStudentGrade.append(str(i["grade"]))
        lbStudentPoints.append(str(i["points"]))

    lenevent = 0
    if len(lbStudentName) < 5:
        lenevent = len(lbStudentName)
    else:
        lenevent = 5
    counter = 0.3
    for i in range(lenevent):
        if len(num_holder) > 0:
            num_holder['num' + str(i)].destroy()
            name_holder['name' + str(i)].destroy()
            grade_holder['grade' + str(i)].destroy()
            points_holder['pointsum' + str(i)].destroy()
    for i in range(lenevent):
        num_holder['num' + str(i)] = ctk.CTkLabel(frame, text=str(i + 1) + '.')
        num_holder['num' + str(i)].place(relx=0.4, rely=counter)
        name_holder['name' + str(i)] = ctk.CTkLabel(frame, text=lbStudentName[i])
        name_holder['name' + str(i)].place(relx=0.45, rely=counter)
        grade_holder["grade" + str(i)] = ctk.CTkLabel(frame, text=lbStudentGrade[i])
        grade_holder["grade" + str(i)].place(relx=0.7, rely=counter)
        points_holder["pointsum" + str(i)] = ctk.CTkLabel(frame, text=lbStudentPoints[i])
        points_holder["pointsum" + str(i)].place(relx=0.875,rely=counter)
        counter = counter + 0.09


def updatepoints():
    from main import collection
    from login import email
    global pointsLabel, pointsFrame
    user = collection.find_one({'email': email})
    points = user['points']
    if points >= 1000:
        pointsFrame.configure(width=105)
    elif points >= 100:
        pointsFrame.configure(width=80)
    elif points == 0:
        pointsFrame.configure(width=55)
    pointsLabel.configure(text=points)


def changepass(self):
    from main import collection
    from login import email
    self.errorMessage.configure(text_color="red")
    if self.ogpassEntry.get() == "" or self.newpassEntry.get() == "" or self.newconpassEntry.get() == "":
        self.errorMessage.place(relx=0.16)
        return self.errorMessage.configure(text="Error: Fill All Fields")
    if self.newpassEntry.get() != self.newconpassEntry.get():
        self.errorMessage.place(relx=0)
        return self.errorMessage.configure(text="Error: Passwords Don't Match", font=("", 11))
    user = collection.find_one({"email": email})
    ogpass = user['password']
    if not self.ogpassEntry.get() == ogpass:
        self.errorMessage.place(relx=0.07)
        return self.errorMessage.configure(text="Error: Invalid Password")
    self.errorMessage.configure(text="Successfully Reset Password", text_color="green", font=("", 11))
    self.errorMessage.place(relx=0)
    collection.find_one_and_update({'email': email}, {'$set': {"password": self.newconpassEntry.get()}})
    self.ogpassEntry.delete(0, ctk.END)
    self.newpassEntry.delete(0, ctk.END)
    self.newconpassEntry.delete(0, ctk.END)


def logout(self, controller, para1):
    from login import loginPage
    show_frame(self, controller, loginPage)
    menuClose(self, para1)


openm = False


def menuOpen(self, para1):
    global openm
    if not openm:
        self.settingFrame.place(relx=0.8)
        if para1:
            self.menuButton.configure(fg_color="#212121", hover_color="#292929", bg_color="#212121")
            self.logoutButton.configure(fg_color="#212121", hover_color="#292929", bg_color="#212121")
        else:
            self.menuButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
            self.logoutButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
        openm = True
        return
    else:
        menuClose(self, para1)
        openm = False
        return


def menuClose(self, para1):
    self.settingFrame.place(relx=1)
    self.ogpassEntry.delete(0, ctk.END)
    self.ogpassEntry.configure(show="\u2022")
    self.newpassEntry.delete(0, ctk.END)
    self.newpassEntry.configure(placeholder_text="new password")
    self.newpassEntry.configure(show="\u2022")
    self.newconpassEntry.delete(0, ctk.END)
    self.newconpassEntry.configure(placeholder_text="confirm password")
    self.newconpassEntry.configure(show="\u2022")
    self.errorMessage.configure(text="")
    if para1:
        self.menuButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
        self.logoutButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
    else:
        self.menuButton.configure(fg_color="#212121", hover_color="#292929", bg_color="#212121")
        self.logoutButton.configure(fg_color="#212121", hover_color="2929292", bg_color="#212121")


class student(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global welcomeLabel, frame, pointsLabel, pointsFrame
        ctk.CTkFrame.__init__(self, parent)
        frame = ctk.CTkFrame(self, width=800, height=500, fg_color="transparent")
        frame.place(relx=0, rely=0)

        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[3]), light_image=Image.open(env.img[3]),
                                      size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0, rely=-0.05)

        welcomeLabel = ctk.CTkLabel(self, text="Welcome, Iggy", font=("courier new", 26))
        welcomeLabel.place(relx=0.055, rely=0.025)

        pointsFrame = ctk.CTkFrame(self, width=80, height=37, fg_color="transparent", border_color="#212121",
                                        border_width=2)
        pointsFrame.place(relx=0.809)
        #80 #105

        self.pointsImage = ctk.CTkImage(dark_image=Image.open(env.img[8]), light_image=Image.open(env.img[8]), size=(30,30))
        self.pointsImageL = ctk.CTkLabel(self, image=self.pointsImage, text="")
        self.pointsImageL.place(relx=0.81, rely=0.005)

        pointsLabel = ctk.CTkLabel(self, text="0", font=("courier new", 25))
        pointsLabel.place(relx=0.85, rely=0.0099)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[7]),
                                      light_image=Image.open(env.img[7]), size=(75, 75))
        self.eventsButton = ctk.CTkButton(self, image=self.plusImage, text="Events", width=15, height=50,
                                          fg_color="#292929",
                                          hover_color="#212121", font=("courier new", 24), border_width=2,
                                          border_spacing=20, border_color="#212121", command=lambda: toaddEvents(self, controller))
        self.eventsButton.place(relx=0.085, rely=0.45)

        self.lbTitle = ctk.CTkLabel(self, text="Leaderboard", font=("Courier New", 28)).place(relx=0.55, rely=0.1)

        self.lbHeadings = ctk.CTkLabel(self, text="Name\t" + "      " + "Grade" + "    " + "Points",
                                       font=("courier new", 22))
        self.lbHeadings.place(relx=0.45, rely=0.2)

        upcomingEvents = ctk.CTkFrame(self, width=800, height=125, corner_radius=10, bg_color="#363636",
                                      fg_color="#363636")
        upcomingEvents.place(relx=0, y=375)

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
                                        bg_color="#212121", hover_color="#212121", command=lambda: changepass(self))
        self.saveButton.place(relx=0.34, rely=0.52)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self, True))
        self.menuButton.place(relx=0.95, rely=0)

        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]),
                                        size=(25, 25))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=25,
                                          fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                          command=lambda: logout(self, controller, True))
        self.logoutButton.place(relx=0.78, rely=0.93)

from datetime import datetime, date

import customtkinter as ctk
from PIL import Image

import env
from account import accountPage
from help import helpPage


# function to switch pages
def show_frame(self, controller, page):
    frame = controller.frames[page]
    menuClose(self, True)
    frame.tkraise()


# function to change welcome label to the student's first name
def changeText():
    from login import first_name
    global welcomeLabel
    welcomeLabel.configure(text="Welcome, " + first_name)


# function to switch to event page
def toaddEvents(self, controller):
    from addEvent import eventPage, updateevents, eventdropdown, updateeventdropdown
    updateevents()
    eventdropdown()
    updateeventdropdown()
    show_frame(self, controller, eventPage)


# initializing variables to be used later
frame = None
pointsLabel = None
welcomeLabel = None
pointsFrame = None
upcomingEventsFrame = None
errorImage = None
openm = False
name_holder = {}
grade_holder = {}
points_holder = {}
eventbd_holder = {}
event_holder = {}
eventdate_holder = {}


# function to update the leaderboard
def updatelb():
    from main import student
    from login import school
    global frame, name_holder, grade_holder, points_holder
    lbStudentName = []  # initializes list for student names
    lbStudentGrade = []  # initializes list for student grades
    lbStudentPoints = []  # initializes list for student points
    for i in student.find({'school': school}).sort('points',
                                                   -1):  # sorts all the students in the same school by points
        # Adds the items to list
        lbStudentName.append(str(i['first_name'] + " " + i["last_name"]))
        lbStudentGrade.append(str(i["grade"]))
        lbStudentPoints.append(str(i["points"]))

    #
    lenevent = 0
    if len(lbStudentName) < 5:
        lenevent = len(lbStudentName)
    else:
        lenevent = 5
    counter = 0.3
    for i in range(len(name_holder)):  # if the name,grade, or email is already created, deletes it
        if len(name_holder) > 0:
            name_holder['name' + str(i)].destroy()
            grade_holder['grade' + str(i)].destroy()
            points_holder['pointsum' + str(i)].destroy()
    for i in range(lenevent):  # creates the labels for every student in the lists
        name_holder['name' + str(i)] = ctk.CTkLabel(frame, text=lbStudentName[i])
        name_holder['name' + str(i)].place(relx=0.45, rely=counter)
        grade_holder["grade" + str(i)] = ctk.CTkLabel(frame, text=lbStudentGrade[i])
        grade_holder["grade" + str(i)].place(relx=0.7, rely=counter)
        points_holder["pointsum" + str(i)] = ctk.CTkLabel(frame, text=lbStudentPoints[i])
        points_holder["pointsum" + str(i)].place(x=680, rely=counter)
        counter = counter + 0.08


# function to update the upcoming events
def updateupcoming():
    from main import events
    from login import school
    global upcomingEventsFrame, event_holder, eventdate_holder, eventbd_holder, errorImage
    eventname = []  # initializes list for event name
    eventdate = []  # initializes list for event date
    for i in events.find({'school': school}).sort('sortdate', 1):  # sorts all events by date
        eventname.append(i['event'])
        eventdate.append(i['date'])
    currentdate = date.today().strftime("%m/%d/%Y")  # gets today's date
    eventdate.append(currentdate)
    eventdate.sort(key=lambda date: datetime.strptime(date, "%m/%d/%Y"), reverse=False)  # resorts the dates
    index = eventdate.index(currentdate)
    eventname.insert(index, 'space')
    for i in reversed(range(len(eventdate))):
        if index > i:
            del eventdate[i]
    for i in reversed(range(len(eventname))):
        if index > i:
            del eventname[i]
    eventdate.remove(currentdate)  # Removes today's date
    eventname.remove('space')
    lenevent = 0
    if len(eventdate) < 3:
        lenevent = len(eventdate)
    else:
        lenevent = 3
    counter = 0.08
    counter2 = 0.23
    for i in range(len(event_holder)):  # if the event name,event date, or border is already created, deletes it
        if len(event_holder) > 0:
            event_holder['event' + str(i)].destroy()
            eventdate_holder['date' + str(i)].destroy()
            eventbd_holder['bd' + str(i)].destroy()
    if lenevent == 0:  # if there is no upcoming events
        for i in range(3):  # creates upcoming events
            eventbd_holder['bd' + str(i)] = ctk.CTkFrame(upcomingEventsFrame, width=200, height=90,
                                                         bg_color="transparent", fg_color="transparent", border_width=2,
                                                         border_color="#292929")
            eventbd_holder['bd' + str(i)].place(relx=counter, rely=0.3)
            event_holder['event' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], image=errorImage, text="",
                                                          font=("Courier New", 12), bg_color="transparent",
                                                          fg_color="transparent")
            event_holder['event' + str(i)].place(x=60, rely=0.07)
            eventdate_holder['date' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], image=errorImage, text="",
                                                             font=("Courier New", 14), bg_color="transparent",
                                                             fg_color="transparent")
            eventdate_holder['date' + str(i)].place(relx=1)
            counter = counter + 0.3
        return
    for i in range(lenevent):  # creates upcoming events
        eventbd_holder['bd' + str(i)] = ctk.CTkFrame(upcomingEventsFrame, width=200, height=90, bg_color="transparent",
                                                     fg_color="transparent", border_width=2, border_color="#292929")
        eventbd_holder['bd' + str(i)].place(relx=counter, rely=0.3)
        event_holder['event' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], text=eventname[i],
                                                      font=("Courier New", 12), bg_color="transparent",
                                                      fg_color="transparent")
        if len(eventname[i]) >= 20:
            event_holder['event' + str(i)].place(x=12, rely=0.02)
        elif len(eventname[i]) >= 16:
            event_holder['event' + str(i)].place(relx=0.2, rely=0.02)
        else:
            event_holder['event' + str(i)].place(relx=0.285, rely=0.02)
        eventdate_holder['date' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], text=eventdate[i],
                                                         font=("Courier New", 14), bg_color="transparent",
                                                         fg_color="transparent")
        eventdate_holder['date' + str(i)].place(x=58, rely=0.46)
        if lenevent == 1:  # if there is only one upcoming event, creates only one upcoming event border
            eventbd_holder['bd' + str(i)].place(relx=0.38, rely=0.3)
        elif lenevent == 2:  # if there is two upcoming event, creates two upcoming event borders
            eventbd_holder['bd' + str(i)].place(relx=counter2, rely=0.3)
            counter2 = counter2 + 0.3
        counter = counter + 0.3


# function to update the points
def updatepoints():
    from main import student
    from login import email
    global pointsLabel, pointsFrame
    user = student.find_one({'email': email})  # finds the user from the datebase based on email
    points = user['points']  # sets the user points to the variable points
    if points >= 1000:
        pointsFrame.configure(width=105)
    elif points >= 100:
        pointsFrame.configure(width=80)
    elif points == 0:
        pointsFrame.configure(width=55)
    pointsLabel.configure(text=points)  # sets points


# function to switch to report page
def reportPage(self, controller):
    from report import winners, reportPage, updateUserinfo
    updateUserinfo(False)
    winners()
    show_frame(self, controller, reportPage)


# function to logout and go back to the login screen
def logout(self, controller, para1):
    from login import loginPage
    show_frame(self, controller, loginPage)
    menuClose(self, para1)


# function to open the menu and close
def menuOpen(self, para1):
    global openm
    if not openm:
        self.settingFrame.place(relx=0.95)
        if para1:  # for
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


# function to close the menu and clear entries
def menuClose(self, para1):
    self.settingFrame.place(relx=1)
    if para1:
        self.menuButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
        self.logoutButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")
    else:
        self.menuButton.configure(fg_color="#212121", hover_color="#292929", bg_color="#212121")
        self.logoutButton.configure(fg_color="#212121", hover_color="2929292", bg_color="#212121")


# initializes frame and places widgets on the page
class studentDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global welcomeLabel, frame, pointsLabel, pointsFrame, upcomingEventsFrame, errorImage
        ctk.CTkFrame.__init__(self, parent)

        # creating frames and borders around the screen
        frame = ctk.CTkFrame(self, width=800, height=500, fg_color="transparent")
        frame.place(relx=0, rely=0)

        # placing logo
        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[3]), light_image=Image.open(env.img[3]),
                                      size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0, rely=-0.05)

        # Welcome label for students
        welcomeLabel = ctk.CTkLabel(self, text="Welcome", font=("courier new", 26))
        welcomeLabel.place(relx=0.055, rely=0.025)

        # Points frame
        pointsFrame = ctk.CTkFrame(self, width=80, height=37, fg_color="transparent", border_color="#212121",
                                   border_width=2)
        pointsFrame.place(relx=0.809)

        self.pointsImage = ctk.CTkImage(dark_image=Image.open(env.img[8]), light_image=Image.open(env.img[8]),
                                        size=(30, 30))
        self.pointsImageL = ctk.CTkLabel(self, image=self.pointsImage, text="")
        self.pointsImageL.place(relx=0.81, rely=0.005)

        pointsLabel = ctk.CTkLabel(self, text="0", font=("courier new", 25))
        pointsLabel.place(relx=0.85, rely=0.0099)

        # To add event page button
        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[7]),
                                      light_image=Image.open(env.img[7]), size=(75, 75))
        self.eventsButton = ctk.CTkButton(self, image=self.plusImage, text="Events", width=15, height=50,
                                          fg_color="#292929",
                                          hover_color="#212121", font=("courier new", 24), border_width=2,
                                          border_spacing=20, border_color="#212121",
                                          command=lambda: toaddEvents(self, controller))
        self.eventsButton.place(relx=0.085, rely=0.45)

        # To report page button
        self.reportImage = ctk.CTkImage(dark_image=Image.open(env.img[10]), light_image=Image.open(env.img[10]),
                                        size=(20, 20))
        self.reportButton = ctk.CTkButton(self, image=self.reportImage, text="", width=35, height=35,
                                          fg_color="#292929", hover_color="#212121",
                                          command=lambda: reportPage(self, controller))
        self.reportButton.place(relx=0.96, rely=0.64)

        # adding leaderboard labels
        self.lbTitle = ctk.CTkLabel(self, text="Leaderboard", font=("Courier New", 28)).place(relx=0.55, rely=0.1)

        self.lbHeadings = ctk.CTkLabel(self, text="Name\t" + "      " + "Grade" + "    " + "Points",
                                       font=("courier new", 22))
        self.lbHeadings.place(relx=0.45, rely=0.2)

        # Upcoming Events labels
        upcomingEventsFrame = ctk.CTkFrame(self, width=800, height=150, corner_radius=10, bg_color="#363636",
                                           fg_color="#363636")
        upcomingEventsFrame.place(relx=0, y=350)

        errorImage = ctk.CTkImage(dark_image=Image.open(env.img[9]), light_image=Image.open(env.img[9]), size=(75, 75))

        self.upcomingTitle = ctk.CTkLabel(upcomingEventsFrame, text="Upcoming Events", font=("Courier New", 18)).place(
            relx=0.4, rely=0.05)

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

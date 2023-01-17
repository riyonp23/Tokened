from datetime import datetime, date
import customtkinter as ctk
from PIL import Image
import env
from help import helpPage


# add help button to menu
# add help screen


def show_frame(self, controller, page):
    frame = controller.frames[page]
    # raises the current frame to the top
    menuClose(self, True)
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
upcomingEventsFrame = None
errorImage = None
openm = False
name_holder = {}
grade_holder = {}
points_holder = {}
eventbd_holder = {}
event_holder = {}
eventdate_holder = {}


def updatelb():
    from main import collection
    from login import school
    global frame, name_holder, grade_holder, points_holder
    lbStudentName = []
    lbStudentGrade = []
    lbStudentPoints = []
    for i in collection.find({'school': school}).sort('points', -1):
        lbStudentName.append(str(i['first_name'] + " " + i["last_name"]))
        lbStudentGrade.append(str(i["grade"]))
        lbStudentPoints.append(str(i["points"]))

    lenevent = 0
    if len(lbStudentName) < 5:
        lenevent = len(lbStudentName)
    else:
        lenevent = 5
    counter = 0.3
    for i in range(len(name_holder)):
        if len(name_holder) > 0:
            name_holder['name' + str(i)].destroy()
            grade_holder['grade' + str(i)].destroy()
            points_holder['pointsum' + str(i)].destroy()
    for i in range(lenevent):
        name_holder['name' + str(i)] = ctk.CTkLabel(frame, text=lbStudentName[i])
        name_holder['name' + str(i)].place(relx=0.45, rely=counter)
        grade_holder["grade" + str(i)] = ctk.CTkLabel(frame, text=lbStudentGrade[i])
        grade_holder["grade" + str(i)].place(relx=0.7, rely=counter)
        points_holder["pointsum" + str(i)] = ctk.CTkLabel(frame, text=lbStudentPoints[i])
        points_holder["pointsum" + str(i)].place(x=680, rely=counter)
        counter = counter + 0.08


def updateupcoming():
    from main import events
    from login import email
    global upcomingEventsFrame, event_holder, eventdate_holder, eventbd_holder, errorImage
    eventname = []
    eventdate = []
    for i in events.find({'email': email}).sort('sortdate', -1):
        eventname.append(i['event'])
        eventdate.append(i['date'])
    currentdate = date.today().strftime("%m/%d/%Y")
    eventdate.append(currentdate)
    eventdate.sort(key=lambda date: datetime.strptime(date, "%m/%d/%Y"), reverse=True)
    index = eventdate.index(currentdate)
    eventname.insert(index, 'space')
    for i in range(len(eventdate)):
        if index < i:
            eventdate.pop()
    for i in range(len(eventname)):
        if index < i:
            eventname.pop()
    eventdate.remove(currentdate)
    eventname.remove('space')
    lenevent = 0
    if len(eventdate) < 3:
        lenevent = len(eventdate)
    else:
        lenevent = 3
    counter = 0.08
    counter2 = 0.23
    for i in range(len(event_holder)):
        if len(event_holder) > 0:
            event_holder['event' + str(i)].destroy()
            eventdate_holder['date' + str(i)].destroy()
            eventbd_holder['bd' + str(i)].destroy()
    if lenevent == 0:
        for i in range(3):
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
    for i in range(lenevent):
        eventbd_holder['bd' + str(i)] = ctk.CTkFrame(upcomingEventsFrame, width=200, height=90, bg_color="transparent",
                                                     fg_color="transparent", border_width=2, border_color="#292929")
        eventbd_holder['bd' + str(i)].place(relx=counter, rely=0.3)
        event_holder['event' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], text=eventname[i],
                                                      font=("Courier New", 12), bg_color="transparent",
                                                      fg_color="transparent")
        event_holder['event' + str(i)].place(x=15, rely=0.02)
        eventdate_holder['date' + str(i)] = ctk.CTkLabel(eventbd_holder['bd' + str(i)], text=eventdate[i],
                                                         font=("Courier New", 14), bg_color="transparent",
                                                         fg_color="transparent")
        eventdate_holder['date' + str(i)].place(x=58, rely=0.46)
        if lenevent == 1:
            eventbd_holder['bd' + str(i)].place(relx=0.38, rely=0.3)
        elif lenevent == 2:
            eventbd_holder['bd' + str(i)].place(relx=counter2, rely=0.3)
            counter2 = counter2 + 0.3
        counter = counter + 0.3


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


def reportPage(self, controller):
    from report import winners, reportPage, updateUserinfo
    updateUserinfo()
    winners()
    show_frame(self, controller, reportPage)


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


def menuOpen(self, para1):
    global openm
    if not openm:
        self.settingFrame.place(relx=0.8)
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
        global welcomeLabel, frame, pointsLabel, pointsFrame, upcomingEventsFrame, errorImage
        ctk.CTkFrame.__init__(self, parent)
        frame = ctk.CTkFrame(self, width=800, height=500, fg_color="transparent")
        frame.place(relx=0, rely=0)

        self.mainImage = ctk.CTkImage(dark_image=Image.open(env.img[3]), light_image=Image.open(env.img[3]),
                                      size=(350, 350))
        self.imageLabel = ctk.CTkLabel(self, image=self.mainImage, text="")
        self.imageLabel.place(relx=0, rely=-0.05)

        welcomeLabel = ctk.CTkLabel(self, text="Welcome", font=("courier new", 26))
        welcomeLabel.place(relx=0.055, rely=0.025)

        pointsFrame = ctk.CTkFrame(self, width=80, height=37, fg_color="transparent", border_color="#212121",
                                   border_width=2)
        pointsFrame.place(relx=0.809)

        self.pointsImage = ctk.CTkImage(dark_image=Image.open(env.img[8]), light_image=Image.open(env.img[8]),
                                        size=(30, 30))
        self.pointsImageL = ctk.CTkLabel(self, image=self.pointsImage, text="")
        self.pointsImageL.place(relx=0.81, rely=0.005)

        pointsLabel = ctk.CTkLabel(self, text="0", font=("courier new", 25))
        pointsLabel.place(relx=0.85, rely=0.0099)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[7]),
                                      light_image=Image.open(env.img[7]), size=(75, 75))
        self.eventsButton = ctk.CTkButton(self, image=self.plusImage, text="Events", width=15, height=50,
                                          fg_color="#292929",
                                          hover_color="#212121", font=("courier new", 24), border_width=2,
                                          border_spacing=20, border_color="#212121",
                                          command=lambda: toaddEvents(self, controller))
        self.eventsButton.place(relx=0.085, rely=0.45)

        self.reportImage = ctk.CTkImage(dark_image=Image.open(env.img[10]), light_image=Image.open(env.img[10]),
                                        size=(20, 20))
        self.reportButton = ctk.CTkButton(self, image=self.reportImage, text="", width=35, height=35,
                                          fg_color="#292929", hover_color="#212121",
                                          command=lambda: reportPage(self, controller))
        self.reportButton.place(relx=0.96, rely=0.64)

        self.lbTitle = ctk.CTkLabel(self, text="Leaderboard", font=("Courier New", 28)).place(relx=0.55, rely=0.1)

        self.lbHeadings = ctk.CTkLabel(self, text="Name\t" + "      " + "Grade" + "    " + "Points",
                                       font=("courier new", 22))
        self.lbHeadings.place(relx=0.45, rely=0.2)

        upcomingEventsFrame = ctk.CTkFrame(self, width=800, height=150, corner_radius=10, bg_color="#363636",
                                           fg_color="#363636")
        upcomingEventsFrame.place(relx=0, y=350)

        errorImage = ctk.CTkImage(dark_image=Image.open(env.img[9]), light_image=Image.open(env.img[9]), size=(75, 75))

        self.upcomingTitle = ctk.CTkLabel(upcomingEventsFrame, text="Upcoming Events", font=("Courier New", 18)).place(
            relx=0.4, rely=0.05)

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

        self.helpImage = ctk.CTkImage(dark_image=Image.open(env.img[11]), light_image=Image.open(env.img[11]),
                                      size=(20, 20))
        self.helpButton = ctk.CTkButton(self.settingFrame, image=self.helpImage, text="", width=25, height=25,
                                        fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                        command=lambda: show_frame(self, controller, helpPage))
        self.helpButton.place(relx=0.79, rely=0.87)

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

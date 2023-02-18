from datetime import date, datetime

import customtkinter as ctk
from PIL import Image

import env
from account import accountPage
from help import helpPage


def show_frame(self, controller, page):  # used to switch to next frame
    frame = controller.frames[page]
    frame.tkraise()


# Initializes variable
welcomeTLabel = None
upcomingEventsFrame = None
errorImage = None
frame = None
eventbd_holder = {}
event_holder = {}
eventdate_holder = {}
event_holder2 = {}
date_holder = {}


# function to change welcome label to the teacher's last name
def changeTextT():
    from login import last_name
    global welcomeTLabel
    welcomeTLabel.configure(text="Welcome, " + last_name)


# Updates events in the events list
def updateeventsT():
    from main import events
    from login import school
    global frame, event_holder2, date_holder
    eventname = []
    tempeventdate = []
    for i in events.find({'school': school}).sort('sortdate', 1):  # sorts all events by date
        eventname.append(i['event'])
        tempeventdate.append(str(i['date']))

    lenevent = 0
    if len(eventname) < 5:  # Only allows maximum of 5 events shown at a time
        lenevent = len(eventname)
    else:
        lenevent = 5
    counter = 0.26
    for i in range(len(event_holder2)):
        if len(event_holder2) > 0:  # if the event name and date is already created, deletes it
            event_holder2['event' + str(i)].destroy()
            date_holder['date' + str(i)].destroy()
    for i in range(lenevent):  # Initializes the event name and date
        event_holder2['event' + str(i)] = ctk.CTkLabel(frame, text=eventname[i], font=("courier new", 14),
                                                       fg_color="#292929")
        event_holder2['event' + str(i)].place(x=410, rely=counter)
        date_holder['date' + str(i)] = ctk.CTkLabel(frame, text=tempeventdate[i], font=("courier new", 14),
                                                    fg_color="#292929")
        date_holder['date' + str(i)].place(x=650, rely=counter)
        counter = counter + 0.08


# Updates upcoming events list
def updateupcomingT():
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
    for i in reversed(range(len(eventdate))):  # Removes all the dates that are before today's date
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


# Adds new event for the school the teacher belongs to
def addEventT(self):
    from main import events
    from login import school
    self.errorMessage2.configure(text="", text_color="red")
    if self.eventBox.get() == "events" or self.dateEntry.get() == " ":
        self.errorMessage2.configure(text="Error: Fill All Fields")
        self.errorMessage2.place(relx=0.34)
        return
    try:
        datetime.strptime(self.dateEntry.get(), '%m/%d/%Y')
        pass
    except ValueError:
        self.errorMessage2.place(relx=0.3)
        return self.errorMessage2.configure(text="Error: Wrong Date Format")
    # Obtaining date from entries
    eventname = self.eventBox.get()
    date = self.dateEntry.get()
    date_object = datetime.strptime(date, "%m/%d/%Y")  # creating new format date
    sdate = date_object.strftime("%Y-%m-%d")
    event = {'school': school, "event": eventname, "sortdate": sdate, "date": date}
    events.insert_one(event)  # inserting new event into database, sorted by school
    self.errorMessage2.place(relx=0.28)
    self.errorMessage2.configure(text="Successfully Added Event", text_color="green")
    self.eventBox.set("events")
    self.dateEntry.delete(0, ctk.END)
    updateupcomingT()
    updateeventsT()


# function to change to report page
def reportPage(self, controller):
    from report import winners, reportPage, updateUserinfo
    updateUserinfo(True)
    winners()
    show_frame(self, controller, reportPage)


# initializes frame for teacher dashboard and places widgets
class teacherDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import menuOpen, logout
        global welcomeTLabel, upcomingEventsFrame, errorImage, frame

        # creating frames and borders around the screen
        frame = ctk.CTkFrame(self, width=800, height=500, fg_color="transparent")
        frame.place(relx=0, rely=0)

        self.lbBorder = ctk.CTkFrame(self, width=370, height=500, fg_color="transparent")
        self.lbBorder.place(relx=0)

        # Welcome label for teacher
        welcomeTLabel = ctk.CTkLabel(self, text="Welcome", font=("courier new", 26))
        welcomeTLabel.place(relx=0.055, rely=0.025)

        # adding add event labels, entries, and buttons
        self.addeventtitle = ctk.CTkLabel(self.lbBorder, text="Add Event", font=("courier new", 25)).place(relx=0.3,
                                                                                                           rely=0.2)

        self.eventBox = ctk.CTkOptionMenu(self.lbBorder, values=env.events, width=200, dropdown_fg_color="#343638",
                                          bg_color="#343638", fg_color="#343638", button_color="#343638",
                                          dynamic_resizing=False, text_color="gray")
        self.eventBox.place(relx=0.2, rely=0.3)
        self.eventBox.set("events")

        self.dateEntry = ctk.CTkEntry(self.lbBorder, placeholder_text="Date: mm/dd/yyyy", width=200)
        self.dateEntry.place(relx=0.2, rely=0.4)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[4]), light_image=Image.open(env.img[4]),
                                      size=(28, 28))

        self.plusButton = ctk.CTkButton(self.lbBorder, image=self.plusImage, text="", width=28, height=28,
                                        fg_color="#292929", bg_color="#292929", hover_color="#212121",
                                        command=lambda: addEventT(self))
        self.plusButton.place(relx=0.4, rely=0.52)

        self.errorMessage2 = ctk.CTkLabel(self.lbBorder, text="", text_color="red")
        self.errorMessage2.place(relx=0.34, rely=0.46)

        # Events Added List labels
        self.eventleaderboardtitle = ctk.CTkLabel(self, text="Added Events", font=("courier new", 25),
                                                  text_color="white")
        self.eventleaderboardtitle.place(relx=0.6, rely=0.1)
        self.eventleaderboard = ctk.CTkLabel(self, text=" Event   \t\tDate  ", font=("courier new", 18),
                                             text_color="white", corner_radius=20, fg_color="#212121")
        self.eventleaderboard.place(relx=0.48, rely=0.2)

        # Report Page buttons
        self.reportImage = ctk.CTkImage(dark_image=Image.open(env.img[10]), light_image=Image.open(env.img[10]),
                                        size=(20, 20))
        self.reportButton = ctk.CTkButton(self, image=self.reportImage, text="", width=35, height=35,
                                          fg_color="#292929", hover_color="#212121",
                                          command=lambda: reportPage(self, controller))
        self.reportButton.place(relx=0.96, rely=0.64)

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

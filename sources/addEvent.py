from datetime import datetime, date

import customtkinter as ctk
from PIL import Image

import env
from account import accountPage
from help import helpPage
from student import studentDashboard, menuOpen, logout


def show_frame(self, controller, cont):  # used to switch to next frame
    global feedbacktext1, eventBox
    from student import menuClose
    frame = controller.frames[cont]
    # raises the current frame to the top
    frame.tkraise()
    self.feedbackslider.set(5)
    self.errorMessage2.configure(text="")
    self.checkbox.deselect()
    feedbacktext1.configure(text="Feedback: 5")
    menuClose(self, False)


# initializes all variables, lists, and dictionary
feedbacktext1 = None
frame = None
eventBox = None
event_holder = {}
date_holder = {}
feedback_holder = {}
eventnameOG = []
eventdateOG = []
eventsortdateOG = []
eventnamenew = []
eventdatenew = []


# Initializes event list from dropdown
def eventdropdown():
    from main import events
    from login import school
    global eventBox, eventnameOG, eventdateOG, eventsortdateOG
    for i in events.find({'school': school}).sort('sortdate', 1):  # sorts all events by date
        eventnameOG.append(i['event'])
        eventdateOG.append(i['date'])
    currentdate = date.today().strftime("%m/%d/%Y")  # gets today's date
    eventdateOG.append(currentdate)
    eventdateOG.sort(key=lambda date: datetime.strptime(date, "%m/%d/%Y"), reverse=False)  # resorts the dates
    index = eventdateOG.index(currentdate)
    eventnameOG.insert(index, 'space')
    for i in reversed(range(len(eventdateOG))):  # Removes all the dates that are after today's date
        if index < i:
            del eventdateOG[i]
    for i in reversed(range(len(eventnameOG))):
        if index < i:
            del eventnameOG[i]
    eventdateOG.remove(currentdate)  # Removes today's date
    eventnameOG.remove('space')
    eventBox.configure(values=eventnameOG)  # Updates events in dropdown menu


# Function to remove common elements from two lists
def remove_commonelement(a, b, newlist):
    a, b = list(set(a).difference(b)), list(set(b).difference(a))

    newlist.clear()
    for elem in a:
        newlist.append(elem)


# Updates event list from dropdown
def updateeventdropdown():
    from main import student_events
    from login import email
    global eventBox, eventnameOG, eventdateOG, eventnamenew, eventdatenew
    for i in student_events.find({'email': email}).sort('sortdate', 1):  # sorts all events by date
        eventnamenew.append(i['event'])
        eventdatenew.append(i['date'])
    remove_commonelement(eventnameOG, eventnamenew, eventnameOG)  # removes common events between the lists
    remove_commonelement(eventdateOG, eventdatenew, eventdateOG)  # removes common event dates between the lists
    if len(eventnameOG) == 0:
        eventBox.set("No More Events")
        eventBox.configure(state="disabled")
        return
    eventBox.set("events")
    eventBox.configure(state="normal", values=eventnameOG)  # Updates events in dropdown menu


# Updates list events
def updateevents():
    from main import student_events
    from login import email
    global frame, event_holder, date_holder, feedback_holder
    eventname = []
    tempeventdate = []
    eventfeedback = []
    for i in student_events.find({'email': email}).sort('sortdate', -1):  # sorts all events by date
        eventname.append(i['event'])
        tempeventdate.append(str(i['date']))
        eventfeedback.append(i['feedback'])

    lenevent = 0
    if len(eventname) < 5:
        lenevent = len(eventname)
    else:
        lenevent = 5
    counter = 0.3
    for i in range(len(event_holder)):
        if len(event_holder) > 0:  # if the event name, date, and feedback is already created, deletes it
            event_holder['event' + str(i)].destroy()
            date_holder['date' + str(i)].destroy()
            feedback_holder['feedback' + str(i)].destroy()
    for i in range(lenevent):  # Initializes the event name, date, and feedback
        event_holder['event' + str(i)] = ctk.CTkLabel(frame, text=eventname[i], font=("courier new", 14))
        event_holder['event' + str(i)].place(x=370, rely=counter)
        date_holder['date' + str(i)] = ctk.CTkLabel(frame, text=tempeventdate[i], font=("courier new", 14))
        date_holder['date' + str(i)].place(x=600, rely=counter)
        feedback_holder['feedback' + str(i)] = ctk.CTkLabel(frame, text=str(eventfeedback[i]) + "/10",
                                                            font=("courier new", 14))
        feedback_holder['feedback' + str(i)].place(x=710, rely=counter)
        counter = counter + 0.11


# Adds new events to student
def addEvent(self):
    from main import student_events, student
    from login import email
    from student import updatelb, updatepoints
    global eventBox, eventnameOG, eventdateOG, feedbacktext1
    if eventBox.get() == "No More Events":
        self.errorMessage2.configure(
            text="Error: Please Wait For Your Upcoming Events To Pass\nOr For Your Teacher To Add More Events")
        self.errorMessage2.place(relx=0.08)
        return
    if eventBox.get() == "events" or self.checkbox.get() is not True:
        self.errorMessage2.configure(text="Error: Fill All Fields")
        self.errorMessage2.place(relx=0.34)
        return
    self.errorMessage2.configure(text="")
    # gets data from entries
    eventname = eventBox.get()
    feedback = int(self.feedbackslider.get())
    index = eventnameOG.index(eventname)
    date_object = datetime.strptime(eventdateOG[index], "%m/%d/%Y")  # creates new formated date
    sdate = date_object.strftime("%Y-%m-%d")
    event = {'email': email, "event": eventname, "sortdate": sdate, "date": eventdateOG[index], "feedback": feedback}
    student_events.insert_one(event)  # Creates new event in database
    user = student.find_one({'email': email})
    points = user['points'] + 200
    student.find_one_and_update({'email': email}, {'$set': {"points": points}})  # adds points to the student
    self.feedbackslider.set(5)
    self.checkbox.deselect()
    feedbacktext1.configure(text="Feedback: 5")
    updateevents()
    updateeventdropdown()
    updatelb()
    updatepoints()


# Function to update the slider value
def slider_event(value):
    global feedbacktext1
    if int(value) == 1:
        return feedbacktext1.configure(text="Feedback: " + str(int(value)) + " (Dissatisfied)")
    elif int(value) == 10:
        return feedbacktext1.configure(text="Feedback: " + str(int(value)) + " (Very Satisfied)")
    feedbacktext1.configure(text="Feedback: " + str(int(value)))


# initializes frame and places widgets on the window
class eventPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        global feedbacktext1, frame, eventBox

        # creating frames and borders around the screen
        frame = ctk.CTkFrame(self, width=800, height=500)
        frame.place(relx=0, rely=0)

        self.lbBorder = ctk.CTkCanvas(self, width=370, height=500, bg="#212121", border=0, highlightthickness=0)
        self.lbBorder.place(relx=0)

        # adding add event labels, entries, and buttons
        self.addeventtitle = ctk.CTkLabel(self.lbBorder, text="Add Event", font=("courier new", 25)).place(relx=0.3,
                                                                                                           rely=0.2)

        eventBox = ctk.CTkOptionMenu(self.lbBorder, values=[], width=200, dropdown_fg_color="#343638",
                                     bg_color="#343638", fg_color="#343638", button_color="#343638",
                                     dynamic_resizing=False, text_color="gray")
        eventBox.place(relx=0.2, rely=0.3)
        eventBox.set("events")

        self.text = ctk.CTkLabel(self.lbBorder, text="Rate Your Overall Experience", font=("courier new", 13)).place(
            relx=0.19, rely=0.38)

        self.feedbackslider = ctk.CTkSlider(self.lbBorder, from_=1, to=10, number_of_steps=9, command=slider_event)
        self.feedbackslider.place(relx=0.2, rely=0.44)

        feedbacktext1 = ctk.CTkLabel(self.lbBorder, text="Feedback: 5", font=("courier new", 12), width=0, height=0)
        feedbacktext1.place(relx=0.36, rely=0.48)

        self.checkbox = ctk.CTkCheckBox(self.lbBorder, text="I acknowledge that I was\n  present at the event",
                                        onvalue=True, offvalue=False, checkbox_height=20, font=("courier new", 12),
                                        checkbox_width=20)
        self.checkbox.place(relx=0.2, rely=0.54)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[4]), light_image=Image.open(env.img[4]),
                                      size=(28, 28))

        line = self.lbBorder.create_line(360, 0, 360, 600, fill='#292929', width=1)

        self.plusButton = ctk.CTkButton(self.lbBorder, image=self.plusImage, text="", width=28, height=28,
                                        fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                        command=lambda: addEvent(self))
        self.plusButton.place(relx=0.4, rely=0.62)

        self.errorMessage2 = ctk.CTkLabel(self.lbBorder, text="", text_color="red")
        self.errorMessage2.place(relx=0.34, rely=0.7)

        # adding event participated list labels
        self.eventleaderboardtitle = ctk.CTkLabel(self, text="Events Participated", font=("courier new", 25),
                                                  text_color="white")
        self.eventleaderboardtitle.place(relx=0.56, rely=0.05)
        self.eventleaderboard = ctk.CTkLabel(self, text="  Event\t\t    Date     Feedback ", font=("courier new", 18),
                                             text_color="white", corner_radius=20)
        self.eventleaderboard.place(relx=0.45, rely=0.2)

        # back button to go back to student dashboard
        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#212121", height=25, width=25,
                                        bg_color="#212121",
                                        hover_color="#292929",
                                        command=lambda: show_frame(self, controller, studentDashboard))
        self.backButton.place(relx=0, rely=0)

        # initializes settings menu frame
        self.settingFrame = ctk.CTkCanvas(self, width=100, height=500, background="#292929", highlightthickness=0,
                                          borderwidth=0)

        # places menu button
        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#212121",
                                        bg_color="#212121",
                                        hover_color="#292929", command=lambda: menuOpen(self, False))
        self.menuButton.place(relx=0.95, rely=0)

        # places account settings button

        self.accountImage = ctk.CTkImage(dark_image=Image.open(env.img[12]), light_image=Image.open(env.img[12]),
                                         size=(29, 29))
        self.accountButton = ctk.CTkButton(self.settingFrame, image=self.accountImage, text="", width=25, height=25,
                                           fg_color="#292929", bg_color="#292929", hover_color="#212121",
                                           command=lambda: show_frame(self, controller, accountPage))
        self.accountButton.place(relx=-0.015, rely=0.765)

        # places help button
        self.helpImage = ctk.CTkImage(dark_image=Image.open(env.img[11]), light_image=Image.open(env.img[11]),
                                      size=(28, 28))
        self.helpButton = ctk.CTkButton(self.settingFrame, image=self.helpImage, text="", width=25, height=25,
                                        fg_color="#292929", bg_color="#292929", hover_color="#212121",
                                        command=lambda: show_frame(self, controller, helpPage))
        self.helpButton.place(relx=-0.015, rely=0.84)

        # places log out button
        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]),
                                        size=(37, 37))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=50,
                                          fg_color="#292929", bg_color="#292929", hover_color="#212121",
                                          command=lambda: logout(self, controller, False))
        self.logoutButton.place(relx=-0.04, rely=0.91)

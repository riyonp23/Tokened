from datetime import datetime
import customtkinter as ctk
import env
from PIL import Image
from student import student, menuOpen, changepass, logout

feedbacktext1 = None
frame = None
event_holder = {}
date_holder = {}
feedback_holder = {}


def show_frame(self, controller, cont):  # used to switch to next frame
    global feedbacktext1
    frame = controller.frames[cont]
    # raises the current frame to the top
    frame.tkraise()
    self.eventBox.set("events")
    self.dateEntry.delete(0, ctk.END)
    self.dateEntry.configure(placeholder_text="Date: mm/dd/yyyy")
    self.feedbackslider.set(5)
    feedbacktext1.configure(text="Feedback: 5")


def updateevents():
    from main import events
    from login import email
    global frame, event_holder, date_holder, feedback_holder
    eventname = []
    tempeventdate = []
    eventfeedback = []
    for i in events.find({'email': email}).sort('sortdate', -1):
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
        if len(event_holder) > 0:
            event_holder['event' + str(i)].destroy()
            date_holder['date' + str(i)].destroy()
            feedback_holder['feedback' + str(i)].destroy()
    for i in range(lenevent):
        event_holder['event' + str(i)] = ctk.CTkLabel(frame, text=eventname[i], font=("courier new", 14))
        event_holder['event' + str(i)].place(x=370, rely=counter)
        date_holder['date' + str(i)] = ctk.CTkLabel(frame, text=tempeventdate[i], font=("courier new", 14))
        date_holder['date' + str(i)].place(x=600, rely=counter)
        feedback_holder['feedback' + str(i)] = ctk.CTkLabel(frame, text=str(eventfeedback[i]) + "/10", font=("courier new", 14))
        feedback_holder['feedback' + str(i)].place(x=710, rely=counter)
        counter = counter + 0.11


def addEvent(self):
    from main import events, collection
    from login import email
    from student import updatelb, updatepoints
    if self.eventBox.get() == "events" or self.dateEntry.get() == " ":
        self.errorMessage.place(relx=0.34)
        return self.errorMessage.configure(text="Error: Fill All Fields")
    try:
        datetime.strptime(self.dateEntry.get(), '%m/%d/%Y')
        pass
    except ValueError:
        self.errorMessage.place(relx=0.3)
        return self.errorMessage.configure(text="Error: Wrong Date Format")
    self.errorMessage.configure(text="")
    eventname = self.eventBox.get()
    date = self.dateEntry.get()
    date_object = datetime.strptime(date, "%m/%d/%Y")
    sdate = date_object.strftime("%Y-%m-%d")
    feedback = int(self.feedbackslider.get())
    event = {"email": email, "event": eventname, "sortdate": sdate, "date": date, "feedback": feedback}
    events.insert_one(event)
    points = collection.find_one({'email': email})
    points = points['points'] + 200
    collection.find_one_and_update({'email': email}, {'$set': {"points": points}})
    updateevents()
    updatelb()
    updatepoints()


def slider_event(value):
    global feedbacktext1
    if int(value) == 1:
        return feedbacktext1.configure(text="Feedback: " + str(int(value)) + " (Dissatisfied)")
    elif int(value) == 10:
        return feedbacktext1.configure(text="Feedback: " + str(int(value)) + " (Very Satisfied)")
    feedbacktext1.configure(text="Feedback: " + str(int(value)))


class eventPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)  # make sure to put self. then variable name to use in the program
        global feedbacktext1, frame

        frame = ctk.CTkFrame(self, width=800, height=500)
        frame.place(relx=0,rely=0)

        self.lbBorder = ctk.CTkCanvas(self, width=370, height=500, bg="#212121", border=0, highlightthickness=0)
        self.lbBorder.place(relx=0)

        self.addeventtitle = ctk.CTkLabel(self.lbBorder, text="Add Event", font=("courier new", 25)).place(relx=0.3,
                                                                                                           rely=0.2)

        self.eventBox = ctk.CTkOptionMenu(self.lbBorder, values=env.events, width=200, dropdown_fg_color="#343638",
                                          bg_color="#343638", fg_color="#343638", button_color="#343638",
                                          dynamic_resizing=False, text_color="gray")
        self.eventBox.place(relx=0.2, rely=0.3)
        self.eventBox.set("events")

        self.dateEntry = ctk.CTkEntry(self.lbBorder, placeholder_text="Date: mm/dd/yyyy", width=200)
        self.dateEntry.place(relx=0.2, rely=0.4)

        self.text = ctk.CTkLabel(self.lbBorder, text="Rate Your Overall Experience", font=("courier new", 13)).place(
            relx=0.19, rely=0.48)

        self.feedbackslider = ctk.CTkSlider(self.lbBorder, from_=1, to=10, number_of_steps=9, command=slider_event)
        self.feedbackslider.place(relx=0.2, rely=0.54)

        feedbacktext1 = ctk.CTkLabel(self.lbBorder, text="Feedback: 5", font=("courier new", 12), width=0, height=0)
        feedbacktext1.place(relx=0.36, rely=0.58)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[4]), light_image=Image.open(env.img[4]),
                                      size=(28, 28))

        line = self.lbBorder.create_line(360, 0, 360, 600, fill='#292929', width=1)

        self.plusButton = ctk.CTkButton(self.lbBorder, image=self.plusImage, text="", width=28, height=28,
                                        fg_color="#212121", bg_color="#212121", hover_color="#292929", command=lambda: addEvent(self))
        self.plusButton.place(relx=0.4, rely=0.62)

        self.errorMessage = ctk.CTkLabel(self.lbBorder, text="", text_color="red")
        self.errorMessage.place(relx=0.34, rely=0.7)

        self.eventleaderboardtitle = ctk.CTkLabel(self, text="Recent Events", font=("courier new", 25),
                                                  text_color="white")
        self.eventleaderboardtitle.place(relx=0.6, rely=0.05)
        self.eventleaderboard = ctk.CTkLabel(self, text="  Event\t\t    Date     Feedback ", font=("courier new", 18),
                                             text_color="white", corner_radius=20)
        self.eventleaderboard.place(relx=0.45, rely=0.2)

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#212121", height=25, width=25,
                                        bg_color="#212121",
                                        hover_color="#292929", command=lambda: show_frame(self, controller, student))
        self.backButton.place(relx=0, rely=0)

        self.settingFrame = ctk.CTkCanvas(self, width=160, height=500, background="#292929", highlightthickness=0,
                                          borderwidth=0)

        self.labeltest = ctk.CTkLabel(self.settingFrame, text="Settings", font=("courier new", 15))
        self.labeltest.place(relx=0.24, rely=0.12)

        self.ogpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="password", width=100, show="\u2022")
        self.ogpassEntry.place(relx=0.16, rely=0.2)

        self.newpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="new password", width=100, show="\u2022")
        self.newpassEntry.place(relx=0.16, rely=0.3)

        self.newconpassEntry = ctk.CTkEntry(self.settingFrame, placeholder_text="confirm password", width=100, show="\u2022")
        self.newconpassEntry.place(relx=0.16, rely=0.4)

        self.errorMessage = ctk.CTkLabel(self.settingFrame, text="", text_color="red")
        self.errorMessage.place(relx=0.16, rely=0.46)

        self.saveButton = ctk.CTkButton(self.settingFrame, text="Save", width=40, height=10, fg_color="#292929", bg_color="#292929", hover_color="#212121", command=lambda: changepass(self))
        self.saveButton.place(relx=0.34, rely=0.52)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#212121", bg_color="#212121",
                                        hover_color="#292929", command=lambda: menuOpen(self, False))
        self.menuButton.place(relx=0.95, rely=0)

        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]), size=(25,25))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=25, fg_color="#212121", bg_color="#212121", hover_color="#292929", command=lambda: logout(self, controller, False))
        self.logoutButton.place(relx=0.73, rely=0.93)

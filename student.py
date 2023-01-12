import customtkinter as ctk
from PIL import Image
import env


def show_frame(self, page):
    frame = self.frames[page]
    # raises the current frame to the top
    frame.tkraise()


welcomeLabel = None


def changeText():
    from login import first_name
    global welcomeLabel
    welcomeLabel.configure(text="Welcome, " + first_name)


openm = False

def menuOpen(self):
    global openm
    if not openm:
        self.settingFrame.place(relx=0.82)
        self.menuButton.configure(fg_color="#212121", hover_color="#292929", bg_color="#212121")
        openm = True
        return
    else:
        menuClose(self)
        openm = False
        return



def menuClose(self):
    self.settingFrame.place(relx=1)
    self.menuButton.configure(fg_color="#292929", hover_color="#212121", bg_color="#292929")


class student(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global welcomeLabel
        ctk.CTkFrame.__init__(self, parent)
        welcomeLabel = ctk.CTkLabel(self, text="Welcome, Iggy", font=("", 26))
        welcomeLabel.place(relx=0.055, rely=0.025)
        self.settingFrame = ctk.CTkCanvas(self, width=150, height=300, background="#212121", highlightthickness=0,
                                          borderwidth=0)

        self.labeltest = ctk.CTkLabel(self.settingFrame, text= "Settings")
        self.labeltest.place(relx=0.3, rely=0.12)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[2]),
                                      light_image=Image.open(env.img[2]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self))
        self.menuButton.place(relx=0.935, rely=0.025)

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[10]),
                                      light_image=Image.open(env.img[10]), size=(75, 75))
        self.eventsButton = ctk.CTkButton(self, image=self.plusImage, text="Events", width=15, height=50,
                                          fg_color="#292929", hover_color="#212121", font=("courier new", 24),
                                          border_width=2, border_spacing=20)
        self.eventsButton.place(relx=0.05, rely=0.2)

        self.lbTitle = ctk.CTkLabel(self, text="Leaderboard", font=("Courier New", 28)).place(relx=0.55, rely=0.1)

        self.lbHeadings = ctk.CTkLabel(self, text="Name\t" + "      " + "Grade" + "    " + "Points", font=("courier new", 22))
        self.lbHeadings.place(relx=0.45, rely=0.2)

        from main import collection
        lbStudentName = []
        for i in collection.find().sort("points", -1):
            lbStudentName.append(str(i['first_name'] + " " + i["last_name"]))
        print(lbStudentName)

        var_holder = {}
        place_holder = {}
        counter = 0.275
        for i in range(len(lbStudentName)):
            place_holder['num' + str(i)] = ctk.CTkLabel(self, text=str(i+1) + '.', font=("courier new", 18),
                                                        text_color="white").place(relx=0.4, rely=counter)
            var_holder['myvar' + str(i)] = ctk.CTkLabel(self, text=lbStudentName[i],
                                                        font=("courier new", 16)).place(relx=0.44, rely=counter)
            counter = counter + 0.09


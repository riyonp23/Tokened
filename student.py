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

        self.plusImage = ctk.CTkImage(dark_image=Image.open(env.img[8]),
                                      light_image=Image.open(env.img[8]), size=(75, 75))
        self.addButton = ctk.CTkButton(self, image=self.plusImage, text="Add Event",width=15, height=50, fg_color="#292929",
                                        hover_color="#212121", font=("", 24))
        self.addButton.place(relx=0.1, rely=0.3)
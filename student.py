import customtkinter as ctk
from PIL import Image

import env


def show_frame(self, page):
    frame = self.frames[page]
    # raises the current frame to the top
    frame.tkraise()


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
        ctk.CTkFrame.__init__(self, parent)
        self.settingFrame = ctk.CTkCanvas(self, width=150, height=500, background="#212121", highlightthickness=0,
                                          borderwidth=0)

        self.labeltest = ctk.CTkLabel(self.settingFrame, text="Account Settings")
        self.labeltest.place(relx=0.3)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[2]),
                                      light_image=Image.open(env.img[2]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self))
        self.menuButton.place(relx=0.955)


def userInfo(self):
    window = ctk.CTkToplevel(self)
    window.geometry("200x400")
    window.title("Tokened - Student Info")
    window.resizable(False, False)

    label = ctk.CTkLabel(window, text="CTkToplevel window")
    label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

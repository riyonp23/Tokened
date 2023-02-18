import webbrowser

import customtkinter as ctk
from PIL import Image

import env
from account import accountPage


def show_frame(self, controller, page):  # used to switch to next frame
    from login import grade
    from student import studentDashboard
    from teacher import teacherDashboard
    if grade == "Teacher" and page == studentDashboard:
        frame = controller.frames[teacherDashboard]
    else:
        frame = controller.frames[page]
    frame.tkraise()


# sets up function to open documentation website
def openWebsite():
    webbrowser.open_new_tab("https://github.com/riyonp23/Tokened")


# initializes frame for help page and places widgets
class helpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import studentDashboard, menuOpen, logout

        # places title label
        self.titleLabel = ctk.CTkLabel(self, text="Tokened - Help Page", font=("courier new", 30))
        self.titleLabel.place(relx=0.3, rely=0.05)

        # places contact us label along with email and phone number
        self.contacttitleLabel = ctk.CTkLabel(self, text="Contact Us", font=("courier new", 20))
        self.contacttitleLabel.place(relx=0.1, rely=0.3)
        self.contactLabel = ctk.CTkLabel(self, text="Phone: (813)-758-0531\n\t  Email: riyonpraveen23@gmail.com",
                                         font=("courier new", 17))
        self.contactLabel.place(relx=0.01, rely=0.36)

        # places code documentation label along with website link
        self.doctitelLabel = ctk.CTkLabel(self, text="Code Documentation", font=("courier new", 20))
        self.doctitelLabel.place(relx=0.1, rely=0.5)
        self.docLabel = ctk.CTkLabel(self, text="https://github.com/riyonp23/Tokened", font=("courier new", 15),
                                     cursor="hand2", text_color="#1b70cf")
        self.docLabel.place(relx=0.11, rely=0.55)
        self.docLabel.bind("<Button-1>", lambda e: openWebsite())

        self.authorLabel = ctk.CTkLabel(self, text="Riyon Praveen, Ignatius Martin, & Anay Patel © FBLA 2023",
                                        font=("courier new", 14))
        self.authorLabel.place(relx=0.24, rely=0.955)

        # places back button
        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121",
                                        command=lambda: show_frame(self, controller, studentDashboard))
        self.backButton.place(relx=0, rely=0)

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

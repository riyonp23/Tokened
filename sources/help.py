import customtkinter as ctk
import env
from PIL import Image
import webbrowser


def show_frame(self, controller, page):  # used to switch to next frame
    frame = controller.frames[page]
    # raises the current frame to the top
    frame.tkraise()
    self.schoolbox.set("school")
    self.gradebox.set("grade")
    self.errorMessage2.configure(text="")


def openWebsite():
    webbrowser.open_new_tab("https://github.com/skyy-rad/Tokened")


def changeschoolgrade(self):
    from main import collection
    import login
    userschool = None
    usergrade = None
    if self.schoolbox.get() == "school" and self.gradebox.get() == "grade":
       return self.errorMessage2.configure(text="Error: Please Fill One of the Options", text_color="red")
    if not self.schoolbox.get() == "school":
        userschool = self.schoolbox.get()
    if not self.gradebox.get() == "grade":
        usergrade = self.gradebox.get()
    if userschool is not None:
        collection.find_one_and_update({'email': login.email}, {'$set': {'school': userschool}})
        login.school = userschool
    if usergrade is not None:
        collection.find_one_and_update({'email': login.email}, {'$set': {'grade': usergrade}})
        login.grade = usergrade
    self.errorMessage2.configure(text="             Successfully Updated", text_color="green")
    self.schoolbox.set("school")
    self.gradebox.set("grade")

class helpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        from student import student, changepass, menuOpen, logout

        self.titleLabel = ctk.CTkLabel(self, text="Tokened - Help Page", font=("courier new", 30))
        self.titleLabel.place(relx=0.3, rely=0.05)

        self.changeLabel = ctk.CTkLabel(self, text="Change School Or Grade Level", font=("courier new", 20))
        self.changeLabel.place(relx=0.3, rely=0.2)

        self.schoolbox = ctk.CTkOptionMenu(self, values=env.high_schools, width=200, dropdown_fg_color="#343638",
                                           bg_color="#343638", fg_color="#343638", button_color="#343638",
                                           dynamic_resizing=False, text_color="gray")
        self.schoolbox.place(relx=0.38, rely=0.3)
        self.schoolbox.set("school")

        self.gradebox = ctk.CTkOptionMenu(self, values=env.grades, width=200, dropdown_fg_color="#343638",
                                          bg_color="#343638", fg_color="#343638", button_color="#343638",
                                          dynamic_resizing=False, text_color="gray")
        self.gradebox.place(relx=0.38, rely=0.42)
        self.gradebox.set("grade")

        self.errorMessage2 = ctk.CTkLabel(self, text="", text_color="red")
        self.errorMessage2.place(relx=0.38, rely=0.49)

        self.updateButton = ctk.CTkButton(self, text="Update", width=200, height=30,
                                          command=lambda: changeschoolgrade(self))
        self.updateButton.place(relx=0.38, rely=0.54)

        self.contacttitleLabel = ctk.CTkLabel(self, text="Contact Us", font=("courier new", 20))
        self.contacttitleLabel.place(relx=0.1, rely=0.62)
        self.contactLabel = ctk.CTkLabel(self, text="Phone: (813)-758-0531\n\t  Email: riyonpraveen23@gmail.com", font=("courier new", 17))
        self.contactLabel.place(relx=0.01, rely=0.68)

        self.doctitelLabel = ctk.CTkLabel(self, text="Code Documentation", font=("courier new", 20))
        self.doctitelLabel.place(relx=0.1, rely=0.8)
        self.docLabel = ctk.CTkLabel(self, text="https://github.com/skyy-rad/Tokened", font=("courier new", 15), cursor="hand2", text_color="#1b70cf")
        self.docLabel.place(relx=0.11, rely=0.85)
        self.docLabel.bind("<Button-1>", lambda e: openWebsite())

        self.authorLabel = ctk.CTkLabel(self, text="Riyon Praveen, Ignatius Martin, & Anay Patel © FBLA 2023", font=("courier new", 14))
        self.authorLabel.place(relx=0.24, rely=0.955)

        self.backIcon = ctk.CTkImage(dark_image=Image.open(env.img[0]), light_image=Image.open(env.img[0]),
                                     size=(25, 25))
        self.backButton = ctk.CTkButton(self, image=self.backIcon, text="", fg_color="#292929", height=25, width=25,
                                        hover_color="#212121", command=lambda: show_frame(self, controller, student))
        self.backButton.place(relx=0, rely=0)

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
                                        bg_color="#212121", hover_color="#292929", command=lambda: changepass(self))
        self.saveButton.place(relx=0.34, rely=0.52)

        self.helpImage = ctk.CTkImage(dark_image=Image.open(env.img[11]), light_image=Image.open(env.img[11]), size=(20, 20))
        self.helpButton = ctk.CTkButton(self.settingFrame, image=self.helpImage,text="", width=25, height=25, fg_color="#212121", bg_color="#212121", hover_color="#292929", command=lambda: show_frame(self, controller, helpPage))
        self.helpButton.place(relx=0.79, rely=0.87)

        self.menuImage = ctk.CTkImage(dark_image=Image.open(env.img[6]),
                                      light_image=Image.open(env.img[6]), size=(25, 25))
        self.menuButton = ctk.CTkButton(self, image=self.menuImage, text="", width=15, height=25, fg_color="#292929",
                                        bg_color="#292929",
                                        hover_color="#212121", command=lambda: menuOpen(self, True))
        self.menuButton.place(relx=0.95, rely=0)

        self.logoutImage = ctk.CTkImage(dark_image=Image.open(env.img[5]), light_image=Image.open(env.img[5]),
                                        size=(25, 25))
        self.logoutButton = ctk.CTkButton(self.settingFrame, image=self.logoutImage, text="", width=15, height=25,
                                          fg_color="#212121", bg_color="#212121", hover_color="#292929",
                                          command=lambda: logout(self, controller, False))
        self.logoutButton.place(relx=0.78, rely=0.93)

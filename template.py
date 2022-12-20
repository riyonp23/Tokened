import customtkinter as ctk


def show_frame(self, cont): # used to switch to next frame
    frame = self.frames[cont]
    # raises the current frame to the top
    frame.tkraise()


class student(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent) # make sure to put self. then variable name to use in the program
        self.titleLabel = ctk.CTkLabel(self, text="Template Page")
        self.titleLabel.place(relx=0.47, rely=0.2) # Use place and relx and rely to put elements on screen
        # Wiki page to custom tkinter: https://github.com/TomSchimansky/CustomTkinter/wiki

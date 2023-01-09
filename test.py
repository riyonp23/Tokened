#!python3

import tkinter as tk
from PIL import Image, ImageTk
import os


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Image Fading")
        self.label = tk.Label(self)
        self.label.pack()
        self.load_pictures()
        self.fadetime = 1  # time between alpha channel changes in ms
        self.fadestep = 5  # change to alpha channel
        self.curstep = 0  # the current step through the transparency

        self.im = None  # to hold the raw picture
        self.photo = None  # to hold the tk compatible picture

        self.after(self.fadetime, self.fade_in)

    def fade_in(self):
        if not self.im:
            self.load_picture()
        alpha = min(self.curstep * self.fadestep, 255)  # clamp to 255 maximum
        self.im.putalpha(alpha)
        self.photo = ImageTk.PhotoImage(self.im)
        self.label.configure(image=self.photo)
        self.curstep += 1
        print('fade in: %i' % alpha)
        if alpha == 255:
            self.curstep = 0
            self.after(3000, self.fade_out)  # wait three seconds then fade out
        else:
            self.after(self.fadetime, self.fade_in)

    def fade_out(self):
        alpha = max(255 - self.curstep * self.fadestep, 0)  # clamp to 0 minimum
        self.im.putalpha(alpha)
        self.photo = ImageTk.PhotoImage(self.im)
        self.label.configure(image=self.photo)
        self.curstep += 1
        print('fade out: %i' % alpha)
        if alpha == 0:
            self.curstep = 0
            self.im = None
            self.index += 1  # to use next picture
            if self.index >= len(self.filenames):
                self.index = 0
            self.after(3000, self.fade_in)  # wait three seconds then load next picture
        else:
            self.after(self.fadetime, self.fade_out)

    def load_picture(self):
        while True:
            file = open(self.filenames[self.index], mode='rb')
            try:  # if errors opening file as image, ignore and try next one
                self.im = Image.open(file)  # this is a lazy operation and only reads image header
                self.im.load()  # force image load here
                file.close()  # close the file
                print('loaded: %s' % self.filenames[self.index])
                break
            except:
                file.close()
                self.index += 1
                if self.index >= len(self.filenames):
                    self.index = 0

    def load_pictures(self):
        self.filenames = []
        for file in os.listdir():
            if file.rsplit('.', 1)[-1] not in ['db', 'py', 'pyw']:
                self.filenames.append(file)
        self.index = -1


if __name__ == '__main__':
    app = App()
    app.mainloop()

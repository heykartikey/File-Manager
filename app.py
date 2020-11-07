from tkinter import PhotoImage, Tk


class App(Tk):
    def __init__(self, title, min_width=700, min_height=300):
        super().__init__()

        self.title(title)
        self.minsize(min_width, min_height)

        # first parameter is True so that all future TopLevels have the
        # same icon as root window
        self.iconphoto(True, PhotoImage(file='images/icon.png'))

        # Binds F11 key to toggle fullscreen state of app
        self.bind('<Key-F11>', self.__toggleFullscreen)

    def __toggleFullscreen(self, event):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

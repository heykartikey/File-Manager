from tkinter import Tk


class App(Tk):
    def __init__(self, title, min_width=700, min_height=300):
        super().__init__()

        self.title(title)
        self.minsize(min_width, min_height)

        self.bind('<Key-F11>', self.__toggleFullscreen)

    def __toggleFullscreen(self, event):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

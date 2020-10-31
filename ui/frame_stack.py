from tkinter import Frame


class FrameStack(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.lastframe = None
        self.frames = dict()

    def push(self, cls, key):
        self.frames[key] = cls(self)
        self.frames[key].grid(row=0, column=0, sticky='nsew')

    def raise_frame(self, key):
        self.frames[key].lift()

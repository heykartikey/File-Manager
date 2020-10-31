from tkinter import Frame

from ui.button import Button
import ui.images as img


def create_folder():
    ...


def cut():
    ...


def copy():
    ...


def paste():
    ...


def delete():
    ...


def rename():
    ...


class Toolbar(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__draw_tools()

    def __draw_tools(self):
        self.newfolder = Button(self, text='New Folder', image=img.new_folder,
                                command=create_folder)

        self.cut = Button(self, text='Cut', image=img.cut, command=cut)
        self.copy = Button(self, text='Copy', image=img.copy, command=copy)
        self.paste = Button(self, text='Paste', image=img.paste, command=paste)
        self.delete = Button(self, text='Delete',
                             image=img.delete, command=delete)
        self.rename = Button(self, text='Rename',
                             image=img.cut, command=rename)

        for i, child in enumerate(self.winfo_children()):
            child.config(bg=self.cget('bg'), padx=5)
            child.grid(row=0, column=i)

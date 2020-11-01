from tkinter import Frame

import ui.images as img
from ui.button import Button


class Toolbar(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__draw_tools()

    def __draw_tools(self):
        self.newfolder = Button(self, text='New Folder', image=img.new_folder)

        self.cut = Button(self, state='disabled', text='Cut', image=img.cut)
        self.copy = Button(self, state='disabled', text='Copy', image=img.copy)
        self.paste = Button(self, state='disabled',
                            text='Paste', image=img.paste)
        self.delete = Button(self, state='disabled',
                             text='Delete', image=img.delete)
        self.rename = Button(self, state='disabled',
                             text='Rename', image=img.rename)

        for i, child in enumerate(self.winfo_children()):
            child.config(bg=self.cget('bg'), padx=5)
            child.grid(row=0, column=i)

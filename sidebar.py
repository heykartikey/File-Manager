from tkinter import Frame, Label


class Sidebar(Frame):
    __current = None

    def __init__(self, master, bg, activebg, folders, **kwargs):
        kwargs['bg'] = bg
        super().__init__(master, kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.bg = bg
        self.activebg = activebg

        self.__draw_widgets(*folders)

    def __draw_widgets(self, *folders):
        i = 0
        for icon, name in folders:
            Label(self, text=name, fg='#333', padx=7, anchor='w', image=icon, compound='left', bg=self.bg)\
                .grid(sticky='ew', row=i, column=0, ipady=4)
            i += 1

        # Changing bind tags for the child of Sidebar so that event could be
        # bind easily using bind_class method
        for child in self.winfo_children():
            tags = list(child.bindtags())
            tags[2] = 'SidebarLabel'
            child.bindtags(tuple(tags))

        # Let the first child be active by default
        self.__current = self.winfo_children()[0]
        self.__current.config(bg=self.activebg)

        self.bind_class('SidebarLabel', '<Enter>',
                        lambda e: e.widget.config(bg=self.activebg))
        self.bind_class('SidebarLabel', '<Leave>', self.__mouse_leave)

        self.bind_class('SidebarLabel', '<Button-1>', self.__markactive)

    def __mouse_leave(self, event):
        # Do not switch color if we leave Label that has already been marked active
        if not (widget := event.widget) is self.__current:
            widget.config(bg=self.bg)

    def __markactive(self, event):
        # Switch the active state whenever a label is clicked
        if not (widget := event.widget) is self.__current:
            self.__current.config(bg=self.bg)
            self.__current = widget

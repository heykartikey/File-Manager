from tkinter import Canvas, Frame, Scrollbar


class ScrollableFrame(Frame):
    '''Scrollable Frame Widget'''

    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs, bg='#fff')
        self.tkraise()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._canvas = Canvas(self, bg=self.cget('bg'))
        self._canvas.grid(row=0, column=0, sticky='nsew')
        self._canvas.columnconfigure(0, weight=1)

        self.__sbar = Scrollbar(self, orient='vertical',
                                command=self._canvas.yview)
        self.__sbar.grid(row=0, column=1, sticky='ns')

        self.window = Frame(self._canvas, bg='#fff')
        self.window.columnconfigure(0, weight=1)

        self._canvas.create_window((0, 0), window=self.window,
                                   anchor='nw', tags='inner')
        self._canvas.configure(yscrollcommand=self.__sbar.set)

        self.winfo_toplevel().bind("<Configure>", self.__resize)

    def __resize(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._canvas.itemconfig('inner', width=self._canvas.winfo_width())

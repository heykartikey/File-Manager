from tkinter import Canvas, Frame, Scrollbar


class ScrollableFrame(Frame):
    '''Scrollable Frame Widget'''

    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', 'white')

        super().__init__(master, **kwargs)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        vscrollbar = Scrollbar(self, orient='vertical')
        vscrollbar.grid(row=0, column=1, sticky='ns')

        canvas = Canvas(self, bd=0, highlightthickness=0, bg=kwargs['bg'])
        canvas.grid(row=0, column=0, sticky='nsew')

        vscrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vscrollbar.set)

        self.window = w = Frame(canvas)
        self.window.columnconfigure(0, weight=1)

        inner = canvas.create_window((0, 0), window=w, anchor='nw')

        def configure_window(event):
            r_width, r_height = w.winfo_reqwidth(), w.winfo_reqheight()
            canvas.config(scrollregion=f'0 0 {r_width} {r_height}')

            if r_width != canvas.winfo_width():
                canvas.config(width=r_width)

        self.window.bind('<Configure>', configure_window)

        def configure_canvas(event):
            if w.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(inner, width=canvas.winfo_width())

        canvas.bind('<Configure>', configure_canvas)

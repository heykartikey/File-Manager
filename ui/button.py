from tkinter import Button


class Button(Button):
    '''Flat Button widget'''

    def __init__(self, master=None, **kwargs):
        kwargs['relief'] = 'sunken'
        kwargs['anchor'] = 'nw'
        kwargs['bd'] = 0

        kwargs['highlightcolor'] = 'red'
        kwargs['highlightbackground'] = kwargs.get('bg', '#fff')

        kwargs.setdefault('compound', 'left')
        kwargs.setdefault('cursor', 'hand2')

        super().__init__(master, kwargs)

        self.bind('<Key-Return>', lambda event: self.invoke())

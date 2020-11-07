from tkinter import Button


class Button(Button):
    '''Flat Button widget'''

    def __init__(self, master=None, **kwargs):
        kwargs['relief'] = 'sunken'

        # When a button has sunken relief, the text inside goes slightly
        # towards right-bottom therefore I need to bring it back to its
        # original top-position to make it appear like it has a flat relief
        kwargs['anchor'] = 'n'

        # The reason behind using `relief: sunken` + `anchor: n` is that
        # it doesn't appear to animate when the button is clicked because
        # it already has `sunken` relief

        kwargs['bd'] = 0

        kwargs['highlightcolor'] = 'red'
        kwargs['highlightbackground'] = kwargs.get('bg', '#fff')

        kwargs.setdefault('compound', 'left')
        kwargs.setdefault('cursor', 'hand2')

        super().__init__(master, kwargs)

        # Let make this fire button fire event when 'Enter' key is
        # clicked while the button is focused
        self.bind('<Key-Return>', lambda event: self.invoke())

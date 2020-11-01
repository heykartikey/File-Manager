from tkinter import Frame, Label

from .images import file, folder


class ListLabel(Frame):
    _icon = {'file': file, 'dir': folder}
    _active_color = '#eee'

    _current = None

    def __init__(self, master, type, *texts, **kwargs):
        kwargs.setdefault('bg', '#fff')
        super().__init__(master, **kwargs)

        self._name = texts[0]

        Label(self, image=ListLabel._icon[type], bg=self.cget('bg'))\
            .pack(side='left')

        for txt in texts:
            Label(self, text=txt, anchor='w', bg=self.cget('bg'), width=10)\
                .pack(expand=True, side='left', fill='both')

        self.bind(
            '<Enter>',
            lambda e: self.child_config(bg=ListLabel._active_color)
        )
        self.bind('<Leave>', self.__mouse_leave)

        if ListLabel._current is None:
            ListLabel._current = self
            ListLabel._current.child_config(bg=ListLabel._active_color)

        # Changing bind tags for the child of this widget so that event could be
        # bind easily using bind_class method
        for child in self.winfo_children():
            tags = list(child.bindtags()) or []
            tags[1] = 'ListLabel'
            child.bindtags(tuple(tags))

    def child_config(self, **kwargs):
        for child in self.winfo_children():
            child.config(**kwargs)

    def __mouse_leave(self, event):
        if ListLabel._current == self:
            return

        self.child_config(bg=self.cget('bg'))

    @staticmethod
    def change_current(event):
        if ListLabel._current:
            ListLabel._current.child_config(bg=ListLabel._current.cget('bg'))

        ListLabel._current = event.widget.master
        ListLabel._current.child_config(bg=ListLabel._active_color)

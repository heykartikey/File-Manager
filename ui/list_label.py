from tkinter import Frame, Label

from .images import file, folder


class ListLabel(Frame):
    _icon = {'file': file, 'dir': folder}
    _active_color = '#eee'

    def __init__(self, master, type, *texts, **kwargs):
        super().__init__(master, **kwargs, bg='#fff')
        self._name = texts[0]

        Label(self, image=self._icon[type], bg=self.cget('bg'))\
            .pack(side='left')

        for txt in texts:
            Label(self, text=txt, anchor='w', bg=self.cget('bg'), width=10)\
                .pack(expand=True, side='left', fill='both')

        self.bind(
            '<Enter>',
            lambda e: self.child_config(bg=self._active_color)
        )
        self.bind('<Leave>', lambda e: self.child_config(bg=self.cget('bg')))

        for child in self.winfo_children():
            tags = list(child.bindtags()) or []
            tags[1] = 'ListLabel'
            child.bindtags(tuple(tags))

    def child_config(self, **kwargs):
        for child in self.winfo_children():
            child.config(**kwargs)

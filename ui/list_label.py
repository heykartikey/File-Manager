from tkinter import Frame, Label

from .images import file, folder


class ListLabel(Frame):
    _icon = {'file': file, 'dir': folder}

    active_color = '#eee'
    currently_selected = None

    def __init__(self, master, type, *texts, **kwargs):
        kwargs.setdefault('bg', '#fff')
        super().__init__(master, **kwargs)

        self.name = texts[0]

        Label(self, image=ListLabel._icon[type or 'dir'], bg=self.cget('bg'))\
            .pack(side='left')

        for txt in texts:
            Label(self, text=txt, anchor='w', bg=self.cget('bg'), width=16, activebackground='red')\
                .pack(expand=True, side='left', fill='both')

        if type is not None:
            self.bind(
                '<Enter>',
                lambda e: self.child_config(bg=ListLabel.active_color)
            )
            self.bind('<Leave>', self.__mouse_leave)

            if ListLabel.currently_selected is None:
                ListLabel.currently_selected = self
                ListLabel.currently_selected.child_config(
                    bg=ListLabel.active_color)

            # Changing bind tags for the child of this widget so that event
            # could be bind easily using bind_class method
            for child in self.winfo_children():
                tags = list(child.bindtags()) or []
                tags[1] = 'ListLabel'
                child.bindtags(tuple(tags))

    def child_config(self, **kwargs):
        for child in self.winfo_children():
            child.config(**kwargs)

    def __mouse_leave(self, event):
        if ListLabel.currently_selected is self:
            return

        self.child_config(bg=self.cget('bg'))

    @staticmethod
    def change_current(event):
        if (active_widget := ListLabel.currently_selected) is not None:
            active_widget.child_config(bg=active_widget.cget('bg'))

        ListLabel.currently_selected = event.widget.master
        ListLabel.currently_selected.child_config(bg=ListLabel.active_color)

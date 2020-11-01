import os
from tkinter import BooleanVar, Button, Entry, Frame, Label, PanedWindow, StringVar, Toplevel

from app import App

root = App('File Manager using Tkinter')

root.geometry('500x200')

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


# <header>

from toolbar import Toolbar

header = Toolbar(root, height=32, bg='#fff')
header.grid(row=0, column=0, sticky='ew')
# </header>

# <body>

body = PanedWindow(root, sashwidth=2)

# <body-sidebar>

from ui.images import (desktop, documents, downloads, gallery, home, music,
                       videos)

folders = [
    (home, 'Home'),
    (desktop, 'Desktop'),
    (documents, 'Documents'),
    (downloads, 'Downloads'),
    (music, 'Music'),
    (gallery, 'Pictures'),
    (videos, 'Videos')
]

from sidebar import Sidebar

sidebar = Sidebar(body, '#d9d9d9', 'orange', folders)
body.add(sidebar)
# </body-sidebar>

import os
from os.path import isdir, join as joinpath
from platform import system
from subprocess import call as file_call

from ui.frame_stack import FrameStack

if system() == 'Windows':
    def open_file(filepath):
        if isdir(filepath):
            draw_files(filepath)
        else:
            os.startfile(filepath)
else:
    def open_file(filepath):
        if isdir(filepath):
            draw_files(filepath)
        else:
            file_call(('xdg-open', filepath))

from datetime import datetime


def draw_files(dir):
    if dir == joinpath(path := os.path.expanduser('~'), 'Home'):
        os.chdir(path)
        print(f'Raised {dir}')
        content.raise_frame(path)
        return
    os.chdir(dir)

    if dir in content.frames:
        print(f'Raised {dir}')
        content.raise_frame(dir)
        return

    content.push(ScrollableFrame, dir)

    r = 0
    for name in os.listdir():
        stat = os.stat(joinpath(dir, name))
        s = stat[-4]
        t = stat[-2]
        ee = ListLabel(content.frames[dir].window, 'dir' if s ==
                       4096 else 'file', name, datetime.utcfromtimestamp(t), s)
        ee.grid(row=r, column=0, sticky='ew')
        r += 1

    if r == 0:
        Label(content.frames[dir].window, text="Empty Directory").pack(
            expand=True, fill='both')


# <body-content>


os.chdir(os.path.expanduser('~'))

from threading import Thread

from ui.list_label import ListLabel
from ui.scrollable_frame import ScrollableFrame

cbody = Frame(root)
cbody.grid_columnconfigure(0, weight=1)
cbody.grid_rowconfigure(1, weight=1)

ListLabel(cbody, 'dir', 'Name', 'Modification',
          'Size', bg="#eee").grid(sticky='ew', row=0, column=0)

content = FrameStack(cbody)
content.grid(sticky='nsew', row=1, column=0)

Thread(target=draw_files, args=[os.getcwd()], daemon=True).start()

body.add(cbody)

# </body-content>

body.paneconfig(sidebar, minsize=210)
body.grid(sticky='nsew', row=1, column=0, pady=(1, 0))
# </body>

body.bind_class('SidebarLabel',
                '<Button-1>',
                lambda e:
                    Thread(target=draw_files, daemon=True, args=[joinpath(
                        os.path.expanduser('~'), e.widget.cget('text'))]
                    ).start(),
                add=True)


def clicked(event):
    name = event.widget.master._name
    Thread(target=open_file, args=[joinpath(
        os.getcwd(), name)], daemon=True).start()


def enable_buttons(*buttons):
    global cutcopy

    for button in header.winfo_children()[1:]:
        button.config(state='disabled')

    if buttons[0] is None:
        return

    for button in buttons:
        button.config(state='normal')


body.bind_class('ListLabel', '<Double-Button-1>', clicked)
body.bind_class('ListLabel', '<Button-1>', ListLabel.change_current)
body.bind_class('ListLabel', '<Button-1>', lambda e:
                enable_buttons(header.cut, header.copy, header.rename, header.delete) if cutcopy.get() not in ('cut', 'copy') else None, add=True)


body.bind_class('SidebarLabel', '<Button-1>',
                lambda e: enable_buttons(None) if cutcopy.get() not in ('cut', 'copy') else None, add=True)


from tkinter.messagebox import askokcancel
from send2trash import send2trash

F = StringVar(root, value=None)
cutcopy = StringVar(root, value=None, name='cutcopy')

curr = None


def cut():
    F.set(joinpath(os.getcwd(), ListLabel._current._name))
    global curr
    curr = ListLabel._current
    cutcopy.set('cut')
    enable_buttons(header.paste)


header.cut.config(command=cut)


def copy():
    F.set(joinpath(os.getcwd(), ListLabel._current._name))
    global curr
    curr = ListLabel._current
    cutcopy.set('copy')
    enable_buttons(header.paste)


header.copy.config(command=copy)

from shutil import copyfile


def paste():
    action = cutcopy.get()
    cutcopy.set(None)
    enable_buttons(None)
    if os.getcwd() == os.path.dirname(F.get()):
        return

    if action == 'cut':
        global curr
        curr.destroy()
        curr = None

    (copyfile if action == 'copy' else os.rename)(
        F.get(), joinpath(os.getcwd(), os.path.basename(F.get())))

    ListLabel._current = None

    stat = os.stat(joinpath(os.getcwd(), os.path.basename(F.get())))
    s = stat[-4]
    t = stat[-2]
    r = len(os.listdir())
    if r == 1:
        content.frames[os.getcwd()].window.winfo_children()[0].destroy()

    ListLabel(content.frames[os.getcwd()].window, 'dir' if s ==
              4096 else 'file', os.path.basename(joinpath(os.getcwd(), os.path.basename(F.get()))), datetime.utcfromtimestamp(t), s).grid(row=r + 1, column=0, sticky='ew')


header.paste.config(command=paste)


def delete_file():
    F.set(joinpath(os.getcwd(), ListLabel._current._name))

    sure = askokcancel(
        'Confirmation', 'Are you sure you want to delete this?')

    enable_buttons(None)

    if sure:
        send2trash(F.get())
        ListLabel._current.destroy()
        ListLabel._current = None


header.delete.config(command=delete_file)


def rename_file():
    F.set(joinpath(os.getcwd(), ListLabel._current._name))

    dialog = Toplevel(root)
    dialog.title("Rename")
    dialog.transient(root)
    dialog.resizable(False, False)

    newname = StringVar(root)
    sure = BooleanVar(root, value=False)

    def yes():
        sure.set(True)
        dialog.destroy()

    Entry(dialog, textvariable=newname).pack(padx=5, pady=(5, 0))
    Button(dialog, command=yes).pack(side='right', padx=5, pady=(5, 0))

    dialog.grab_set()
    root.wait_window(dialog)
    dialog.grab_release()

    if sure.get():
        os.rename(F.get(), joinpath(os.getcwd(), newname.get()))
        ListLabel._current.winfo_children()[1].config(text=newname.get())
        ListLabel._current._name = newname.get()


header.rename.config(command=lambda: Thread(
    target=rename_file, daemon=True).start())

root.mainloop()

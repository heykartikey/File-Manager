import os
from tkinter import PanedWindow

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

# <body-content>


os.chdir(os.path.expanduser('~'))

from threading import Thread

from ui.list_label import ListLabel
from ui.scrollable_frame import ScrollableFrame

content = FrameStack(root)

Thread(target=draw_files, args=[os.getcwd()], daemon=True).start()

body.add(content)

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


body.bind_class('ListLabel', '<Double-Button-1>', clicked)

destroy = Thread(target=root.quit)
root.protocol('WM_DELETE_WINDOW', lambda: destroy.start())

root.mainloop()

destroy.join()

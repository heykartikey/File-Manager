import os
from ui.button import Button
from tkinter import BooleanVar, Entry, Frame, PanedWindow, StringVar, Toplevel

from app import App

root = App('File Manager using Tkinter')

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


# <header>

from toolbar import Toolbar

header = Toolbar(root, height=32, bg='#fff')
header.grid(row=0, column=0, sticky='ew')
# </header>

# <body>

body = PanedWindow(root, sashwidth=2, bd=0)

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

sidebar = Sidebar(body, '#D9D9D9', 'orange', folders)
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
utc = datetime.utcfromtimestamp

from glob import glob


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
    for name in glob('*'):
        file_path = joinpath(dir, name)
        size = f'{os.path.getsize(file_path)} Bytes'
        mtime = utc(os.path.getmtime(file_path))
        mtime = mtime.date()
        icon_type = 'dir' if isdir(file_path) else 'file'
        ListLabel(content.frames[dir].window, icon_type, name, mtime, size)\
            .grid(row=r, column=0, sticky='ew')
        r += 1

    print(dir, r)

# <body-content>


os.chdir(os.path.expanduser('~'))

from threading import Thread

from ui.list_label import ListLabel
from ui.scrollable_frame import ScrollableFrame

cbody = Frame(root)
cbody.grid_columnconfigure(0, weight=1)
cbody.grid_rowconfigure(1, weight=1)

ListLabel(cbody, None, 'Name', 'Modified', 'Size', bg="#999")\
    .grid(sticky='ew', row=0, column=0)

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


def double_clicked(event):
    name = event.widget.master.name
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


body.bind_class('ListLabel', '<Double-Button-1>', double_clicked)
body.bind_class('ListLabel', '<Button-1>', ListLabel.change_current)
body.bind_class('ListLabel', '<Button-1>', lambda e:
                enable_buttons(header.cut, header.copy, header.rename, header.delete) if cutcopy.get() not in ('cut', 'copy') else None, add=True)


body.bind_class('SidebarLabel', '<Button-1>',
                lambda e: enable_buttons(None) if cutcopy.get() not in ('cut', 'copy') else None, add=True)


from tkinter.messagebox import askyesno
from send2trash import send2trash

F = StringVar(root, value=None)
cutcopy = StringVar(root, value=None, name='cutcopy')

curr = None

from tkinter import messagebox


def create_folder():
    dialog = Toplevel(root)
    dialog.title("New Folder")
    dialog.transient(root)
    dialog.resizable(False, False)

    foldername = StringVar(root)
    sure = BooleanVar(root, value=False)

    def yes():
        sure.set(True)
        try:
            os.mkdir(joinpath(os.getcwd(), foldername.get()))
            dialog.destroy()
        except FileExistsError:
            messagebox.showerror("Folder already exists!",
                                 "A folder with same name is already present in the current directory. Try entering another name")
        except FileNotFoundError:
            messagebox.showerror("Invalid Name!",
                                 "A folder with same name is already present in the current directory. Try entering another name")

    Entry(dialog, textvariable=foldername).pack(padx=5, pady=(5, 0))
    Button(dialog, text='CREATE', command=yes).pack(
        side='right', padx=5, pady=5)

    dialog.grab_set()
    root.wait_window(dialog)
    dialog.grab_release()

    stat = os.stat(joinpath(os.getcwd(), foldername.get()))
    r = len(os.listdir())
    if sure.get():
        ListLabel(content.frames[os.getcwd()].window, 'dir', foldername.get(
        ), datetime.utcfromtimestamp(stat[-2]), stat[-4]).grid(row=r + 1, column=0, sticky='ew')


header.newfolder.config(command=create_folder)


def cut():
    F.set(joinpath(os.getcwd(), ListLabel.currently_selected.name))
    global curr
    curr = ListLabel.currently_selected
    cutcopy.set('cut')
    enable_buttons(header.paste)


header.cut.config(command=cut)


def copy():
    F.set(joinpath(os.getcwd(), ListLabel.currently_selected.name))
    global curr
    curr = ListLabel.currently_selected
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

    ListLabel.currently_selected = None

    stat = os.stat(joinpath(os.getcwd(), os.path.basename(F.get())))
    s = stat[-4]
    t = stat[-2]
    r = len(os.listdir())

    ListLabel(content.frames[os.getcwd()].window, 'dir' if s ==
              4096 else 'file', os.path.basename(joinpath(os.getcwd(), os.path.basename(F.get()))), datetime.utcfromtimestamp(t), s).grid(row=r + 1, column=0, sticky='ew')


header.paste.config(command=paste)


def delete_file():
    F.set(joinpath(os.getcwd(), ListLabel.currently_selected.name))

    sure = askyesno(
        'Confirmation', 'Are you sure you want to delete this?')

    if sure:
        send2trash(F.get())
        ListLabel.currently_selected.destroy()
        ListLabel.currently_selected = None


header.delete.config(command=delete_file)


def rename_file():
    F.set(joinpath(os.getcwd(), ListLabel.currently_selected.name))

    src, ext = os.path.splitext(os.path.basename(F.get()))

    dialog = Toplevel(root)
    dialog.title("Rename")
    dialog.transient(root)
    dialog.resizable(False, False)

    newname = StringVar(root)
    sure = BooleanVar(root, value=False)

    def yes():
        try:
            if src == newname.get():
                dialog.destroy()
                return

            newfile = joinpath(os.getcwd(), f'{newname.get()}{ext}')

            i = 1
            while os.path.exists(newfile):
                newfile = joinpath(os.getcwd(), f'{newname.get()}{i}{ext}')
                i += 1

            os.rename(F.get(), newfile)
            newname.set(os.path.basename(newfile))
            sure.set(True)
            dialog.destroy()
        except IsADirectoryError:
            messagebox.showerror("Error",
                                 "A folder with same name already exists")

    Entry(dialog, textvariable=newname).pack(padx=5, pady=(5, 0))
    Button(dialog, text='OK', command=yes).pack(
        side='right', padx=5, pady=5)

    dialog.grab_set()
    root.wait_window(dialog)
    dialog.grab_release()

    if sure.get():
        ListLabel.currently_selected.winfo_children()[1]\
            .config(text=newname.get())

        ListLabel.currently_selected.name = newname.get()


header.rename.config(command=rename_file)

root.bind('<Control-Shift-n>', lambda e: header.newfolder.invoke())
root.bind('<Control-Shift-N>', lambda e: header.newfolder.invoke())

root.bind('<Control-x>', lambda e: header.cut.invoke())
root.bind('<Control-X>', lambda e: header.cut.invoke())

root.bind('<Control-c>', lambda e: header.copy.invoke())
root.bind('<Control-C>', lambda e: header.copy.invoke())

root.bind('<Control-v>', lambda e: header.paste.invoke())
root.bind('<Control-V>', lambda e: header.paste.invoke())

root.bind('<Delete>', lambda e: header.delete.invoke())
root.bind('<F2>', lambda e: header.rename.invoke())

root.mainloop()

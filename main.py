# imports
import os, PIL.Image, PIL.ImageTk, tkinter.ttk
from tkinter import *
# functions
def iconLoader():
    drive_icon = PIL.Image.open(basepath+'/drive.png')
    drive_icon.thumbnail((size,size))
    drive_icon = PIL.ImageTk.PhotoImage(drive_icon)
    folder_icon = PIL.Image.open(basepath+'/folder.png')
    folder_icon.thumbnail((size,size))
    folder_icon = PIL.ImageTk.PhotoImage(folder_icon)
    file_icon = PIL.Image.open(basepath+'/file.png')
    file_icon.thumbnail((size,size))
    file_icon = PIL.ImageTk.PhotoImage(file_icon)
    return drive_icon, folder_icon, file_icon
def view(e, location, stem):
    stem.destroy()
    content = [[], []]
    items = os.listdir(location)
    for item in os.listdir(location):
        content[0].append(os.path.join(location, item))
        if os.path.isdir(os.path.join(location, item)):
            content[1].append('folder')
        if os.path.isfile(os.path.join(location, item)):
            content[1].append('file')
    display(content)
def display(content):
    stem = Frame(root)
    stem.pack(fill=BOTH, expand=1)
    mc = Canvas(stem)
    mc.pack(side=LEFT, fill=BOTH, expand=1)
    ms = tkinter.ttk.Scrollbar(stem, orient=VERTICAL, command=mc.yview)
    ms.pack(side=RIGHT, fill=Y)
    mc.configure(bg=bg, yscrollcommand=ms.set)
    mc.bind('<Configure>', lambda e: mc.configure(scrollregion=mc.bbox('all')))
    branch = Frame(mc)
    mc.create_window((0, 0), window=branch, anchor='nw')
    stem.configure(bg=bg)
    branch.configure(bg=bg)
    name, category = content
    r, c = 0, 0
    for item in range(len(content[0])):
        icon_choice = drive_icon if category[item]=='drive' else folder_icon if category[item]=='folder' else file_icon
        icon = Label(branch, image=icon_choice, bg=bg)
        icon.image = icon_choice
        icon.grid(row=r, column=c)
        item_name = name[item].split('\\')
        icon.bind("<Double-Button-1>", lambda e, d=name[item], s=stem: view(e, d, s))
        print_name = item_name[0] if not(item_name[len(item_name)-1]) else item_name[len(item_name)-1] if len(item_name[len(item_name)-1])<25 else item_name[len(item_name)-1][:24]+'...'
        label = Label(branch, font=(None, 10), text=print_name, bg=bg, fg=fg)
        label.grid(row=r+1, column=c)
        c += 1
        if not(c%per_row):
            c = 0
            r += 2
def drive():
    drives = ['%s:\\' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    content = [drives, ['drive' for d in range(len(drives))]]
    display(content)
# tkinter globals
size = 200
bg = '#ffffff'
fg = '#000000'
title = 'Radikl'
per_row = 7
basepath = 'E:\Important\Radikl\Radikl'
root = Tk()
root.title(title)
root.configure(bg=bg)
drive_icon, folder_icon, file_icon = iconLoader()
for cd in range(len(os.getcwd().split('\\'))-1):
    os.chdir('../')
drive()
root.mainloop()
# rough

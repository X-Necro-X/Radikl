# imports
import os, PIL.Image, PIL.ImageTk
from tkinter import *
# functions
def view(e, drive):
    print(os.listdir(drive))
def main():
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    drive_icon = PIL.Image.open(basepath+'/drive.png')
    drive_icon.thumbnail((size,size))
    img = PIL.ImageTk.PhotoImage(drive_icon)
    r, c = 0, 0
    for drive in drives:        
        icon = Label(root, image=img, bg=bg)
        icon.image = img
        icon.grid(row=r, column=c)
        icon.bind("<Double-Button-1>", lambda e, d=drive: view(e, d))
        label = Label(root, font=(None, 10), text=drive, bg=bg, fg=fg)
        label.grid(row=r+1, column=c)
        c += 1
        if not(c%7):
            c = 0
            r += 2
# tkinter globals
size = 200
bg = '#ffffff'
fg = '#000000'
title = 'Radikl'
basepath = 'E:\Important\Radikl\Radikl'
root = Tk()
root.title(title)
root.configure(bg=bg)
for cd in range(len(os.getcwd().split('\\'))-1):
    os.chdir('../')
main()
root.mainloop()
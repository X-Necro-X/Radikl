# imports
import os, sys, PIL.Image, PIL.ImageTk
from tkinter import *
# functions
def view(e, drive):
    print(drive)
def main():
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    drive_icon = PIL.Image.open(os.getcwd()+'/drive.png')
    drive_icon.thumbnail((200,200))
    img = PIL.ImageTk.PhotoImage(drive_icon)
    r, c = 0, 0
    for drive in drives:        
        icon = Label(root, image=img)
        icon.image = img
        icon.grid(row=r, column=c)
        icon.bind("<Double-Button-1>", lambda e: view(e, drive))
        label = Label(root, font=(None, 10), text=drive)
        label.grid(row=r+1, column=c)
        c += 1
        if not(c%7):
            c = 0
            r += 2
    root.update()
# tkinter globals
bg = '#ffffff'
fg = '#000000'
root = Tk()
root.title('Radikl')
root.attributes("-fullscreen", True)
# root.configure(bg=bg)
main()
root.mainloop()
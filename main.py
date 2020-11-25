import os, sys
from tkinter import *
bg = '#ffffff'
fg = '#000000'
root = Tk()
root.title('Radikl')
root.attributes("-fullscreen", True)
root.configure(bg=bg)
# root.mainloop()
drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
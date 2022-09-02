# from tkinter import *
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

btnExit = tk.Button(root, text='Exit')

btnExit.grid(row=0, column=0, sticky='s')
root.state('zoomed')
root.mainloop()
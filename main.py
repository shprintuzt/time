# -*- coding: utf-8 -*-
"""
Created on Sat May 11 15:57:21 2019

@author: T-GOTOH
"""

import tkinter as tk
from viewer import EntryLabel
#from canvas_extended import My_Canvas
#import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        self.main_part = EntryLabel(self.master)
        self.main_part.grid(row=0)
        self.master.bind("<Return>", self.main_part.show_entry_fields)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=1)

#        self.input_frame = tk.Frame(self.master)
#        self.input_frame.Label(master, text="First Name").grid(row=0)
#        self.input_frame.Label(master, text="Last Name").grid(row=1)
#        self.input_frame.jihou = tk.Entry(master)
#        self.input_frame.jihou["text"] = "jihou"
#        self.input_frame.jihou.pack(side="left")
#        self.input_frame.start = tk.Entry(master)
#        self.input_frame.start["text"] = "start"
#        self.input_frame.start.pack(side="left")

        self.show = tk.Button(self.button_frame)
        self.show["text"] = "Show"
        self.show["command"] = self.main_part.show_entry_fields
        self.show.grid(row=1, column=0)
        self.button_frame.quit = tk.Button(master,
                                          text='Quit',
                                          command=master.quit)
        self.button_frame.quit.grid(row=1, column=1)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:26:09 2019

@author: T-GOTOH
"""
import tkinter as tk


class EntryLabel(tk.Frame):
    def __init__(self, master, **kargs):
        super().__init__(master)
        self.jihou = TimeInput(self, text="時報")
        self.jihou.grid(row=0, columnspan=2)
        self.start = TimeInput(self, text="録音開始から時報までの経過時間")
        self.start.grid(row=1, columnspan=2)
        self.target = TimeInput(self, text="録音開始から鳴き声までの経過時間")
        self.target.grid(row=2, columnspan=2)
        self.result_l = tk.Label(self, text="鳴き声の発生時間", width=20).grid(row=3, column=0, columnspan=1)
        self.result = tk.Label(self, text="", width=20)
        self.result.grid(row=3, column=1, columnspan=1)

    def show_entry_fields(self, event=None):
        j = self.jihou.get()
        s = self.start.get()
        t = self.target.get()
        duration = timeDelta(s, t)
        result = timeAdd(j, duration)
        self.result["text"] = str(result[0]) + "時" + str(result[1]) + "分" + str(result[2]) + "秒"


def timeDelta(f, t):  # f: from, t: to
    h, m, s = 0, 0, 0
    s = t[2] - f[2]
    if t[2] < f[2]:
        t[1] -= 1
        s += 60
    m = t[1] - f[1]
    if t[1] < f[1]:
        t[0] -= 1
        m += 60
    h = t[0] - f[0]
    return h, m, s


def timeAdd(target, duration):
    h, m, s = 0, 0, 0
    s = target[2] + duration[2]
    if s >= 60:
        s -= 60
        m += 1
    m = target[1] + duration[1]
    if m >= 60:
        m -= 60
        h += 1
    h = target[0] + duration[0]
    return h, m, s


class TimeInput(tk.Frame):
    def __init__(self, master, text, **kargs):
        super().__init__(master)
        self.title = tk.Label(self, text=text, width=25).grid(row=0, column=0)
        self.h_ent = tk.Entry(self, width=5)
        self.h_ent.grid(row=0, column=1)
        self.h_l = tk.Label(self, text="時").grid(row=0, column=2)
        self.m_ent = tk.Entry(self, width=5)
        self.m_ent.grid(row=0, column=3)
        self.m_l = tk.Label(self, text="分").grid(row=0, column=4)
        self.s_ent = tk.Entry(self, width=5)
        self.s_ent.grid(row=0, column=5)
        self.s_l = tk.Label(self, text="秒").grid(row=0, column=6)

    def get(self):
        return int(self.h_ent.get()), int(self.m_ent.get()), int(self.s_ent.get())

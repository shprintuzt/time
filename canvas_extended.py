# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:35:54 2019

@author: T-GOTOH
"""
import tkinter as tk
import numpy as np
from models import Network_rr

class My_Canvas(tk.Canvas):
    def __init__(self, master, **kargs):
        super().__init__(master, **kargs)
        self.flag_rec = False
        self.flag_flush = False
        self.n_size = 20
        self.p_size = 5
        self.id = []
        self.time = []
        self.delta = []

        self.network_rr = Network_rr()
        self.rotor = [ self.create_oval(0,0,0,0,fill="black") for i in range(self.network_rr.node_num) ]
        self.pointer = [ self.create_line(0,0,0,0,fill="black") for i in range(self.network_rr.node_num) ]
#        self.nodes = np.array([ [100*np.cos(2*np.pi*i/5)+320, 100*np.sin(2*np.pi*i/5)+240] for i in range(5)])
#        print(self.nodes[:, 0]-320, self.nodes[:, 1]-240)
        self.drawing()

    def next_state(self):
        print("Transit to a next state.")
        self.network_rr.next_state()
        self.drawing()
    
    def start_sim(self):
        if self.flag_flush == False:
            self.flag_flush = True
            print("Start!")
            self.after(0, self.simulation)
    
    def simulation(self):
        if self.flag_flush == True:
            self.network_rr.next_state()
            self.drawing()
            self.after(50, self.simulation)
    
    def stop_sim(self):
        if self.flag_flush == True:
            print("Stop!")
            self.flag_flush = False
            
    def drawing(self):
        self.delete("all")
        
        n_num = self.network_rr.node_num
        RR = self.network_rr
        #draw edges from i to j
        i_j = [(i, j) for i in range(n_num) for j in range(n_num)]
        for i, j in i_j:
            if RR.E[i][j] == 1:
                x_i = RR.L[i][0] + self.p_size*RR.cos[i][j]
                y_i = RR.L[i][1] + self.p_size*RR.sin[i][j]
                x_j = RR.L[j][0] + self.p_size*RR.cos[i][j]
                y_j = RR.L[j][1] + self.p_size*RR.sin[i][j]
                self.create_line(x_i, y_i, x_j, y_j, fill="#FFFFFF")
                                 
        for i in range(n_num):
            # draw nodes
            if RR.V[i] == 0:
                self.create_rectangle(RR.L[i][0]-self.n_size / 2, RR.L[i][1]-self.n_size / 2,
                                      RR.L[i][0]+self.n_size / 2, RR.L[i][1]+self.n_size / 2,
                                      fill="#7F7F7F") # (x1, y1, x2, y2) x1 and y1 are upper-left, and x2 and y2 are lower-right
            else:
                self.create_rectangle(RR.L[i][0]-self.n_size / 2, RR.L[i][1]-self.n_size / 2,
                                      RR.L[i][0]+self.n_size / 2, RR.L[i][1]+self.n_size / 2,
                                      fill="#007700") # (x1, y1, x2, y2) x1 and y1 are upper-left, and x2 and y2 are lower-right
                                      
            #draw agents
            if i in RR.K:
                self.create_rectangle(RR.L[i][0]-self.n_size/2,
                                      RR.L[i][1]-self.n_size/2,
                                      RR.L[i][0]+self.n_size/2,
                                      RR.L[i][1]+self.n_size/2,
                                      fill="#33FF33")

            # draw pointers
            self.rotor[i] = self.create_oval(RR.L[i][0]-self.p_size,
                                             RR.L[i][1]-self.p_size,
                                             RR.L[i][0]+self.p_size,
                                             RR.L[i][1]+self.p_size,
                                             fill="#FFFFFF")
            self.tag_bind(self.rotor[i], '<ButtonPress-1>', self.p_next)
                                                 #  (x1, y1, x2, y2) x1 and y1 are upper-left, and x2 and y2 are lower-right
            t_x = RR.L[i][0] + (2*self.p_size)*RR.cos_p[i][RR.N[i][RR.pointer[i]]]
            t_y = RR.L[i][1] + (2*self.p_size)*RR.sin_p[i][RR.N[i][RR.pointer[i]]]
            s_x = RR.L[i][0]
            s_y = RR.L[i][1]
            self.pointer[i] = self.create_line(s_x, s_y, t_x, t_y,
                                               fill="#FF0000")
            self.tag_bind(self.pointer[i], '<ButtonPress-1>', self.p_next)

    def show_id(self):
        if len(self.id) == 0:
            RR = self.network_rr
            n_num = RR.node_num
            self.id = [ self.create_text(RR.L[i][0], RR.L[i][1]-self.n_size/2,
                                         fill="lightblue",
                                         font="system 10 bold",
                                         text="{0}".format(i)) for i in range(n_num) ]
    
    def hide_id(self):
        if len(self.id) != 0:
            n_num = self.network_rr.node_num
            for i in range(n_num):
                self.delete(self.id[0])
                del self.id[0]

    def show_time(self):
        if len(self.time) == 0:
            RR = self.network_rr
            n_num = RR.node_num
            RR.exp_time()
            self.time = [ self.create_text(RR.L[i][0], RR.L[i][1]-self.n_size/2,
                                           fill="yellow",
                                           font="system 10 bold",
                                           text="{0}".format(RR.Exp_time[i])) for i in range(n_num) ]
    
    def hide_time(self):
        if len(self.time) != 0:
            n_num = self.network_rr.node_num
            for i in range(n_num):
                self.delete(self.time[0])
                del self.time[0]
                
    def show_delta(self):
        if len(self.delta) == 0:
            RR = self.network_rr
            n_num = RR.node_num
            RR.exp_delta(25)
            self.delta = [ self.create_text(RR.L[i][0], RR.L[i][1]-self.n_size/2,
                                            fill="blue",
                                            font="system 10 bold",
                                            text="{0}".format(RR.Exp_delta[i])) if RR.Exp_delta[i] <= 0\
                           else self.create_text(RR.L[i][0], RR.L[i][1]-self.n_size/2,
                                            fill="red",
                                            font="system 10 bold",
                                            text="{0}".format(RR.Exp_delta[i])) for i in range(n_num) ]
    
    def hide_delta(self):
        if len(self.delta) != 0:
            n_num = self.network_rr.node_num
            for i in range(n_num):
                self.delete(self.delta[0])
                del self.delta[0]
    
    def p_next(self, event):
        RR = self.network_rr
        obj_id = np.argmin([ np.sqrt((event.x - RR.L[i][0])**2 + (event.y - RR.L[i][1])**2) for i in range(RR.node_num) ])
        self.network_rr.p_next(obj_id)
        self.delete(self.pointer[obj_id])
        t_x = RR.L[obj_id][0] + (2*self.p_size)*RR.cos_p[obj_id][RR.N[obj_id][RR.pointer[obj_id]]]
        t_y = RR.L[obj_id][1] + (2*self.p_size)*RR.sin_p[obj_id][RR.N[obj_id][RR.pointer[obj_id]]]
        s_x = RR.L[obj_id][0]
        s_y = RR.L[obj_id][1]
        self.pointer[obj_id] = self.create_line(s_x, s_y, t_x, t_y,
                                                fill="#FF0000")
        self.tag_bind(self.pointer[obj_id], '<ButtonPress-1>', self.p_next)
        if len(self.time) != 0:
            self.hide_time()
            self.show_time()

        
    
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
green = (0, 125, 0)
YELLOW = (255, 255, 0)
yellow = (125, 125, 0)
color_list = [[(0, 255, 0), (0, 125, 0)],#[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],
              [(255, 0, 0), (125, 0, 0)],
              [(0, 0, 255), (0, 0, 125)],
              [(255, 255, 0), (125, 125, 0)],
              [(255, 0, 255), (125, 0, 125)],
              [(0, 255, 255), (0, 125, 125)],
              [(255, 125, 0), (125, 60, 0)],
              [(125, 255, 0), (60, 125, 0)],
              [(255, 0, 125), (125, 0, 60)],
              [(125, 0, 255), (60, 0, 125)],
              [(0, 125, 255), (0, 60, 125)],
              [(0, 255, 125), (0, 125, 60)]]

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 23:45:35 2018

@author: T-GOTOH
"""

import numpy as np
#import matplotlib.pyplot as plt

class Network_rr():
    def __init__(self):#, n_num):
        grid_r = 5
        grid_c = 10
        self.node_num = grid_r * grid_c # number of nodes
        width = 50
        height = 50
        mergin = 50
        
        x = [ i*width+mergin for i in range(grid_c) ]
        y = [ i*height+mergin for i in range(grid_r) ]
        self.L = np.array([ [j, i] for i in y for j in x ]) # location (coordination) of nodes
#        self.L[:, 0] = np.array([(i % self.grid_c)*50+20 for i in range(self.node_num)])
#        self.L[:, 1] = np.array([(i // self.grid_c)*50+20 for i in range(self.node_num)])
        #L[i][0] = 200*np.cos(2*np.pi*i/node_num) + 320
        #L[i][1] = 200*np.sin(2*np.pi*i/node_num) + 240

        self.E = np.array([[0 for i in range(self.node_num)] for j in range(self.node_num)]) # edges
        self.E[:, :] = 0
        i_j = [(i, j) for i in range(self.node_num) for j in range(self.node_num)]
        for i, j in i_j:
            #if i != j: # complete graph
            #if i == (j-1) % self.node_num or i == (j+1) % self.node_num: # ring
            #if (i != 0 and i != node_num-1) and (i == (j-1) % node_num or i == (j+1) % node_num): # line
            if (i % grid_c != grid_c-1 and j == i+1) or (i / grid_c != grid_r-1 and j == i+grid_c): # grid
            #if i == (j-1) % node_num or i == (j+1) % node_num or i == (j-2) % node_num or i == (j+2) % node_num or i == (j-3) % node_num or i == (j+3) % node_num: # ring with degree 6 of each node
                self.E[i][j], self.E[j][i] = 1, 1
        
        self.N = [ [] for i in range(self.node_num) ] # neighbors
        for i, j in i_j:
            if self.E[i][j] == 1:
                self.N[i].append(j)
        
        self.agent_num = 1
        self.K = np.random.randint(0, self.node_num, self.agent_num) # location (node) of agents
        self.V = np.array([ 0 for i in range(self.node_num) ]) # boolean showing whether the node is explored or not. 1:explored, 0:not explored.
        self.V[self.K] = 1
        self.explored = 0 # the number of explored nodes

        self.flag = 0 # flag for what?
        self.pointer = [ np.random.randint(0, len(self.N[i])-1) for i in range(self.node_num) ]
        self.TS = []
        self.time_step = 0
        
        self.Exp_time = [ 0 for i in range(self.node_num) ] # exploration time from each node
        self.Exp_delta = [ 0 for i in range(self.node_num) ]

        self.cos = np.array([[0 for i in range(self.node_num)] for j in range(self.node_num)])
        self.sin = np.array([[0 for i in range(self.node_num)] for j in range(self.node_num)])
        self.cos_p = np.array([[0 for i in range(self.node_num)] for j in range(self.node_num)])
        self.sin_p = np.array([[0 for i in range(self.node_num)] for j in range(self.node_num)])
        for i, j in i_j:
            dx = self.L[i][0] - self.L[j][0]
            dy = self.L[i][1] - self.L[j][1]
            dz = np.sqrt(dx**2+dy**2)
            if dx == 0 and dy == 0:
                pass
            elif dx == 0:
                self.cos[i][j], self.sin[i][j] = -dy / dz, 0
                self.cos_p[i][j], self.sin_p[i][j] = 0, -dy / dz
            elif dy == 0:
                self.cos[i][j], self.sin[i][j] = 0, -dx / dz
                self.cos_p[i][j], self.sin_p[i][j] = -dx / dz, 0
            else:
                self.cos[i][j], self.sin[i][j] = -dy / dz, dx / dz
                self.cos_p[i][j], self.sin_p[i][j] = -dx / dz, -dy / dz

    def next_state(self): # compute a next configuration
        # increment round
        self.time_step = self.time_step + 1
        print(self.time_step)
        
        # simulation part
        for i in range(self.agent_num):
            cur = self.K[i]

            self.pointer[cur] = (self.pointer[cur] + 1) % len(self.N[cur])
            self.K[i] = self.N[cur][self.pointer[cur]]

            if self.V[self.K[i]] == 0:
                self.V[self.K[i]] = self.V[self.K[i]] + 1
                self.explored = self.explored + 1
    
    def exp_time(self): # compute exploration time from each node
        for i in range(self.node_num):
            K_tmp = i
            p_tmp = [ self.pointer[l] for l in range(self.node_num) ]
            V_tmp = [ 0 for l in range(self.node_num) ]
            e_time = 0
            
            while 0 in V_tmp:
                for j in range(self.agent_num):
                    cur = K_tmp
                    
                    p_tmp[cur] = (p_tmp[cur] + 1) % len(self.N[cur])
                    K_tmp = self.N[cur][p_tmp[cur]]
                    
                    if V_tmp[K_tmp] == 0:
                        V_tmp[K_tmp] = V_tmp[K_tmp] + 1
                
                e_time = e_time + 1
                
            self.Exp_time[i] = e_time
                
    def p_next(self, i): # shift a rotor of node i
        self.pointer[i] = (self.pointer[i] + 1) % len(self.N[i])
        
    def exp_delta(self, i): # compute how exp-time increases by changing one rotor
        self.exp_time()
        for j in range(self.node_num):
            K_tmp = i
            p_tmp = [ self.pointer[l] for l in range(self.node_num) ]
            p_tmp[j] = (p_tmp[j] + 1) % len(self.N[j])
            V_tmp = [ 0 for l in range(self.node_num) ]
            e_time = 0
            
            while 0 in V_tmp:
                for k in range(self.agent_num):
                    cur = K_tmp
                    
                    p_tmp[cur] = (p_tmp[cur] + 1) % len(self.N[cur])
                    K_tmp = self.N[cur][p_tmp[cur]]
                    
                    if V_tmp[K_tmp] == 0:
                        V_tmp[K_tmp] = V_tmp[K_tmp] + 1
                
                e_time = e_time + 1
                
            self.Exp_delta[j] = self.Exp_time[i] - e_time
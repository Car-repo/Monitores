#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:04:46 2022

@author: alumno
"""
from multiprocessing import Lock,Condition

class Table():
    
    def __init__(self, n, manager):
        self.mutex = Lock()
        self.size = n
        self.current_phil = None
        self.array = manager.list([False]*self.size)
        self.condicion = Condition(self.mutex)
        
    def verificar_tenedor(self):
        anterior, posterior = (self.current_phil-1)%self.size, (self.current_phil+1)%self.size
        return not(self.array[anterior] or self.array[posterior])
        
    def wants_eat(self, pid):
        self.mutex.acquire()
        self.condicion.wait_for(self.verificar_tenedor)
        self.array[pid] = True
        self.mutex.release()
        
    def wants_think(self, pid):     
        self.mutex.acquire()
        self.array[pid] = False
        self.condicion.notify_all()
        self.mutex.release()
        
    def set_current_phil(self, pid):
        self.current_phil = pid
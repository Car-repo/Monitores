#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 18:38:18 2022

@author: mat
"""
from multiprocessing import Lock,Condition,Value

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
        
        
        
class CheatMonitor():
    """
    Los filosofos 0 y 2 estan compinchados. Ninguno de ellos dejara de comer
    mientras el otro no se encuentre comiendo, por lo que el filosofo 1 nunca
    tendra los dos tenedores disponibles.
    
    Nota: valido para filosofos que no terminen.
    """
    
    def __init__(self):
        self.mutex = Lock()
        self.phil0_eating = Value('b', False)
        self.phil2_eating = Value('b', False)
        self.condicion = Condition(self.mutex)
        
    def is_eating(self, pid):
        self.mutex.acquire()
        if pid == 0:
            self.condicion.notify()
            self.phil0_eating.value = True
        elif pid == 2:
            self.condicion.notify()
            self.phil2_eating.value = True
        self.mutex.release()
        
    def wants_think(self, pid):
        self.mutex.acquire()
        if pid == 0:
            self.condicion.wait_for(lambda : self.phil2_eating.value)
            self.phil0_eating.value = False
        elif pid == 2:
            self.condicion.wait_for(lambda : self.phil0_eating.value)
            self.phil2_eating.value = False
        self.mutex.release()
    
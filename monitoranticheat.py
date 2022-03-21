#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 18:38:18 2022

@author: mat
"""
from multiprocessing import Lock,Condition,Value

class AnticheatTable():
    """
    Incorpora un mecanismo para prevenir la inanicion de cualquier filosofo.
    Cada filosofo primero comprueba si su compañero a la derecha esta hambriento,
    y despues espera a tener los dos tenedores disponibles antes de comer.
    Cuando proceda a comer avisa al resto de filosofos de que ya no esta hambriento.
    """
    
    def __init__(self, n, manager):
        self.mutex = Lock()
        self.size = n
        self.current_phil = None
        self.array = manager.list([False]*self.size)
        self.hungry = manager.list([False]*self.size)
        self.condicion = Condition(self.mutex)
        self.chungry = Condition(self.mutex)
        
    def verificar_tenedor(self):
        anterior, posterior = (self.current_phil-1)%self.size, (self.current_phil+1)%self.size
        return not(self.array[anterior] or self.array[posterior])
    
    def wants_eat(self, pid):
        self.mutex.acquire()
        self.hungry[pid] = True
        self.chungry.wait_for(lambda : not(self.hungry[(pid+1)%self.size]))
        self.condicion.wait_for(self.verificar_tenedor)
        self.array[pid] = True
        self.hungry[pid] = False
        self.chungry.notify_all()
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
    Los filosofos 0 y 2 estan compinchados. Intentaran sincronizarse para no dejar
    los tenedores disponibles al filosofo 1.
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
            self.condicion.wait_for(lambda : self.phil2_eating.value, 0.1)
            self.phil0_eating.value = False
        elif pid == 2:
            self.condicion.wait_for(lambda : self.phil0_eating.value, 0.1)
            self.phil2_eating.value = False
        self.mutex.release()
    
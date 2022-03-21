#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:30:25 2022

@author: mat
"""

from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
import time
import random
from monitorcheat import Table,CheatMonitor

NPHIL = 5
K = 100

def delay(n):
    time.sleep(random.random()/n)


def philosopher_task(num:int, table: Table, cheat:CheatMonitor):  
    
    table.set_current_phil(num)    
    while True:
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        table.wants_eat(num)
        if num == 0 or num == 2:
            cheat.is_eating(num)
        print (f"Philosofer {num} eating")
        delay(100)
        if num == 0 or num == 2:
            cheat.wants_think(num)
        table.wants_think(num)
        print (f"Philosofer {num} stops eating")
               
               
def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    cheat = CheatMonitor()
    philosofers = [Process(target=philosopher_task, args=(i,table,cheat)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()
        
if __name__ == '__main__':
    main()
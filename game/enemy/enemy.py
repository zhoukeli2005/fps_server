# -*- coding: utf-8 -*-
#======================================================================
#
# enemy.py - xxxx
#
#======================================================================

import enemies_data
import util.state_manager as state_manager
import util.timer as timer
import game.maps.astar as astar
import data

STATE_IDLE = "idle"
STATE_RUN = "run"
STATE_ATTACK = "attack"

#=================== Enemy & State Machine ===========================
class enemy(object):
    def __init__(self, name, x, z):
        self.__name = name
        self.__data = enemies_data.get_data(name)
        self.__statem = state_manager.istate_manager()
        self.__statem.register(STATE_IDLE, state_idle(self.__data))
        self.__statem.register(STATE_RUN, state_run(self.__data))
        self.__statem.register(STATE_ATTACK, state_attack(self.__data))
        self.__statem.change_to(STATE_IDLE, None)
        
        self.__data.pos = data.data()
        self.__data.pos.x = x
        self.__data.pos.z = z
        
    def update(self):
        self.__statem.update()
        
    def move_to(self, x, z):
        self.__statem.change_to(STATE_RUN, (x, z))
        
    
#=================== Idle ============================
class state_idle(state_manager.istate):
    def __init__(self, d):
        self.__data = d
        
    def enter(self, param):
        self.__enter_time = timer.gtimer.current()
        
    def update(self):
        now = timer.gtimer.current()
        delta = now - self.__enter_time
        if delta > 1000:
            pass
                
#================== Run ==========================
class state_run(state_manager.istate):
    def __init__(self, d):
        self.__data = d
        
    def enter(self, param):
        self.__target_x, self.__target_z = param
        self.__path = astar.path_find(self.__data.pos.x, self.__data.pos.z, self.__target_x, self.__target_z)
        self.__pos = 1
        print param
        print self.__data.pos
        print self.__path
    
    def re_enter(self, param):
        self.enter(param)
    
    def update(self, param):
        pass

#===================== Attack ========================
class state_attack(state_manager.istate):
    def __init__(self, d):
        self.__data = d

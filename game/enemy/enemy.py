# -*- coding: utf-8 -*-
#======================================================================
#
# enemy.py - xxxx
#
#======================================================================

import enemies_data
import misc.state_manager as state_manager
import misc.timer as timer
import game.maps.astar as astar
import data
import math

STATE_IDLE = "idle"
STATE_RUN = "run"
STATE_ATTACK = "attack"

ENEMY_ID = 1

#=================== Enemy & State Machine ===========================
class enemy(object):
    def __init__(self, name, x, z):
        
        global ENEMY_ID
        
        self.id = ENEMY_ID
        ENEMY_ID += 1
        
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
        if delta > 1:
            pass
                
#================== Run ==========================
class state_run(state_manager.istate):
    def __init__(self, d):
        self.__data = d
        
    def enter(self, param):
        self.__target_x, self.__target_z = param
        self.__path = astar.path_find(self.__data.pos.x, self.__data.pos.z, self.__target_x, self.__target_z)
        self.__pos = 1
        self.__last_time = timer.gtimer.current()
    
    def re_enter(self, param):
        self.enter(param)
    
    def update(self, param):
        delta_time = timer.gtimer.current() - self.__last_time
        self.__last_time = timer.gtimer.current()
        
        distance = delta_time * self.__data.walk_velocity
        print "distance", distance, delta_time
        
        next_pos = self.__path[self.__pos]
        delta_x = next_pos[0] - self.__data.pos.x
        delta_z = next_pos[1] - self.__data.pos.z
        
        L = delta_x * delta_x + delta_z * delta_z
        if distance * distance >= L:
            self.__data.pos.x = next_pos[0]
            self.__data.pos.z = next_pos[1]
            
            self.__pos += 1
            if self.__pos >= len(self.__path):
                self._statem.change_to(STATE_IDLE, None)
            return
        
        L = math.sqrt(L)
        distance = math.sqrt(distance)
        delta_x /= L
        delta_z /= L
        
        delta_x *= distance
        delta_z *= distance
        
        self.__data.pos.x += delta_x
        self.__data.pos.z += delta_z
        
        print "pos:", self.__data.pos

#===================== Attack ========================
class state_attack(state_manager.istate):
    def __init__(self, d):
        self.__data = d

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
import network.events
import network.packet
import game

STATE_IDLE = "idle"
STATE_RUN = "run"
STATE_ATTACK = "attack"

ENEMY_ID = 1

#=================== Enemy & State Machine ===========================
class enemy(object):
    def __init__(self, name, x, z):
        
        # id
        global ENEMY_ID        
        self.id = ENEMY_ID
        ENEMY_ID += 1        
        
        # set data        
        self.__name = name
        self.__data = enemies_data.get_data(name)
        self.__data.pos = data.data()
        self.__data.pos.x = x
        self.__data.pos.z = z
        self.__data.id = self.id
        
        # state machine
        self.__statem = state_manager.istate_manager()
        self.__statem.register(STATE_IDLE, state_idle(self.__data))
        self.__statem.register(STATE_RUN, state_run(self.__data))
        self.__statem.register(STATE_ATTACK, state_attack(self.__data))
        self.__statem.change_to(STATE_IDLE, None)
        
        # broadcast enemy born
        pkt = self.get_born_pkt()
        game.controller.gcontroller.broadcast(pkt)
        
    def update(self):
        self.__statem.update()
        
    def move_to(self, x, z):
        self.__statem.change_to(STATE_RUN, (x, z))
        
    def get_born_pkt(self):
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_BORN, 
                                    id = self.id, 
                                    name = self.__data.name, 
                                    x = self.__data.pos.x, 
                                    z = self.__data.pos.z)
        return pkt
        
    
#=================== Idle ============================
class state_idle(state_manager.istate):
    def __init__(self, d):
        self.__data = d
        
    def enter(self, param):
        print "enemy stop"
        self.__enter_time = timer.gtimer.current()
        
        # broadcast enemy stop
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_STOP, id = self.__data.id, x = self.__data.pos.x, z = self.__data.pos.z)
        game.controller.gcontroller.broadcast(pkt)
        
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
        
        if not self.__path:
            self._statem.change_to(STATE_IDLE, None)
            return
        
        # broadcast enemy run
        self.ibroadcast_run()
    
    def re_enter(self, param):
        self.enter(param)
    
    def update(self):
        now = timer.gtimer.current()
        delta_time = now - self.__last_time
        self.__last_time = now
        
        distance = delta_time * self.__data.walk_velocity * 0.001
        
        next_pos = self.__path[self.__pos]
        delta_x = next_pos[0] - self.__data.pos.x
        delta_z = next_pos[1] - self.__data.pos.z
        
        L = delta_x * delta_x + delta_z * delta_z
        if distance * distance >= L:    # reached next waypoint
            self.__data.pos.x = next_pos[0]
            self.__data.pos.z = next_pos[1]
            
            self.__pos += 1
            if self.__pos >= len(self.__path):
                self._statem.change_to(STATE_IDLE, None)
            
            # broadcast enemy run
            self.ibroadcast_run()
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
        
    def ibroadcast_run(self):        
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_RUN)
        pkt.id = self.__data.id
        pkt.x = self.__data.pos.x
        pkt.z = self.__data.pos.z
        pkt.velocity = self.__data.walk_velocity
        if self.__pos >= len(self.__path):
            pkt.next_x = pkt.x
            pkt.next_z = pkt.z
        else:
            pkt.next_x = self.__path[self.__pos][0]
            pkt.next_z = self.__path[self.__pos][1]
            
        game.controller.gcontroller.broadcast(pkt)

#===================== Attack ========================
class state_attack(state_manager.istate):
    def __init__(self, d):
        self.__data = d

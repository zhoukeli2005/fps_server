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
        import game.maps
        x, z = game.maps.maps.find_nearest_walkable(x, z)        
        self.__statem.change_to(STATE_RUN, (x, z))
        
    def get_born_pkt(self):
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_BORN, 
                                    id = self.id, 
                                    name = self.__data.name, 
                                    x = self.__data.pos.x, 
                                    z = self.__data.pos.z,
                                    next_x = self.__data.pos.x,
                                    next_z = self.__data.pos.z,
                                    velocity = 0)
        
        if self.__statem.get_curr_state_name() == STATE_RUN:
            run_pkt = self.__statem.get_curr_state().get_run_pkt()
            pkt.next_x = run_pkt.next_x
            pkt.next_z = run_pkt.next_z
            pkt.velocity = run_pkt.velocity
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
        if delta > 1000:
            pass
                
#================== Run ==========================
class state_run(state_manager.istate):
    def __init__(self, d):
        self.__data = d
        
    def enter(self, param):
        print "[enemy]", "start run"
        self.__target_x, self.__target_z = param
        self.__path = astar.path_find(self.__data.pos.x, self.__data.pos.z, self.__target_x, self.__target_z)
        self.__pos = 1
                
        if not self.__path:
            print "[enemy]", "not find path"
            self._statem.change_to(STATE_IDLE, None)
            return
        
        print "[enemy]", "find path, len:", len(self.__path)
        
        self.icalc_next()
        
        # broadcast enemy run
        self.ibroadcast_run()
    
    def re_enter(self, param):
        self.enter(param)
    
    def update(self):
        now = timer.gtimer.current()
        delta_time = now - self.__last_time

        distance = delta_time * self.__data.walk_velocity * 0.001
        
        if distance >= self.__L:    # reached waypoint
            self.__data.pos.x = self.__next_waypoint.x
            self.__data.pos.z = self.__next_waypoint.z
            
            self.__pos += 1
            if self.__pos >= len(self.__path):
                self._statem.change_to(STATE_IDLE, None)
                return
            
            self.icalc_next()
            
            # broadcast enemy run
            self.ibroadcast_run()
            return
              
        self.__data.pos.x = self.__last_waypoint.x + distance * self.__dir.x
        self.__data.pos.z = self.__last_waypoint.z + distance * self.__dir.z
        
        self.ibroadcast_run()
        
    def icalc_next(self):
        self.__last_time = timer.gtimer.current()
        
        curr_waypoint = self.__path[self.__pos - 1]
        next_waypoint = self.__path[self.__pos]
        
        delta_x = next_waypoint[0] - curr_waypoint[0]
        delta_z = next_waypoint[1] - curr_waypoint[1]
        
        L = delta_x ** 2 + delta_z ** 2
        L = math.sqrt(L)
        
        self.__dir = data.data(x = delta_x / L, z = delta_z / L)
        self.__last_waypoint = data.data(x = curr_waypoint[0], z = curr_waypoint[1])
        self.__next_waypoint = data.data(x = next_waypoint[0], z = next_waypoint[1])
        self.__L = L
        
        
    def ibroadcast_run(self):
        pkt = self.get_run_pkt()
        game.controller.gcontroller.broadcast(pkt)
        
    def get_run_pkt(self):
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
        return pkt

#===================== Attack ========================
class state_attack(state_manager.istate):
    def __init__(self, d):
        self.__data = d

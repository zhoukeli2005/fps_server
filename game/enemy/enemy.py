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
import util

STATE_IDLE = "idle"
STATE_RUN = "run"
STATE_FIRE = "fire"
STATE_BEATEN = "beaten"

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
        self.__data.last_fire_time = timer.gtimer.current()
        self.__data.target = None
        
        self.hp = 100
        
        # state machine
        self.__statem = state_manager.istate_manager()
        self.__statem.register(STATE_IDLE, state_idle(self.__data, self))
        self.__statem.register(STATE_RUN, state_run(self.__data, self))
        self.__statem.register(STATE_FIRE, state_fire(self.__data, self))
        self.__statem.register(STATE_BEATEN, state_beaten(self.__data, self))
        self.__statem.change_to(STATE_IDLE, None)
        
        # broadcast enemy born
        pkt = self.get_born_pkt()
        game.controller.gcontroller.broadcast(pkt)
        
    def update(self):
        self.__statem.update()
        
    def get_pos(self):
        return self.__data.pos
    
    def get_id(self):
        return self.__data.id
        
    def move_to(self, x, z):
        import game.maps
        x, z = game.maps.maps.find_nearest_walkable(x, z)        
        self.__statem.change_to(STATE_RUN, (x, z))
        
    def fire(self, x, z):
        self.__statem.change_to(STATE_FIRE, (x, z))
        
    def beaten(self, dir_x, dir_z):
        print "enemy beaten", dir_x, dir_z
        self.__statem.change_to(STATE_BEATEN, (dir_x, dir_z))
        
    def find_nearest_player(self):
        import game.controller
        dis = 0
        player = None
        for ply in game.controller.gcontroller.Players.values():
            d = abs(ply.pos.x - self.__data.pos.x) + abs(ply.pos.z - self.__data.pos.z)
            if not player or dis > d:
                player = ply
                dis = d
        if player:
            self.__data.target = player.name
            
        return player
    
    def find_player_in_fire_range(self):
        import game.controller
        dis = self.__data.fire_range ** 2
        for ply in game.controller.gcontroller.Players.values():
            d = (ply.pos.x - self.__data.pos.x) ** 2 + (ply.pos.z - self.__data.pos.z) ** 2
            if dis >= d:
                return ply
        return None
                
    def get_target(self):
        if not self.__data.target:
            return None
        import game.player
        ply = game.player.get_ply_by_name(self.__data.target)
        if not ply:
            self.__data.target = None
            
        return ply
    
    def clear_target(self):
        self.__data.target = None
            
        
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
    def __init__(self, d, e):
        self.__data = d
        self.__enemy = e
        
    def enter(self, param):
        # broadcast enemy stop
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_STOP, id = self.__data.id, x = self.__data.pos.x, z = self.__data.pos.z)
        game.controller.gcontroller.broadcast(pkt)
        
        ply = self.__enemy.get_target()
        if ply:
            self.__enemy.clear_target()
            self.__data.last_fire_time = timer.gtimer.current()
        
    def update(self):
        now = timer.gtimer.current()
        if now - self.__data.last_fire_time > self.__data.cd * 1000:
            ply = self.__enemy.find_nearest_player()
            if ply:
                self.__enemy.move_to(ply.pos.x, ply.pos.z)
                
        if now - self._enter_time > 500:
            import random, game.maps
            self.__enemy.move_to(random.randint(game.maps.maps.MinX, game.maps.maps.MaxX),
                                 random.randint(game.maps.maps.MinZ, game.maps.maps.MaxZ))
                
#================== Run ==========================
class state_run(state_manager.istate):
    def __init__(self, d, e):
        self.__data = d
        self.__enemy = e
        
    def enter(self, param):
        import game.maps.maps
        self.__target_x, self.__target_z =  game.maps.maps.find_nearest_walkable(param[0], param[1])
        self.__data.pos.x, self.__data.pos.z = game.maps.maps.find_nearest_walkable(self.__data.pos.x, self.__data.pos.z)
        self.__path = astar.path_find(self.__data.pos.x, self.__data.pos.z, self.__target_x, self.__target_z)
        self.__pos = 1
                
        if not self.__path:
            print "[enemy]", "not find path", self.__target_x, self.__target_z, param
            self._statem.change_to(STATE_IDLE, None)
            return
                
        self.icalc_next()
        
        # broadcast enemy run
        self.ibroadcast_run()
    
    def re_enter(self, param):
        self.enter(param)
    
    def update(self):
        # 1. check target
        target = self.__enemy.find_player_in_fire_range()
        if target:
            self.__enemy.clear_target()
            self.__enemy.fire(target.pos.x, target.pos.z)
            return;

        # 2. move
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
class state_fire(state_manager.istate):
    def __init__(self, d, e):
        self.__data = d
        self.__enemy = e
        
    def enter(self, param):
        self.__state = 0
        target_x, target_z = param
        
        self.__dir_x = target_x - self.__data.pos.x
        self.__dir_z = target_z - self.__data.pos.z
        
        self.__dir_x, self.__dir_z = util.normalize(self.__dir_x, self.__dir_z)
        
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_FIRE, 
                                    id = self.__data.id, 
                                    dir_x = target_x - self.__data.pos.x,
                                    dir_z = target_z - self.__data.pos.z)
        
        game.controller.gcontroller.broadcast(pkt)

    def update(self):
        now = timer.gtimer.current()
        if self.__state == 0 and now - self._enter_time > 500:
            self.__data.last_fire_time = now
            self.__state = 1
            import game.bullet
            pos = self.__data.pos
            game.bullet.create_bullet("enemy%d" % self.__data.id, 
                                      pos.x + self.__dir_x * 1.2,
                                      1.5, 
                                      pos.z + self.__dir_z * 1.2, 
                                      self.__dir_x,
                                      self.__dir_z,
                                      self.__data.bullet)
            
        if self.__state == 1 and now - self._enter_time > 1000:
            self._statem.change_to(STATE_IDLE, None)
            
            
#====================== Beaten ================================
class state_beaten(state_manager.istate):
    def __init__(self, d, e):
        self.__data = d
        self.__enemy = e
        
    def enter(self, param):
        
        self.__dir_x, self.__dir_z = util.normalize(param[0], param[1])
        
        self.__data.pos.x += self.__dir_x * 0.5
        self.__data.pos.z += self.__dir_z * 0.5
        
        pkt = network.packet.packet(network.events.MSG_SC_ENEMY_BEATEN, 
                                    id = self.__data.id, 
                                    x = self.__data.pos.x,
                                    z = self.__data.pos.z)
        
        game.controller.gcontroller.broadcast(pkt)

    def update(self):
        now = timer.gtimer.current()
        if now - self._enter_time > 500:
            # can not fire immediately
            self.__data.last_fire_time = now            
            self._statem.change_to(STATE_IDLE, None)
            
# -*- coding: utf-8 -*-
#======================================================================
#
# player.py - xxxx
#
#======================================================================
import constants
import data
import bag

def get_ply(conn):
    if hasattr(conn, "ply"):
        return conn.ply
    return None

def get_ply_by_name(name):
    import game.controller
    if not name in game.controller.gcontroller.Players:
        return None
    return game.controller.gcontroller.Players[name]

class player(object):
    def __init__(self, d, conn):
        self.name = d.name
        self.__conn = conn
        self.__state = constants.PLAYER_STATE_LOGIN
        conn.ply = self 
        self.bag = bag.bag(self)
        self.bag.add(constants.ItemBullet, 10000)
        self.dead = False
        self.pos = data.data(x = 1000, z = 1000)
        
        # data
        self.hero = "hero"
        self.weapon = constants.WeaponNormal
        self.run_distance = 0
        self.point = 0
        
            
    def send_packet(self, pkt):
        if self.__conn:
            self.__conn.send_packet(pkt)
            
    def add_run_distance(self, d):
        self.run_distance += d
        import network
        pkt = network.packet.packet(network.events.MSG_SC_ADD_RUN_DISTANCE, name = self.name, distance = d)
        self.send_packet(pkt)
        
    def add_point(self, d):
        self.point += d
        import network
        pkt = network.packet.packet(network.events.MSG_SC_ADD_POINT, name = self.name, point = d)
        self.send_packet(pkt)
                    
    def is_ok(self):
        return self.__state == constants.PLAYER_STATE_OK
    
    def set_ok(self):
        self.__state = constants.PLAYER_STATE_OK
        
    def get_state(self):
        return self.__state
    
    def update(self):
        pass
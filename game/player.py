# -*- coding: utf-8 -*-
#======================================================================
#
# player.py - xxxx
#
#======================================================================
import constants
import data

def get_ply(conn):
    if hasattr(conn, "ply"):
        return conn.ply
    return None

class player(object):
    def __init__(self, d, conn):
        self.name = d.name
        self.__conn = conn
        self.__state = constants.PLAYER_STATE_LOGIN
        conn.ply = self 
        self.hero = "hero"
        self.pos = data.data(x = 1000, z = 1000)
            
    def send_packet(self, pkt):
        if self.__conn:
            self.__conn.send_packet(pkt)
            
    def is_ok(self):
        return self.__state == constants.PLAYER_STATE_OK
    
    def set_ok(self):
        self.__state = constants.PLAYER_STATE_OK
        
    def get_state(self):
        return self.__state
    
    def update(self):
        pass
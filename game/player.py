# -*- coding: utf-8 -*-
#======================================================================
#
# player.py - xxxx
#
#======================================================================
import constants

def get_ply(conn):
    if hasattr(conn, "ply"):
        return conn.ply
    return None

class player(object):
    def __init__(self, data, conn):
        self.name = data.name
        self.__conn = conn
        self.__state = constants.PLAYER_STATE_LOGIN
        conn.ply = self 
        self.hero = "hero"
            
    def send_packet(self, pkt):
        if self.__conn:
            self.__conn.send_packet(pkt)
            
    def is_ok(self):
        return self.__state == constants.PLAYER_STATE_OK
    
    def set_ok(self):
        self.__state = constants.PLAYER_STATE_OK
    
    def update(self):
        pass
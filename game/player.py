# -*- coding: utf-8 -*-
#======================================================================
#
# player.py - xxxx
#
#======================================================================

class player(object):
    def __init__(self, data, conn):
        self.__name = data.name
        self.__conn = conn
            
    def send_packet(self, pkt):
        if self.__conn:
            self.__conn.send_packet(pkt)
    
    def update(self):
        pass
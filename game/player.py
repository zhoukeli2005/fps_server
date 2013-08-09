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
        
    def get_conn(self):
        return self.__conn
    
    def update(self):
        pass
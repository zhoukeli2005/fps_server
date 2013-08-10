# -*- coding: utf-8 -*-
#======================================================================
#
# controller.py - xxxx
#
#======================================================================

import network.network as network
import player
import network.events as events
import maps.maps as maps
import event_processor

class controller(network.net_callback):
    def __init__(self):
        print "init controller"
        network.init(self)
        self.Players = {}
        self.Enemies = {}
        self.__eventp = {}
        
        maps.load(".\\maps")
        
        # register event processor
        self.__eventp[events.MSG_CS_LOGIN] = event_processor.eventp_login()
        self.__eventp[events.MSG_CS_POSITION] = event_processor.eventp_position()
        
    
    # ============= connection & packet ========================
    def do_conn_comes(self, conn):
        pass
   
    def do_conn_close(self, conn):
        pass
    
    def do_packet(self, conn, pkt):
        if not pkt.flag in self.__eventp:
            raise Exception("No Event Processor For %d" % pkt.flag)
        ep = self.__eventp[pkt.flag]
        ep.run(conn, pkt)
        
    # ============== game logic =============================
    def update(self):
        
        if len(self.Enemies) < 1:
            # test : create an enemy
            
            import enemy.enemy as enemy
            self.Enemies[1] = enemy.enemy("e1", -2, 0)
        
        for enemy in self.Enemies.values():
            enemy.update()
            
        for ply in self.Players.values():
            ply.update()
            
    def broadcast(self, pkt):
        for ply in self.Players.values():
            ply.send_packet(pkt)
    
        
        
gcontroller = controller()
        


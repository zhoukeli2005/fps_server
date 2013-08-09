# -*- coding: utf-8 -*-
#======================================================================
#
# controller.py - xxxx
#
#======================================================================

import network.network as network
import player
import enemy.enemy
import network.events as events
import maps.maps as maps

class controller(network.net_callback):
    def __init__(self):
        print "init controller"
        network.init(self)
        self.Players = {}
        self.Enemies = {}
        
        maps.load(".\\maps")
        
        # create an enemy
        self.Enemies[1] = enemy.enemy.enemy("e1", -2, 0)
    
    # ============= connection & packet ========================
    def do_conn_comes(self, conn):
        pass
   
    def do_conn_close(self, conn):
        pass
    
    def do_packet(self, conn, pkt):
        print pkt.__dict__
        if pkt.flag == events.MSG_CS_LOGIN:
            print "login", pkt.name
            ply = player.player(pkt, conn)
            self.Players[pkt.name] = ply
            return
        
        if pkt.flag == events.MSG_CS_POSITION:
            print "position", pkt.x, pkt.z
            for enemy in self.Enemies.values():
                enemy.move_to(pkt.x, pkt.z)
            return
        
    # ============== game logic =============================
    def update(self):
        for enemy in self.Enemies:
            enemy.update()
            
        for ply in self.Players:
            ply.update()
            
    def broadcast(self, pkt):
        for ply in self.Players:
            conn = ply.get_conn()
            conn.send_packet(pkt)
    
        
        
gcontroller = controller()
        


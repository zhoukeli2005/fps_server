# -*- coding: utf-8 -*-
#======================================================================
#
# controller.py - xxxx
#
#======================================================================

import network.network as network
import network.events as events
import maps.maps as maps

class controller(network.net_callback):
    def __init__(self):
        print "init controller"
        network.init(self)
        self.Players = {}
        self.Enemies = {}
        self.Bullets = {}
        self.Items = {}
        self.__eventp = {}
        
        maps.load(".\\maps")
        
        # register event processor
        import game.event_processor.event_loginout as event_loginout
        import game.event_processor.event_player as event_player
        import game.event_processor.event_item as event_item
        
        self.__eventp[events.MSG_CS_LOGIN] = event_loginout.eventp_login()
        self.__eventp[events.MSG_CS_I_AM_OK] = event_loginout.eventp_iamok()
        self.__eventp[events.MSG_CS_LOGOUT] = event_loginout.eventp_logout()
        
        self.__eventp[events.MSG_CS_POSITION] = event_player.eventp_position()
        self.__eventp[events.MSG_CS_PLAYER_RUN] = event_player.eventp_run()
        self.__eventp[events.MSG_CS_PLAYER_STOP] = event_player.eventp_stop()
        self.__eventp[events.MSG_CS_PLAYER_MAGIC] = event_player.eventp_magic()
        self.__eventp[events.MSG_CS_PLAYER_CHANGE_WEAPON] = event_player.eventp_change_weapon()
        
        self.__eventp[events.MSG_CS_PLAYER_BULLET] = event_player.eventp_bullet()
        self.__eventp[events.MSG_CS_PLAYER_BULLET_END] = event_player.eventp_bullet_end()
        self.__eventp[events.MSG_CS_PLAYER_BULLET_HIT] = event_player.eventp_bullet_hit()
        
        self.__eventp[events.MSG_CS_PICK_ITEM] = event_item.eventp_pick()
    
    # ============= connection & packet ========================
    def do_conn_comes(self, conn):
        pass
   
    def do_conn_close(self, conn):
        ep = self.__eventp[events.MSG_CS_LOGOUT]
        ep.run(conn, None)
    
    def do_packet(self, conn, pkt):
        if not pkt.flag in self.__eventp:
            raise Exception("No Event Processor For %d" % pkt.flag)
        ep = self.__eventp[pkt.flag]
        ep.run(conn, pkt)
        
    # ============== game logic =============================
    def update(self):
        
        if len(self.Enemies) < 1:
            # test : create an enemy
            import random
            pos = ((-2, 0), (-10, 0))
            i = random.randint(0, 1)
            p = pos[i]
            self.born_enemy("e1", p[0], p[1])
            
        if len(self.Items) < 1:
            # test : create an item
            import item, constants
            item.create_item(constants.ItemBarrel, -2, 0)
        
        for enemy in self.Enemies.values():
            enemy.update()
            
        for ply in self.Players.values():
            ply.update()
            
    def broadcast(self, pkt, without_player_name = None):
        for ply in self.Players.values():
            if ply.is_ok() and ply.name != without_player_name:
                ply.send_packet(pkt)
                
    def born_enemy(self, name, x, z):
        import game.enemy.enemy as enemy
        e = enemy.enemy(name, x, z)
        self.Enemies[e.id] = e
    
        
        
gcontroller = controller()
        


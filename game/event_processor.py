# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

import data

class ieventp(object):
    def run(self, conn, pkt):
        raise Exception("must be implemented!")
    
class eventp_login(ieventp):
    def run(self, conn, pkt):
        name = pkt.name
        password = pkt.password
        print "login", name, password
        
        d = data.data()
        d.name = name                
                
        import game.player as player
        ply = player.player(d, conn)
        conn.ply = ply        
        
        import game.controller
        gcontroller = game.controller.gcontroller
        
        # save in gcontroller.Players
        gcontroller.Players[name] = ply
        
        # send enemy info
        for enemy in gcontroller.Enemies.values():
            pkt = enemy.get_born_pkt()
            ply.send_packet(pkt)
            
        # broadcast to other players
        
        # send other ply info
        
class eventp_position(ieventp):
    def run(self, conn, pkt):
        print "event position", pkt
        import game.controller
        gcontroller = game.controller.gcontroller
        for enemy in gcontroller.Enemies.values():
            enemy.move_to(pkt.x, pkt.z)
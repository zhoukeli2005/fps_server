# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

import data

users = {
         "netease001" : "163",
         "netease002" : "163",
         "netease003" : "163"
}

class ieventp(object):
    def run(self, conn, pkt):
        raise Exception("must be implemented!")
    
class eventp_login(ieventp):
    def run(self, conn, pkt):
        name = pkt.name
        password = pkt.password
        print "login", name, password
        
        import network
        pkt_back = network.packet.packet(network.events.MSG_SC_LOGIN, status = 0, err = "")
        
        if not name in users:
            print "no such user", name
            pkt_back.err = "no such user"
            conn.send_packet(pkt_back)
            return
        
        if users[name] != password:
            print "password error", password, users[name]
            pkt_back.err = "password error"
            conn.send_packet(pkt_back)
            return
        
        import game.controller
        gcontroller = game.controller.gcontroller
        
        if name in gcontroller.Players:
            print "already login", name
            pkt_back.err = "already login"
            conn.send_packet(pkt_back)
            return
               
        # build data
        d = data.data()
        d.name = name 
                  
                
        import game.player as player
        ply = player.player(d, conn)
        conn.ply = ply        
        
        # save in gcontroller.Players
        gcontroller.Players[name] = ply
        
        # send enemy info
        for enemy in gcontroller.Enemies.values():
            pkt = enemy.get_born_pkt()
            ply.send_packet(pkt)
            
        # send back success
        pkt_back.status = 1
        conn.send_packet(pkt_back)
        
        # broadcast to other players
        
        # send other ply info
        
class eventp_position(ieventp):
    def run(self, conn, pkt):
        print "[event] position", pkt
        import game.controller
        gcontroller = game.controller.gcontroller
        for enemy in gcontroller.Enemies.values():
            enemy.move_to(pkt.x, pkt.z)
# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

users = {
         "netease001" : "163",
         "netease002" : "163",
         "netease003" : "163"
}

import ieventp
import data

# ============== Event Login =====================
class eventp_login(ieventp.ieventp):
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
        
        # save in gcontroller.Players
        gcontroller.Players[name] = ply
        
        # send back success
        pkt_back.status = 1
        conn.send_packet(pkt_back)
        
        
#================== Event Logout ====================
class eventp_logout(ieventp.ieventp):
    def run(self, conn, _):
        import game.player as player
        ply = player.get_ply(conn)
        if not ply:
            return
        
        print "logout", ply.name
        
        # 1. remove from gcontroller
        import game.controller
        gcontroller = game.controller.gcontroller
        if ply.name in gcontroller.Players:
            del gcontroller.Players[ply.name]
            
        # 2. broadcast to everyone
        import network
        pkt = network.packet.packet(network.events.MSG_SC_OTHER_LOGOUT, name = ply.name)
        gcontroller.broadcast(pkt)
            
        
#================= Event I Am OK ============================
class eventp_iamok(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        
        ply = game.player.get_ply(conn)
        if not ply:
            return;
        
        print "set ok"
        ply.set_ok()
        
        import game.controller
        gcontroller = game.controller.gcontroller
        
        # 1. send enemy info
        for enemy in gcontroller.Enemies.values():
            pkt = enemy.get_born_pkt()
            ply.send_packet(pkt)
            
        # 2. broadcast to everyone without this ply
        import network
        pkt = network.packet.packet(network.events.MSG_SC_OTHER_LOGIN, name = ply.name, x = pkt.x, z = pkt.z, hero = ply.hero)
        gcontroller.broadcast(pkt, without_player_name = ply.name)
        
        # 3. sent other players info to this ply
        for other_ply in gcontroller.Players.values():
            if other_ply != ply:
                pkt = network.packet.packet(network.events.MSG_SC_OTHER_LOGIN, name = other_ply.name, hero = other_ply.hero, 
                                        x = 10000, z = 10000, dir_x = 1, dir_z = 1, velocity = 0)
                ply.send_packet(pkt)
        
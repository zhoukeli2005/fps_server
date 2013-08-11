# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

import ieventp
    
#================= Event Position ============================
class eventp_position(ieventp.ieventp):
    def run(self, conn, pkt):
        print "[event] position", pkt
        import game.controller
        gcontroller = game.controller.gcontroller
        for enemy in gcontroller.Enemies.values():
            enemy.move_to(pkt.x, pkt.z)
            
#================= Event Run ==============================
class eventp_run(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event player run, no such player:", ply.name
            return
        
        ply.pos.x = pkt.x
        ply.pos.z = pkt.z
        
        import network
        bpkt = network.packet.packet(network.events.MSG_SC_OTHER_RUN, 
                                     name = ply.name, x = pkt.x, z = pkt.z, dir_x = pkt.dir_x, dir_z = pkt.dir_z,
                                     velocity = pkt.velocity)
        import game.controller
        game.controller.gcontroller.broadcast(bpkt, ply.name)
        
#=================== Event Stop =======================================        
class eventp_stop(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event player stop, no such player:", ply.name
            return
        
        ply.pos.x = pkt.x
        ply.pos.z = pkt.z
        
        import network
        bpkt = network.packet.packet(network.events.MSG_SC_OTHER_STOP, name = ply.name, x = pkt.x, z = pkt.z)
        import game.controller
        game.controller.gcontroller.broadcast(bpkt, ply.name)
        
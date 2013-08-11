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
            return
        
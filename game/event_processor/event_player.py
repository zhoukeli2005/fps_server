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
        game.controller.gcontroller.broadcast(bpkt, without_player_name = ply.name)
        
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
        bpkt = network.packet.packet(network.events.MSG_SC_OTHER_STOP, name = ply.name, x = pkt.x, z = pkt.z, dir_x = pkt.dir_x, dir_z = pkt.dir_z)
        import game.controller
        game.controller.gcontroller.broadcast(bpkt, without_player_name = ply.name)
        
#===================== Event Magic ==========================================
class eventp_magic(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event player stop, no such player:", ply.name
            return
        
        import network
        bpkt = network.packet.packet(network.events.MSG_SC_OTHER_MAGIC, name = ply.name, magic = pkt.magic)
        import game.controller
        game.controller.gcontroller.broadcast(bpkt, without_player_name = ply.name)
        
#===================== Event Bullet ============================================

class eventp_bullet(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event bullet, no such player:", ply.name
            return
        
        # 1. broadcast to everyone
        import game.bullet
        game.bullet.create_bullet(ply.name, pkt.x, pkt.y, pkt.z, pkt.dir_x, pkt.dir_z)
        
        
       
        
#====================== Event Bullet End =====================================
class eventp_bullet_end(ieventp.ieventp):
    def run(self, conn, pkt):
        
        # [check] 1. player exist
        import game.player
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event bullet end, no such player:", ply.name
            return
        
        # [check] 2. bullet exist
        bid = pkt.id
        import game.controller
        gcontroller = game.controller.gcontroller
        
        if not bid in gcontroller.Bullets:
            print "[warning] event bullet end, no such bullet:", bid
            return
        
        # [check] 3. bullet -player auth
        d = gcontroller.Bullets[bid]
        if d.ply != ply.name:
            print "[warning] event bullet end, player name error", ply.name, d.ply
            return
        
        # 1. remove from server
        del gcontroller.Bullets[bid]
        
        # 2. broadcast to everyone
        import network
        bpkt = network.packet.packet(network.events.MSG_SC_OTHER_BULLET_END, id = bid)
        gcontroller.broadcast(bpkt)
        
        
#============================ Event Bullet Hit ====================================
class eventp_bullet_hit(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        
        # [check] 1. player exist
        ply = game.player.get_ply(conn)
        if not ply:
            print "[warning] event bullet hit, no such player:", ply.name
            return
        
        # [check] 2. bullet exist
        bid = pkt.id
        import game.controller
        gcontroller = game.controller.gcontroller
        
        if not bid in gcontroller.Bullets:
            print "[warning] event bullet hit, no such bullet:", bid
            return
        
        # [check] 3. bullet - player auth
        d = gcontroller.Bullets[bid]
        if d.ply[:5] == "enemy":
            # enemy bullet hit player
            pass
        
        if d.ply != ply.name:
            print "[warning] event bullet hit, player name error", ply.name, d.ply
            return
        
        import network
        
        eid = pkt.enemy
        other = pkt.player
        
        # 1. hit enemy
        if eid > 0:
            if not eid in gcontroller.Enemies:
                print "[warning] event bullet hit, not such enemy:", eid
                return
            enemy = gcontroller.Enemies[eid]
            enemy.hp -= 50
            if enemy.hp <= 0:
                print "enemy die", eid
                
                # 1. broadcast enemy die
                bpkt = network.packet.packet(network.events.MSG_SC_ENEMY_DEAD, id = eid)
                gcontroller.broadcast(bpkt)
                
                # 2. remove from server
                del gcontroller.Enemies[eid]
                
            return
        
        # 2. hit other player
        print "hit other player", other
                
            
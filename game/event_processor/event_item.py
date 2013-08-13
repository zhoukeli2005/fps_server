# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

import ieventp

class eventp_pick(ieventp.ieventp):
    def run(self, conn, pkt):
        import game.player
        
        ply = game.player.get_ply(conn)
        if not ply:
            return;
        
        item_id = pkt.id
        
        import game.controller
        gcontroller = game.controller.gcontroller
        
        if not item_id in gcontroller.Items:
            print "[warning] pick item", item_id, "not exist"
            return
        
        d = gcontroller.Items[item_id]
        
        # 1. check player has item?
        if ply.bag.count(d.tt) > 0:
            print "[warning] pick one item one time"
            return
        
        # 2. remove from server
        del gcontroller.Items[item_id]
        
        # 3. pick it
        ply.bag.add(d.tt, 1)
        
        print "[log] pick item ok,", ply.name, item_id, ply.bag.count(d.tt)
        
        # 4. broadcast pickup
        import network
        pkt = network.packet.packet(network.events.MSG_SC_ITEM_PICKED, id = item_id, uname = ply.name, tt = d.tt)
        gcontroller.broadcast(pkt)
        
        
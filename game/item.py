# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================

ITEM_ID = 0

def create_item(tt, x, z):
    import network, game
    global ITEM_ID
    ITEM_ID += 1
    bid = ITEM_ID
    
    # 1. save in server
    import data
    d = data.data(id = bid, tt = tt, x = x, z = z)
    game.controller.gcontroller.Items[bid] = d
        
    # 2. broadcast
    bpkt = network.packet.packet(network.events.MSG_SC_ITEM_BORN,
                                     id = bid,
                                     tt = tt,
                                     x = x, 
                                     z = z
                                )

    game.controller.gcontroller.broadcast(bpkt)
    
    return d

def get_born_pkt(item):
    import network
    pkt = network.packet.packet(network.events.MSG_SC_ITEM_BORN,
                                id = item.id,
                                tt = item.tt,
                                x = item.x,
                                z = item.z
                            )
    return pkt
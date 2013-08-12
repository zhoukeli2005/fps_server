# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================
BULLET_ID = 0

def create_bullet(name, x, y, z, dir_x, dir_z):
    import network, constants, game
    global BULLET_ID
    BULLET_ID += 1
    bid = BULLET_ID
    
    # 1. broadcast
    bpkt = network.packet.packet(network.events.MSG_SC_OTHER_BULLET,
                                     id = bid,
                                     name = name, 
                                     x = x, y = y, z = z, 
                                     dir_x = dir_x, dir_z = dir_z, 
                                     velocity = constants.BulletVelocity)

    game.controller.gcontroller.broadcast(bpkt)
    
    # 2. save in server
    import data
    d = data.data(ply = name, id = bid)
    game.controller.gcontroller.Bullets[bid] = d
        
    return d

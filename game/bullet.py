# -*- coding: utf-8 -*-
#======================================================================
#
# event_processor.py - xxxx
#
#======================================================================
BULLET_ID = 0

def create_bullet(name, x, y, z, dir_x, dir_z, tt, damage):
    import constants
    
    if tt == constants.BulletMelee:
        # melee attack
        __melee_attack(name, x, z, dir_x, dir_z, damage);
        return
        
    import network, game
 
    global BULLET_ID
    BULLET_ID += 1
    bid = BULLET_ID
    
    # 1. broadcast
    bpkt = network.packet.packet(network.events.MSG_SC_OTHER_BULLET,
                                     id = bid,
                                     name = name, 
                                     x = x, y = y, z = z, 
                                     dir_x = dir_x, dir_z = dir_z,
                                     tt = tt, 
                                     velocity = constants.BulletVelocity)

    game.controller.gcontroller.broadcast(bpkt)
    
    # 2. save in server
    import data
    d = data.data(ply = name, id = bid, dir_x = dir_x, dir_z = dir_z, damage = damage)
    game.controller.gcontroller.Bullets[bid] = d
        
    return d

def hit_enemy(name, eid, hp, dir_x, dir_z):
    import game, network
    gcontroller = game.controller.gcontroller
    if not eid in gcontroller.Enemies:
        print "[warning] event bullet hit, not such enemy:", eid
        return
    enemy = gcontroller.Enemies[eid]
    enemy.hp -= hp
    
    ply = None
    if name in gcontroller.Players:
        print "hit enemy", name, "add point"
        ply = gcontroller.Players[name]
        ply.add_point(hp * 0.3)
    
    if enemy.hp <= 0:
        print "enemy die", eid, name
        
        if ply:
            print "add point", hp
            ply.add_point(hp)
                
        # 1. broadcast enemy die
        bpkt = network.packet.packet(network.events.MSG_SC_ENEMY_DEAD, id = eid)
        gcontroller.broadcast(bpkt)
                
        # 2. remove from server
        del gcontroller.Enemies[eid]
        return
    enemy.beaten(dir_x, dir_z)

def hit_player(name, uname, hp, dir_x, dir_z):
    import game, network
    
    if name in game.controller.gcontroller.Players:
        from_ply = game.controller.gcontroller.Players[name]
        from_ply.add_point(hp * 1.5)
    
    # just broadcast
    pkt = network.packet.packet(network.events.MSG_SC_OTHER_BEATEN, name = uname, hp = hp, dir_x = dir_x, dir_z = dir_z)
    game.controller.gcontroller.broadcast(pkt)


def __melee_attack(name, x, z, dir_x, dir_z, damage):
    import game, constants
    melee_range = constants.MELEE_RANGE
    gcontroller = game.controller.gcontroller
    if name[:5] != "enemy":
        # not enemy, can attack enemy
        for enemy in gcontroller.Enemies.values():
            pos = enemy.get_pos()
            if abs(pos.x - x) <= melee_range and abs(pos.z - z) <= melee_range:
                hit_enemy(name, enemy.get_id(), damage, dir_x, dir_z)
            
    for ply in gcontroller.Players.values():
        pos = ply.pos
        if ply.name != name and abs(pos.x - x) <= melee_range and abs(pos.z - z) <= melee_range:
            hit_player(name, ply.name, damage, dir_x, dir_z)

# -*- coding: utf-8 -*-
#======================================================================
#
# enemy_born.py - xxxx
#
#======================================================================

BornPosition = [
                (-17, 6),
                (-12, 4),
                (-3, 5),
                (-8, 12),
                (-24, 20),
                (-10, 29),
                (-27, 29),
                (-18, 38),
                (-18, 13)
            ]

class enemy_born(object):
    
    def __init__(self):
        self.EnemyCount = 10
        self.TimeDelta = 1000
        self.last_time = 0
    
    def check_born(self):
        import game.controller, misc.timer
        now = misc.timer.gtimer.current()
        
        if now - self.last_time < self.TimeDelta:
            return
        
        gcontroller = game.controller.gcontroller
        if len(gcontroller.Enemies) > self.EnemyCount:
            return
        
        self.last_time = now
        
        import random
        i = random.randint(0, 1)
        if i == 0:
            name = "e1"
        else:
            name = "e2"
            
        global BornPosition
        i  = random.randint(0, len(BornPosition) - 1)
        p = BornPosition[i]
        
        gcontroller.born_enemy(name, p[0], p[1])
        
gEnemyBorn = enemy_born()
            
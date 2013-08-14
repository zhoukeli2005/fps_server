# -*- coding: utf-8 -*-
#======================================================================
#
# item_born.py - xxxx
#
#======================================================================

BornPosition = [
                (-5, 1),
                (-21, 1),
                (-16, 15.8),
                (-1.4, 22.9),
                (-25.7, 23.1),
                (-23.3, 33.4),
                (-8.7, 43.5)
            ]

class item_born(object):
    def __init__(self):
        self.last_time = 0
        self.TimeDelta = 8000
    
    def find_item_near(self, x, z, d):
        import game.controller
        for itm in game.controller.gcontroller.Items.values():
            if abs(itm.x - x) < 2 and abs(itm.z - z) < 2:
                return True
        return False
    
    def check_born(self):
        import misc.timer
        now = misc.timer.gtimer.current()
        
        if now - self.last_time < self.TimeDelta:
            return
        
        self.last_time = now
        
        import random
        global BornPosition
        i = random.randint(0, len(BornPosition) - 1)
        p = BornPosition[i]
        
        if self.find_item_near(p[0], p[1], 2):
            return
        
        import item, constants
        item.create_item(constants.ItemBarrel, p[0], p[1])
        
        
gItemBorn = item_born()
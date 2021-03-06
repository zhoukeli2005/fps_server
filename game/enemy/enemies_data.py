# -*- coding: utf-8 -*-
#======================================================================
#
# enemies_data.py - xxxx
#
#======================================================================

import data
import constants

Data = {
        "e1" : {
                "name" : "e1",
                "hp" : 200,
                "cd" : 3,
                "damage" : 50,
                "view_range" : 6,
                "fire_range" : 4,
                "bullet" : constants.BulletNormal, 
                "walk_velocity" : 3,
                "level" : 1,
                "exp" : 5
        },
        "e2" : {
                "name" : "e2",
                "hp" : 100,
                "cd" : 2,
                "damage" : 30,
                "view_range" : 5,
                "fire_range" : 2.5,
                "bullet" : constants.BulletMelee,
                "walk_velocity" : 2.1,
                "level" : 1,
                "exp" : 3
        }
}

def get_data(name):
    if not name in Data:
        print "no enemy:", name
        return None
    
    d = Data[name]
    
    out = data.data()

    for k, v in d.items():
        out[k] = v
        
    return out
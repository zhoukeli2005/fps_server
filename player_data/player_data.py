# -*- coding: utf-8 -*-
#======================================================================
#
# server.py - xxxx
#
#======================================================================

def save(ply):
    import constants
    fname = constants.DataPath + ply.name
    
    out = []
    
    out.append(ply.name)
    out.append(ply.hero)
    out.append("%d" % ply.weapon)
    out.append("%f" % ply.point)
    out.append("%f" % ply.run_distance)
    out.append(ply.bag.serialize())
    
    print out
    
    with open(fname) as f:
        f.writelines(out)

def load(uname):
    import constants, data.data, game.bag
    fname = constants.DataPath + uname
    out = data.data()
    
    with open(fname) as f:
        d = f.readlines()
        out.name = d[0]
        out.hero = d[1]
        out.weapon = int(d[2])
        out.point = float(d[3])
        out.run_distance = float(d[4])
        out.bag = game.bag.bag(None)
        out.bag.deserialize(d[5])
        
        print out
    return out

if __name__ == "__main__":
    pass

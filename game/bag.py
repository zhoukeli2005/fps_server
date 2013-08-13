# -*- coding: utf-8 -*-
#======================================================================
#
# player.py - xxxx
#
#======================================================================

import constants

class bag_cell(object):
    def __init__(self, i):
        self.__index = i
        self.__count = 0
        self.__item_type = None
        
    def count(self):
        return self.__count
    
    def item_type(self):
        return self.__item_type
    
    def add(self, item_type, count):
        if count <= 0:
            print "cell.add failed count <= 0", count
            return
        if self.__item_type and self.__item_type != item_type:
            print "cell add Failed", self.__item_type, item_type
            return
        self.__item_type = item_type
        self.__count += count
        
    def remove(self, item_type, count):
        if count <= 0 or count > self.__count:
            return
        if self.__item_type != item_type:
            return
        self.__count -= count
        if self.__count == 0:
            self.__item_type = None
        

class bag(object):
    
    def __init__(self, ply):
        self.__player = ply
        self.__bag_size = constants.BAG_SIZE
        self.__bag = [bag_cell(i) for i in xrange(self.__bag_size)]
        print self.__bag
        
    def add(self, item_type, count):
        if count <= 0:
            return False
        cell = self.__find_cell(item_type)
        if cell:
            cell.add(item_type, count)
            return True
        cell = self.__find_empty_cell()
        if not cell:
            return False
        cell.add(item_type, count)
        return True
        
    def count(self, item_type):
        cell = self.__find_cell(item_type)
        if not cell:
            return 0
        return cell.count()
        
    def __find_empty_cell(self):
        for cell in self.__bag:
            if cell.count() == 0:
                return cell
        return None
        
    def __find_cell(self, item_type):
        for cell in self.__bag:
            if cell.count() > 0 and cell.item_type() == item_type:
                return cell
        return None
    
    def remove(self, item_type, count):
        cell = self.__find_cell(item_type)
        if cell:
            cell.remove(item_type, count)
            
if __name__ == "__main__":
    b = bag(None)
    print b.add(1, 1)
    print b.count(1)
    print b.add(1, 1)
    print b.count(1)
            
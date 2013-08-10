# -*- coding: utf-8 -*-
#======================================================================
#
# server.py - xxxx
#
#======================================================================

import network.network as network
import game.controller

def main():
    
    # save in local stack
    net = network
    game_controller = game.controller.gcontroller
    
    # listen
    net.listener(32130)
    
    print "Init OK"

    # loop
    while True:
        net.loop(0.1)
        
        # do logical update
        game_controller.update()
      
# do the job!  
main()

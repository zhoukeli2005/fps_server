# -*- coding : utf-8 -*- 

import packet

MSG_CS_LOGIN        = 0x1001
MSG_CS_POSITION     = 0x1002    # for debug
MSG_CS_I_AM_OK      = 0x1003
MSG_CS_LOGOUT       = 0x1004

MSG_CS_PLAYER_RUN   = 0x1005
MSG_CS_PLAYER_STOP  = 0x1006
MSG_CS_PLAYER_MAGIC = 0x1007    # Cast Magic

MSG_CS_PLAYER_BULLET        = 0x1008
MSG_CS_PLAYER_BULLET_END    = 0x1009
MSG_CS_PLAYER_BULLET_HIT    = 0x1010


MSG_SC_LOGIN        = 0x2001
MSG_SC_ENEMY_BORN   = 0x2002
MSG_SC_ENEMY_STOP   = 0x2003
MSG_SC_ENEMY_RUN    = 0x2004
MSG_SC_ENEMY_DEAD   = 0x2005
MSG_SC_ENEMY_BEATEN = 0x2006
MSG_SC_ENEMY_FIRE   = 0x2007

MSG_SC_OTHER_LOGIN  = 0x2010
MSG_SC_OTHER_LOGOUT = 0x2011
MSG_SC_OTHER_RUN    = 0x2012
MSG_SC_OTHER_STOP   = 0x2013
MSG_SC_OTHER_MAGIC  = 0x2014

MSG_SC_OTHER_BULLET         = 0x2015
MSG_SC_OTHER_BULLET_END     = 0x2016
MSG_SC_OTHER_BULLET_HIT     = 0x2017


# =========== Client To Server ===================================
packet.register( MSG_CS_LOGIN,          ( "name:s", "password:s" ) )
packet.register( MSG_CS_POSITION,       ( "x:d", "z:d" ) )
packet.register( MSG_CS_I_AM_OK,        ( "x:d", "z:d" ) )
packet.register( MSG_CS_PLAYER_RUN,     ( "x:d", "z:d", "dir_x:d", "dir_z:d", "velocity:d" ) )
packet.register( MSG_CS_PLAYER_STOP,    ( "x:d", "z:d", "dir_x:d", "dir_z:d" ) )
packet.register( MSG_CS_PLAYER_MAGIC,   ( "magic:H", ) )
packet.register( MSG_CS_PLAYER_BULLET,  ( "x:d", "y:d", "z:d", "dir_x:d", "dir_z:d" ) )
packet.register( MSG_CS_PLAYER_BULLET_END,  ( "id:I", ) )
packet.register( MSG_CS_PLAYER_BULLET_HIT,  ( "id:I", "enemy:I", "player:s", "dir_x:d", "dir_z:d" ) )

# =========== Server To Client ===================================
packet.register( MSG_SC_LOGIN,          ( "status:i", "err:s" ) )
packet.register( MSG_SC_ENEMY_BORN,     ( "id:I", "name:s", "x:d", "z:d", "next_x:d", "next_z:d", "velocity:d" ) )
packet.register( MSG_SC_ENEMY_STOP,     ( "id:I", "x:d", "z:d" ) )
packet.register( MSG_SC_ENEMY_RUN,      ( "id:I", "x:d", "z:d", "next_x:d", "next_z:d", "velocity:d" ) )
packet.register( MSG_SC_ENEMY_DEAD,     ( "id:I", ) )
packet.register( MSG_SC_ENEMY_FIRE,     ( "id:I", "dir_x:d", "dir_z:d" ) )

packet.register( MSG_SC_OTHER_LOGIN,    ( "name:s", "x:d", "z:d", "hero:s") )
packet.register( MSG_SC_OTHER_LOGOUT,   ( "name:s", ) )
packet.register( MSG_SC_OTHER_RUN,      ( "name:s", "x:d", "z:d", "dir_x:d", "dir_z:d", "velocity:d" ) )
packet.register( MSG_SC_OTHER_STOP,     ( "name:s", "x:d", "z:d", "dir_x:d", "dir_z:d" ) )
packet.register( MSG_SC_OTHER_MAGIC,    ( "name:s", "magic:H" ) )
packet.register( MSG_SC_OTHER_BULLET,   ( "name:s", "id:I", "x:d", "y:d", "z:d", "dir_x:d", "dir_z:d", "velocity:d" ) )
packet.register( MSG_SC_OTHER_BULLET_END,  ( "id:I", ) )



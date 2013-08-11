# -*- coding : utf-8 -*- 

import packet

MSG_CS_LOGIN        = 0x1001
MSG_CS_POSITION     = 0x1002
MSG_CS_I_AM_OK      = 0x1003
MSG_CS_LOGOUT       = 0x1004

MSG_CS_PLAYER_RUN   = 0x1005
MSG_CS_PLAYER_STOP  = 0x1006

MSG_SC_LOGIN        = 0x2001
MSG_SC_ENEMY_BORN   = 0x2002
MSG_SC_ENEMY_STOP   = 0x2003
MSG_SC_ENEMY_RUN    = 0x2004

MSG_SC_OTHER_LOGIN  = 0x2005
MSG_SC_OTHER_LOGOUT = 0x2006
MSG_SC_OTHER_RUN    = 0x2007
MSG_SC_OTHER_STOP   = 0x2008

# =========== Client To Server ===================================
packet.register( MSG_CS_LOGIN,          ( "name:s", "password:s" ) )
packet.register( MSG_CS_POSITION,       ( "x:d", "z:d" ) )
packet.register( MSG_CS_I_AM_OK,        ( "x:d", "z:d" ) )

# =========== Server To Client ===================================
packet.register( MSG_SC_LOGIN,          ( "status:i", "err:s" ) )
packet.register( MSG_SC_ENEMY_BORN,     ( "id:I", "name:s", "x:d", "z:d", "next_x:d", "next_z:d", "velocity:d" ) )
packet.register( MSG_SC_ENEMY_STOP,     ( "id:I", "x:d", "z:d" ) )
packet.register( MSG_SC_ENEMY_RUN,      ( "id:I", "x:d", "z:d", "next_x:d", "next_z:d", "velocity:d" ) )
packet.register( MSG_SC_OTHER_LOGIN,    ( "name:s", "x:d", "z:d", "hero:s", "dir_x:d", "dir_z:d", "velocity:d") )
packet.register( MSG_SC_OTHER_LOGOUT,   ( "name:s", ) )
packet.register( MSG_SC_OTHER_RUN,      ( "name:s", "x:d", "z:d", "dir_x:d", "dir_z:d", "velocity:d" ) )
packet.register( MSG_SC_OTHER_STOP,     ( "name:s", ) )

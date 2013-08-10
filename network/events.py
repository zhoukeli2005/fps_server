# -*- coding : utf-8 -*- 

import packet

MSG_CS_LOGIN        = 0x1001
MSG_CS_POSITION     = 0x1002

MSG_SC_LOGIN        = 0x2001
MSG_SC_ENEMY_BORN   = 0x2002
MSG_SC_ENEMY_STOP   = 0x2003
MSG_SC_ENEMY_RUN    = 0x2004

# =========== Client To Server ===================================
packet.register( MSG_CS_LOGIN,      ( "name:s", "password:s" ) )
packet.register( MSG_CS_POSITION,   ( "x:d", "z:d" ) )

# =========== Server To Client ===================================
packet.register( MSG_SC_LOGIN,      ( "status:b", "err:s" ) )
packet.register( MSG_SC_ENEMY_BORN, ( "id:I", "name:s", "x:d", "z:d" ) )
packet.register( MSG_SC_ENEMY_STOP, ( "id:I", "x:d", "z:d" ) )
packet.register( MSG_SC_ENEMY_RUN,  ( "id:I", "x:d", "z:d", "next_x:d", "next_z:d", "velocity:d" ) )
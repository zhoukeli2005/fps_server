# -*- coding : utf-8 -*- 

import packet

MSG_CS_LOGIN = 0x1001
MSG_SC_LOGIN = 0x2001

MSG_CS_POSITION = 0x1002

packet.register(
    MSG_CS_LOGIN, 
    (
        "name:s", 
        "age:H", 
        "money:d"
    )
)

packet.register(
    MSG_SC_LOGIN, 
    (
        "status:b", 
        "err:s"
    )
)

packet.register(
    MSG_CS_POSITION,
    (
        "x:d",
        "z:d"
    )
)
(CONN, AUTH, DATA) = range(3)

ORDERED = [DATA, CONN, AUTH]
ALL = ORDERED

ERROR = {}
ERROR[CONN] = "connection"
ERROR[AUTH] = "authorization"
ERROR[DATA] = "data"

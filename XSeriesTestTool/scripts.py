def database_type():
	return "QSQLITE"

def create_session_table():
	return """CREATE TABLE IF NOT EXISTS session(
	Timestamp DATETIME,
	PacketID INTEGER NOT NULL)"""

def create_distinct_table():
	return """CREATE TABLE IF NOT EXISTS distinctpackets(
	ID INTEGER PRIMARY KEY,
	LastChanged DATETIME,
	Direction TEXT NOT NULL,
	Class TEXT NOT NULL,
	Data TEXT NOT NULL)"""

def drop_session_table():
	return "DELETE FROM session"

def drop_distinct_table():
	return "DELETE FROM distinctpackets"

def insert_session():
	return """INSERT INTO
	session(Timestamp, PacketID)
	VALUES(:date,:packetid)"""

def insert_distinct():
	return """INSERT INTO
	distinctpackets(LastChanged, Direction, Class, Data)
	VALUES(:date,:direction,:type,:contents)"""

def get_latest(packet_type):
	return """SELECT *
	FROM distinctpackets
	WHERE Class = '%s'
	AND Direction = 'incoming'
	ORDER BY ID DESC LIMIT 1""" % packet_type
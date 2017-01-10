#!/usr/bin/python

import MySQLdb

def mysql_conn(dbhost):
	user='root'
	passwd='MyPass'
	dbconn = MySQLdb.connect(host=dbhost, user=user, passwd=passwd, db='mysql', connect_timeout=5)
	dbcur = dbconn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	return dbconn, dbcur
def getUsers(dbhost):
	try:
		dbconn, dbcur = mysql_conn(dbhost)
		slavesql = "show slave status"
		dbcur.execute(slavesql)
		slavedata = dbcur.fetchall()
		if not slavedata:
			usersql = "select User, Host from mysql.user"
			dbcur.execute(usersql)
			userdb = dbcur.fetchall()
			db_usermap = []
			for user_host in  userdb:
				user = user_host['User']
				host = user_host['Host']
				if user and host:
					usermap = str("'" + user + "'"+ '@' + "'" + host + "'" )
					privssql = "show grants for %s" % (usermap)
					user_map = {}
					dbcur.execute(privssql)
					privdb = dbcur.fetchall()
					privlist = []
					for priv in privdb:
						grant = priv.values()
						privlist.append(grant[0])
					user_map[usermap]=privlist
				db_usermap.append(user_map)
			return db_usermap
		else:
			return None
		dbconn.close()
	except:
#		print "could not connect to %s" % (dbhost)
		return None

if __name__ == "__main__":
	host_priv = {}
	f = open('list_dbs', 'r+')
	for host in f.readlines():
		host=host.strip()
		db_usermap = getUsers(host)
		if db_usermap:
			host_priv[host]=db_usermap
	for dbhost in host_priv.keys():
		usermap_list  = host_priv[dbhost]
		for usermap in usermap_list:
			grant_list = usermap.values()[0]
			user_map = usermap.keys()[0]
			for grant in grant_list:
				print "%s|%s|%s" % (dbhost, user_map, grant)

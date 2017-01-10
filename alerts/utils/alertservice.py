#!/usr/bin/python

''' import modules and define globals '''

import sys, requests
import log
name = 'process'
logger = log.get_logger(name, "/var/log/domain/mysql_tool.log")


'''
Function for alertservice interaction. Takes team name and url to hit
makes at least 3 attempts before raising unreachable exception. 
Returns json data if success  and null if hits exception
'''

def json_from_service(team, url):
	attempts = 0 
	while attempts < 1:
		try:
			logger.info("""calling alertservice for the team: %s""" % (team))
			response = requests.get(url, timeout = 5)
			'''
			Enable below line if we want to log all responses from alert service to logger
			'''
#			logger.info("response from alertservice at %s:%s" % (url, response.json())) ## remove this once testing is done
			return response.json()
			break
		except:
			attempts += 1
	return None
'''
Function collects the list of checks/rules from alert service for the specific team name and extract the name of the rule alone. For example, ['CPU_Usage', 'Disk_IO', 'Disk_Usage', 'Inode_Usage', 'Memory_Usage', 'Mysql', 'Mysql_queries', 'Mysql_replication', 'Replication_lag', 'Slave_status_check', 'Slow_query', 'Swap_Usage'] is one of the possible outputs
'''
			
def getChecks(team, url):
	alert_response = json_from_service(team, url)
	if alert_response:
		check_list = []
		for rule in alert_response:
			check = rule['name']
			if isinstance(check, unicode):
				check = check.encode('ascii', 'ignore')
			check_list.append(check)
		return check_list
	else:
		return None

'''
Function gets the status of one particular rule/check in alertservice. Returns null if the output obtained was an empty list or no output was received from alertservice.
'''
def getRuleStat(team, url):
	alert_response = json_from_service(team, url)
	if type(alert_response) is list and len(alert_response)  > 0:
		return alert_response[0]
	else:
		return None



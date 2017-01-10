#!/usr/bin/python

# Importing the modules needed

import sys, requests, re
import log, alertservice

base_url = "http://10.47.0.149/fk-alert-service"
# This is alert service end point.  We can move it to some config file later

'''
Function collects the counters for specified team 
'''
def getCounters(team):
	ok_counter = 0
	warn_counter = 0
	crit_counter = 0
	unknown_counter = 0
	url = """%s/teams/%s/rules""" % (base_url, team)
	check_list = alertservice.getChecks(team, url)

	'''
	Collects the list of checks for the specified team. Proceeds if a valid list of checks/rules were obtained for the team. Else returns all counters as zero. The api from alert service gives a paginated output. So we define a random map named "stat" and breaks execution once the stat is an empty dictionary, which is actually the end of the data stream.
	'''

	if check_list:
		rule_stat = []
		for check in check_list:
			stat ={'randamkey': 'randamvalue'}
			indexval = 1
			while stat:
				url = """%s/teams/%s/nagiosRules/%s/hosts?pageSize=1&index=%d""" % (base_url, team, check, indexval)
				indexval += 1
				stat = alertservice.getRuleStat(team, url)
				if stat:
					rule_stat.append(stat)
					'''
					This is where we start counting. The rule data can be a map with list of values or a map with a single value
					'''
		for rule in rule_stat:
			if rule['lastCheck'] is list:
				listdata = rule['lastCheck']
				for item in listdata:
					if re.search(r'[Ww][Aa][Rr][Nn]', item):
						warn_counter += 1
					elif re.search(r'[Cc][Rr][Ii][Tt][Ii]', item):
						crit_counter += 1
					elif re.search(r'[oO][kK]', item):
						ok_counter += 1
					else:
						unknown_counter += 1
			elif re.search(r'[oO][kK]', rule['lastCheck']):
				ok_counter += 1
			elif re.search(r'[Ww][Aa][Rr][Nn]', rule['lastCheck']):
				warn_counter += 1
			elif re.search(r'[Cc][Rr][Ii][Tt][Ii]', rule['lastCheck']):
				crit_counter += 1
			else:
				unknown_counter += 1
	return ok_counter, warn_counter, crit_counter, unknown_counter
if __name__ == "__main__":
	#This is  test data only
	team = 'flo-wh-b2b-db'
	ok_counter, warn_counter, crit_counter, unknown_counter = getCounters(team)
	print ok_counter, warn_counter, crit_counter, unknown_counter

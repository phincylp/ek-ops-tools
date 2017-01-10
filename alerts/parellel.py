#!/usr/bin/python

# import all the required modiles
import multiprocessing
from multiprocessing import Pool, TimeoutError
from utils import alerts

# define global variables

# define the function to call the extenal functions

def getData(team_list):
	ok_counter, warn_counter, crit_counter, unknown_counter = alerts.getCounters(team_list)
	return ok_counter, warn_counter, crit_counter, unknown_counter
def getCounters(team_names):	
	ok = 0;	warn = 0; crit = 0; unknown = 0
	pool = Pool(processes=len(team_names))
	mapping = [pool.map(getData, team_names)]
	for team_data in mapping[0]:
		ok += int(team_data[0])
		warn += int(team_data[1])
		crit += int(team_data[2])
		unknown += int(team_data[3])
	return ok, warn, crit, unknown
if __name__ == '__main__':
	#This is test data only
	team_names=['flo-wh-b2b-db', 'erp-logis-db']
	getCounters(team_names)


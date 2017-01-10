#!/usr/bin/python

# import the required modules

import sys, requests, time, subprocess

base_url="http://hostname:4243/"
# Start functions

'''
This fucntion connects to the host(docker engine) and gets the API reponses as json
'''
class dockerenginedata:
	def getResponse_engine(self, url):
		endpoint = "%s%s" % (base_url, url)
		try:
			response = requests.get(endpoint)
			return response.json()
		except:
			return None
	def getcontProperty(self, data, param):
		if data:
			values_list=[]
			for values in data:
				values_list.append(values[param])
			return values_list
		else:
			return None
	def getoldContainer(self, data, age):
		created_list = self.getcontProperty(data, 'Created')
		old_containers = []
		for date in  created_list:
			if time.time() - date > age:
				for container in data:
					if container['Created'] == date:
						old_containers.append(container['Id'])
		return old_containers
	def getContainerAge(self, data):
		created_list = self.getcontProperty(data, 'Created')
		containers = []
		for date in created_list:
			container2uptime = {}
			uptime = time.time() - date
			for container in data:
				if container['Created'] == date:
					cotainerId = container['Id']
			container2uptime[cotainerId] = uptime
			containers.append(container2uptime)
		return containers
	def getContainerUptime(self, data):
		container_status_list=[]
		for container in data:
			container_ids = self.getcontProperty(data, 'Id')
		for ID in container_ids:
			container_status = {}
			for container in data:
				if container['Id'] == ID:
					status = container['Status']
				container_status[ID]=status
			container_status_list.append(container_status)
		return container_status_list



if __name__ == "__main__":
	#This is only testdata
	url = "containers/json"
	dockerdata = dockerenginedata()
	data = dockerdata.getResponse_engine(url)
	old_containers = dockerdata.getoldContainer(data, 43200)
	print old_containers
	containers = dockerdata.getContainerAge(data)
	print containers
	container_status_list = dockerdata.getContainerUptime(data)
	print container_status_list



#!/usr/bin/python3

import xmlrpc.client
import ssl

import os


def check_variables():

	if ("user" and "password") not in self.template:
		if "masterkey" not in self.template:
			return (False,"No authentication method found")
	else:
		ip_server = self.template["remote_ip"]
		context=ssl._create_unverified_context()
		c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
		ret=c.validate_user(self.template["user"],self.template["password"])
		if ret["status"]!=0:
			return(False,"User validation error")
		if not ret["return"][0]:
			return(False,"User validation error")
			
	return (True,"")
	
ret=check_variables()

# Cleaning process just in case this is a reinitalization

if ret[0]:
	
	if "user" in self.template:
		user=(self.template["user"],self.template["password"])
	else:
		user=self.template["masterkey"]	
	
	ip_server = self.template["remote_ip"]
	context=ssl._create_unverified_context()
	c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
	print(c.clean_exports_file(user,"NfsManager"))
	print(c.remove_mount_on_boot(user,"NfsManager","/net/server-sync"))
	print(c.clean_environment(user,"AutofsManager"))


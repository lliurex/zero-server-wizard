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

	if self.template["enable_data_replication"].lower() == "true":
		
		try:
			
			if self.template["export_nfs"]=="true":
				print(c.add_share(user,"NfsManager","/net/server-sync","127.0.0.1"))
				
			if self.template["mount_nfs"]=="true":
				print(c.configure_mount_on_boot(user,"NfsManager",self.template["nfs_ip"],"/net/server-sync"))
				
		except Exception as e:
			print(e)
			raise e		
		
	else:
		e=Exception()
		e.message=ret[1]
		raise e

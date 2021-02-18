#!/usr/bin/env python3

import xmlrpc.client
import ssl

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
	
#def check_variables


ret=check_variables()

if ret[0]:

	try:
		ip_server=self.template["remote_ip"]
		
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]

		context=ssl._create_unverified_context()
		c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
		
		#print c.get_methods('N4dProxy')
		#se necesitan las siguientes variables del n4d-proxy
		#INTERNAL_NETWORK
		#INTERNAL_MASK
		#SRV_IP
		#se necesitan las siguientes variables del n4d-dnsmasq
		#INTERNAL_DOMAIN

		print(c.load_exports(user,"N4dProxy"))
		
	except Exception as e:
		print(e)
		raise e
		
else:
	e=Exception()
	e.message=ret[1]
	raise e

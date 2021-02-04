#!/usr/bin/env python3

import xmlrpc.client
import ssl


def check_variables():
	
	if ("user" and "password") not in self.template:
		if "masterkey" not in self.template:
			return (False,"No authentication method found")
	else:	
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
		server=self.template["remote_ip"]
		
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]

		c=xmlrpclib.ServerProxy("https://"+server+":9779")
		
		print c.end_operations(user,"ZeroServerWizardManager")
		
	except Exception as e:
		print e
		raise e
		
else:
	e=Exception()
	e.message=ret[1]
	raise e

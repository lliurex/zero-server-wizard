#!/usr/bin/python
import xmlrpclib

def check_variables():
	
	if ("user" and "password") not in self.template:
		
		if "masterkey" not in self.template:
			
			return (False,"No authentication method found")

			
	else:	
		c=xmlrpclib.ServerProxy("https://"+self.template["remote_ip"]+":9779")
		ret=c.validate_user(self.template["user"],self.template["password"])
		if not ret[0]:
			return(False,"User validation error")
		


	return (True,"")
	
#def check_variables


ret=check_variables()

if ret[0]:

	try:

		server_ip = self.template["remote_ip"]
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]
		c = xmlrpclib.ServerProxy("https://"+server_ip+":9779")
		print c.configure_ldap_environment_client(user,"PamnssPlugin")
		print c.configure_ldap(user,"PamnssPlugin")
		print c.configure_nsswitch(user,"PamnssPlugin")

	except Exception as e:
		print e
		raise e
		
else:
	e=Exception()
	e.message=ret[1]
	raise e

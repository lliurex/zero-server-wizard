#!/usr/bin/python

import xmlrpclib
import os


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
	
ret=check_variables()

# Cleaning process just in case this is a reinitalization

print c.clean_exports_file(user,"NfsManager")
print c.remove_mount_on_boot(user,"NfsManager","/net/server-sync")
print.clean_environment(user,"AutofsManager")


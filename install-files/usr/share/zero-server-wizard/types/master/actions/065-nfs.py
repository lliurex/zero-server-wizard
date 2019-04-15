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
			
	for item in ["srv_ip","adminpassword","enable_data_replication","mount_nfs","export_nfs","nfs_ip"]:
		if item not in self.template:
			print("\t[065-nfs] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[065-nfs] [!]" + item + " is missing from template. Aborting initialization")
		
	return (True,"")
	
#def check_variables

ret=check_variables()

# Cleaning process just in case this is a reinitalization

print c.clean_exports_file(user,"NfsManager")
print c.remove_mount_on_boot(user,"NfsManager","/net/server-sync")
print c.clean_environment(user,"AutofsManager")


if self.template["enable_data_replication"].lower() == "true":
	if ret[0]:
		
		try:
			ip_server = self.template["remote_ip"]

			if "user" in self.template:
				user=(self.template["user"],self.template["password"])
			else:
				user=self.template["masterkey"]
		
			
			
			if self.template["export_nfs"]=="true":
				print c.add_share(user,"NfsManager","/net/server-sync","127.0.0.1")
				
			if self.template["mount_nfs"]=="true":
				print c.configure_mount_on_boot(user,"NfsManager",self.template["nfs_ip"],"/net/server-sync")
				
		except Exception as e:
			print e
			raise e		
		
	else:
		e=Exception()
		e.message=ret[1]
		raise e

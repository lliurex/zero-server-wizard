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
			
	for item in ["srv_ip","adminpassword","enable_data_replication","mount_from_master","nfs_ip"]:
		if item not in self.template:
			print("\t[065-nfs] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[065-nfs] [!]" + item + " is missing from template. Aborting initialization")
		
	return (True,"")
	
#def check_variables

ret=check_variables()

# Cleaning process just in case this is a reinitalization

print c.clean_exports_file(user,"NfsManager")
print c.remove_mount_on_boot(user,"NfsManager","/net/server-sync")


if self.template["enable_data_replication"].lower() == "true":
	if ret[0]:
		
		try:
			ip_server = self.template["remote_ip"]

			if "user" in self.template:
				user=(self.template["user"],self.template["password"])
			else:
				user=self.template["masterkey"]
		

			if not "remote_user" in self.template:
				self.template["remote_user"]="netadmin"
				self.template["remote_password"]=self.template["adminpassword"]


			remote_user=(self.template["remote_user"],self.template["remote_password"])

			
			if self.template["mount_from_master"]=="true":
				r=xmlrpclib.ServerProxy("https://10.3.0.254:9779")
				number_classroom = self.template["number_classroom"]
				ip='10.3.0.' + str(int(number_classroom))
				share="10.3.0.254:/net/server-sync"
				print r.add_share(remote_user,"NfsManager","/net/server-sync",ip)
				
				# OLD MOUNT VIA NFSMANAGER
				#print c.configure_mount_on_boot(user,"NfsManager",share,"/net/server-sync")
				
				print c.create_master_file(user,"AutofsManager","/net/server-sync","/etc/auto.lliurex")
				print c.create_mount_script(user,"AutofsManager","/etc/auto.lliurex","*",share+"/&")
				os.system("systemctl restart autofs")
				
				
			if self.template["mount_nfs"]=="true":
				print c.configure_mount_on_boot(user,"NfsManager",self.template["nfs_ip"],"/net/server-sync")
				
		except Exception as e:
			print e
			raise e		
		
	else:
		e=Exception()
		e.message=ret[1]
		raise e

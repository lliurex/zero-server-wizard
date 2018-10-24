#!/usr/bin/python

import xmlrpclib
import os.path


def check_variables():
	try:
		c=xmlrpclib.ServerProxy("https://"+self.template["remote_ip"]+":9779")
		if ("user" and "password") not in self.template:
		
			if "masterkey" not in self.template:
			
				return (False,"No authentication method found")

		else:	
			ret=c.validate_user(self.template["user"],self.template["password"])
			if not ret[0]:
				return(False,"User validation error")
		


		lst=["srv_name"]
		for item in lst:
			if item not in self.template:
				print("\t[010-hostname] [!]" + item + " is missing from template. Aborting initialization")
				return (False,"[010-hostname] [!]" + item + " is missing from template. Aborting initialization")
			
		return (True,"")
	except Exception as e:
		print e
		return(False,str(e))
	
#def check_variables

def print_reboot():
	print "Hostname has been changed. You need to reboot the machine before continuing."


ret=check_variables()

if ret[0]:
	
	try:
		ip_server = self.template["remote_ip"]
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]
		c=xmlrpclib.ServerProxy("https://"+ip_server+":9779")
		ret=c.get_hostname_file("","Hostname")
		if ret["status"]:
			
			if ret["HOSTNAME"]!=self.template["srv_name"]:
				
				c.set_hosts_file(user,"Hostname",self.template["srv_name"])
				c.set_hostname_file(user,"Hostname",self.template["srv_name"])
				c.set_hostname_n4d(user,"Hostname",self.template["srv_name"])
				f=open("/tmp/zsw.reboot","w")
				f.close()
				#print_reboot()
				#raise Exception
				
			
			elif ret["HOSTNAME"]==self.template["srv_name"] and not os.path.exists("/tmp/zsw.reboot"):
				
				ret2=c.get_hostname_n4d("","Hostname")
				if ret2["HOSTNAME"]!=self.template["srv_name"]:
					c.set_hostname_n4d(user,"Hostname",self.template["srv_name"])
				
				
			else:
				#print_reboot()
				#raise Exception
				pass
				
		else:
			print(ret["msg"])
			e=Exception()
			e.message=ret["msg"]
			raise e
		
		
	except Exception as e:
		print(e)
		raise e
	
	
else:
	e=Exception()
	print e
	e.message=ret[1]
	raise e

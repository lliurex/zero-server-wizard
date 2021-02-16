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
		


	lst=["srv_name","srv_domain_name","dns1","dns2"]
	for item in lst:
		if item not in self.template:
			print("\t[050-ldap] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[050-ldap] [!]" + item + " is missing from template. Aborting initialization")
			
	return (True,"")
	
#def check_variables

ret=check_variables()

if ret[0]:

	try:

		ip_server = self.template["remote_ip"]
		c = xmlrpclib.ServerProxy("https://"+ip_server+":9779")
		#c = xmlrpclib.ServerProxy("https://192.168.1.2:9779")
		
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]
		
		#se necesita inicializar previamente las siguientes variables del n4d-network
		#SRV_IP
		#INTERNAL_NETWORK
		#INTERNAL_MASK
		#INTERNAL_INTERFACE

		print c.configure_service(user,'DnsmasqManager',self.template["srv_domain_name"])
		print c.set_dns_external(user,'DnsmasqManager',[self.template["dns1"],self.template["dns2"]])
	except Exception as e:
		print e
		raise e
else:
	e=Exception()
	e.message=ret[1]
	raise e

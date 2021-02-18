#!/usr/bin/python3

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

	lst=["srv_name","srv_domain_name","dns1","dns2"]
	for item in lst:
		if item not in self.template:
			print("\t[050-dnsmasq] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[050-dnsmasq] [!]" + item + " is missing from template. Aborting initialization")
			
	return (True,"")
	
#def check_variables

ret=check_variables()


if ret[0]:

	try:

		ip_server = self.template["remote_ip"]
		context=ssl._create_unverified_context()
		c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
		rcontext=ssl._create_unverified_context()
		r = xmlrpc.client.ServerProxy('https://10.3.0.254:9779',context=context,allow_none=True)
		
		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]
		
		if not "remote_user" in self.template:
			self.template["remote_user"]="netadmin"

		self.template["remote_password"]=self.template["adminpassword"]
			
		remote_user = (self.template["remote_user"],self.template["remote_password"])
		number_classroom = self.template["number_classroom"]

		#se necesita inicializar previamente las siguientes variables del n4d-network
		#SRV_IP
		#INTERNAL_NETWORK
		#INTERNAL_MASK
		#INTERNAL_INTERFACE

		print(c.configure_service(user,'DnsmasqManager',self.template["srv_domain_name"]))
		print(c.set_dns_external(user,'DnsmasqManager',[self.template["dns1"],self.template["dns2"]]))
		print(c.set_dns_master_services(user,'DnsmasqManager'))
		print(r.add_node_center_model(remote_user,'DnsmasqManager',self.template["srv_name"],'10.3.0.' + str(int(number_classroom))))
		print(c.add_node_center_model(user,'DnsmasqManager','','10.3.0.254'))
	except Exception as e:
		print(e)
		raise e
else:
	e=Exception()
	e.message=ret[1]
	raise e

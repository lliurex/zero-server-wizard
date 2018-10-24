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
			
	for item in ["srv_ip","adminpassword"]:
		if item not in self.template:
			print("\t[020-ldap] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[020-ldap] [!]" + item + " is missing from template. Aborting initialization")
		
	return (True,"")
	
#def check_variables

ret=check_variables()

if ret[0]:
	
	try:
		ip_server = self.template["remote_ip"]

		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]

		c = xmlrpclib.ServerProxy("https://"+ip_server+":9779")
		print c.reset_slapd(user,"SlapdManager")
		print c.generate_ssl_certificates(user,"SlapdManager") 
		print c.load_lliurex_schema(user,"SlapdManager") 
		print c.enable_tls_communication(user,"SlapdManager",'/etc/ldap/ssl/slapd.cert','/etc/ldap/ssl/slapd.key') 
		print c.set_replicate_interface(user,'SlapdManager',self.template["external_iface"] + ':42')
		print c.configure_simple_slapd(user,"SlapdManager") 
		#Moved to 030
		#print c.load_acl(user,"SlapdManager")
		print c.open_ports_slapd(user,"SlapdManager",self.template["srv_ip"]) 
		print c.reboot_slapd(user,"SlapdManager") 
		print c.load_basic_struture(user,"SlapdManager")
		print c.change_admin_passwd(user,"SlapdManager",self.template["adminpassword"])
		print c.enable_folders(user,"SlapdManager")
		print c.set_serverid(user,'SlapdManager','254')
		print c.enable_replication_module(user,'SlapdManager')
		print c.enable_overlay_data(user,'SlapdManager')
		print c.enable_syncprov_checkpoint(user,'SlapdManager',100,10)
		print c.update_index(user,'SlapdManager','entryUUID eq',True)
		print c.update_index(user,'SlapdManager','entryCSN eq',True)
		print c.clean_master_server_ip(user,"SlapdManager")
	except Exception as e:
		print e
		raise e
	
else:
	e=Exception()
	e.message=ret[1]
	raise e

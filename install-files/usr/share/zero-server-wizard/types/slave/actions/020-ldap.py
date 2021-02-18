#!/usr/bin/python3

import xmlrpc.client
import ssl
import re


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
			
	for item in ["srv_ip","adminpassword"]:
		if item not in self.template:
			print("\t[020-ldap] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[020-ldap] [!]" + item + " is missing from template. Aborting initialization")
		
	return (True,"")
	
#def check_variables

ret=check_variables()
if ret[0]:
	
	try:
		number_classroom = str(int(self.template["number_classroom"]))
		ip_server = self.template["remote_ip"]

		if "user" in self.template:
			user=(self.template["user"],self.template["password"])
		else:
			user=self.template["masterkey"]
			
		if not "remote_user" in self.template:
			self.template["remote_user"]="netadmin"
		self.template["remote_password"]=self.template["adminpassword"]
			
		remote_user = (self.template["remote_user"],self.template["remote_password"])
		
		context=ssl._create_unverified_context()
		c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
		rcontext=ssl._create_unverified_context()
		r = xmlrpc.client.ServerProxy('https://10.3.0.254:9779',context=rcontext,allow_none=True)
		

		ret=r.get_variable('SAMBASID')
		if ret["status"]==0:
			REMOTESID = ret["return"]
		else:
			raise Exception(ret["msg"])


		if re.search('S(-[0-9]+)+',REMOTESID):
			print(c.set_sambasid(user,'SambaManager',REMOTESID))

		replication_iface=self.template["replication_iface"]
		# "(" as in (recommended) in zero-server-wizard combobox
		if "(" in replication_iface:
			replication_iface=external_iface

		print(c.reset_slapd(user,"SlapdManager"))
		print(c.generate_ssl_certificates(user,"SlapdManager"))
		print(c.load_lliurex_schema(user,"SlapdManager"))
		print(c.enable_tls_communication(user,"SlapdManager",'/etc/ldap/ssl/slapd.cert','/etc/ldap/ssl/slapd.key'))
		print(c.set_replicate_interface(user,'SlapdManager',replication_iface))
		print(c.configure_simple_slapd(user,'SlapdManager'))
		print(c.open_ports_slapd(user,"SlapdManager",self.template["srv_ip"]))
		print(c.reboot_slapd(user,"SlapdManager"))

		result = r.get_ldap_password(remote_user,'SlapdManager')
		if result["status"]!=0:
			raise Exception(result['msg'])
		ldap_password = result['return']
		print(c.change_admin_passwd(user,"SlapdManager",ldap_password))
		print(c.enable_folders(user,"SlapdManager"))
		ret = r.get_variable('LDAP_BASE_DN')
		if ret["status"]!=0:
			raise Exception(ret["msg"])
		aux_ldap_basedn = ret["return"]
		if aux_ldap_basedn == None:
			raise Exception('LDAP_BASE_DN is not defined on master server')
		print(c.add_rid_data_simple_sync(user,'SlapdManager','254','10.3.0.254',ldap_password,'cn=admin,' + str(aux_ldap_basedn),str(aux_ldap_basedn)))
		print(c.add_updateref_data(user,'SlapdManager','10.3.0.254'))
		print(c.set_master_server_ip(user,'SlapdManager','10.3.0.254'))
	except Exception as e:
		print(e)
		raise e
	
else:
	e=Exception()
	e.message=ret[1]
	raise e

#!/usr/bin/python

import xmlrpclib
import os.path


def check_variables():
	
	if ("user" and "password") not in self.template:
		
		if "masterkey" not in self.template:
			
			return (False,"No authentication method found")

			
	else:	
		c=xmlrpclib.ServerProxy("https://"+self.template["remote_ip"]+":9779",allow_none=True)
		ret=c.validate_user(self.template["user"],self.template["password"])
		if not ret[0]:
			return(False,"User validation error")
		


	lst=["external_iface","internal_iface","srv_ip","internal_mask","external_mask","external_ip","external_gateway","external_mode"]
	for item in lst:
		if item not in self.template:
			print("\t[015-network] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[015-network] [!]" + item + " is missing from template. Aborting initialization")
			
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
		c=xmlrpclib.ServerProxy("https://"+ip_server+":9779",allow_none=True)

		internal_iface=self.template["internal_iface"]
		internal_mask=self.template["internal_mask"]
		
		external_mask=self.template["external_mask"]
		external_mode=self.template["external_mode"]
		external_gateway=self.template["external_gateway"]
		external_ip=self.template["external_ip"]
		external_iface=self.template["external_iface"]
		external_dns_search = self.template["srv_domain_name"]
		srv_ip=self.template["srv_ip"]

		print c.load_network_file(user,'NetworkManager')
		# print c.delete_interfaces_in_range(user,'NetworkManager','10.3.0.0/24')
		print c.set_replication_interface(user,'NetworkManager',None, None, None, False)
		print c.set_internal_interface(user,'NetworkManager',internal_iface)
		print c.set_external_interface(user,'NetworkManager',external_iface)
		
		print c.interface_static(user,'NetworkManager',internal_iface,srv_ip,internal_mask,None,external_dns_search)
		
		if external_mode=="dhcp":
			print c.interface_dhcp(user,'NetworkManager',external_iface)
		else:
			print c.interface_static(user,'NetworkManager',external_iface,external_ip,external_mask,external_gateway,external_dns_search)
	
		# DISABLING PROXY BY DEFAULT
		if c.get_variable("","VariablesManager","CLIENT_PROXY_ENABLED")==None:
			print c.add_variable(user,'VariablesManager','CLIENT_PROXY_ENABLED',False,"","Variable to enable or disable proxy in classroom clientes",[])
		else:
			print c.set_variable(user,"VariablesManager","CLIENT_PROXY_ENABLED",False)
		
		print c.set_nat(user,'NetworkManager', True, True, external_iface)
		print c.set_routing(user,'NetworkManager', True, True)
		
		print c.systemd_resolved_conf(user,"NetworkManager")
		print c.apply_changes(user,"NetworkManager")
		
	except Exception as e:
		print(e)
		raise e
	
	
else:
	e=Exception()
	e.message=ret[1]
	raise e

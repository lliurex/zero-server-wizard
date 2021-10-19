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

	lst=["adminpassword"]
	for item in lst:
		if item not in self.template:
			print("\t[020-samba] [!]" + item + " is missing from template. Aborting initialization")
			return (False,"[020-samba] [!]" + item + " is missing from template. Aborting initialization")
			
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
		
		context=ssl._create_unverified_context()
		c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
		
		print(c.load_schema(user,'SambaManager'))
		print(c.load_index(user,'SambaManager'))
		print(c.configure_smb(user,'SambaManager'))
		print(c.load_acl_samba_education(user,'SambaManager'))
		print(c.load_acl(user,"SlapdManager"))
		result = r.get_ldap_password(remote_user,'SlapdManager')
		if result["status"]!=0:
			raise Exception(result['msg'])
		ldap_password = result['return']
		print(c.update_root_password_samba(user,'SambaManager',ldap_password))
		
	except Exception as e:
		print(e)
		raise e
else:
	e=Exception()
	e.message=ret[1]
	raise e

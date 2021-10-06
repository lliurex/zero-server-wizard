#!/usr/bin/python

import xmlrpclib

def check_environment():

    if ("user" and "password") not in self.template:
        if "masterkey" not in self.template:
            return (False,"No authentication method found")
    else:
        c=xmlrpclib.ServerProxy("https://"+self.template["remote_ip"]+":9779",allow_none=True)
        det=c.validate_user(self.template["user"],self.template["password"])
        if not ret[0]:
            return(False,"User validation error")
    return (True,"")


if check_environment()[0]:
    ip_server = self.template["remote_ip"]
    if "user" in self.template:
        user=(self.template["user"],self.template["password"])
    else:
        user=self.template["masterkey"]
    c=xmlrpclib.ServerProxy("https://"+ip_server+":9779",allow_none=True)
    print(c.clean_nat_services( user, 'NetworkManager' ))
    print(c.clean_mirror_redirect_service( user, 'NetworkManager' ))
    print(c.set_replicate_interface(user,'NetworkManager',None))
    print(c.unset_replication_vars(user,'NetworkManager'))


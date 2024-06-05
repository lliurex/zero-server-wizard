#!/usr/bin/python3

import xmlrpc.client
import ssl
import os

def check_environment():

    if ("user" and "password") not in self.template:
        if "masterkey" not in self.template:
            return (False,"No authentication method found")
    else:
        context=ssl._create_unverified_context()
        c = xmlrpc.client.ServerProxy('https://'+self.template["remote_ip"]+':9779',context=context,allow_none=True)
        ret=c.validate_user(self.template["user"],self.template["password"])
        if ret["status"]!=0:
            return(False,"User validation error")
        if not ret["return"][0]:
            return(False,"User validation error")
    return (True,"")

if check_environment()[0]:
    ip_server = self.template["remote_ip"]
    if "user" in self.template:
        user=(self.template["user"],self.template["password"])
    else:
        user=self.template["masterkey"]
    context=ssl._create_unverified_context()
    c = xmlrpc.client.ServerProxy('https://'+ip_server+':9779',context=context,allow_none=True)
    print(c.clean_nat_services( user, 'NetworkManager' ))
    print(c.clean_mirror_redirect_service( user, 'NetworkManager'))
    print(c.unset_replication_vars( user, 'NetworkManager'))
    llx_network_config="/etc/netplan/20-lliurex.yaml"
    replication_network_config="/etc/netplan/30-replication-lliurex.yaml"
    if os.path.exists(llx_network_config):
        os.remove(llx_network_config)
    if os.path.exists(replication_network_config):
        os.remove(replication_network_config)


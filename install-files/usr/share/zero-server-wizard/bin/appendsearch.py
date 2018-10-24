#!/usr/bin/env python
import lliurex.interfacesparser
import xmlrpclib as x

manager = lliurex.interfacesparser.InterfacesParser()
c = x.ServerProxy('https://localhost:9779')
internalinterface = c.get_variable('','VariablesManager','INTERNAL_INTERFACE')
internaldomain = c.get_variable('','VariablesManager','INTERNAL_DOMAIN')
if internaldomain is not None and internalinterface is not None:
	manager.load('/etc/network/interfaces')
	liststanzaindex = manager.interface_mapping[internalinterface]
	for stanzaindex in liststanzaindex:
		if manager.content[stanzaindex].__class__.__name__ == 'StanzaIface':
			manager.content[stanzaindex].set_option('dns-search ' + internaldomain,True)
	manager.write_file('/etc/network/interfaces')
	f = open('/etc/resolv.conf','a')
	f.write("search " + internaldomain + "\n")
	f.close()

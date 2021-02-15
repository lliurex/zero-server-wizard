import os
import multiprocessing
import time
import subprocess

import n4d.server.core
import n4d.responses

class ZeroServerWizardManager:
	
	def __init__(self):
		
		self.core=n4d.server.core.Core.get_core()
		
	#def init 
	
	
	def end_operations(self):

		self.core.get_plugin("ZCenterVariables").set_configured("zero-server-wizard")
		os.system("systemctl restart network-manager")
		os.system("systemctl restart dnsmasq")
		os.system("systemctl restart systemd-resolved")
		os.system("systemctl restart smbd")
		
		try:
			#Fix firefox default config
			serverProperties="/usr/share/lliurex-firefox-settings/lliurex-firefox.properties"
			defaultProperties="/etc/firefox/lliurex-firefox.properties" 
			if os.path.exists(defaultProperties):
				os.remove(defaultProperties)
			os.symlink(serverProperties,defaultProperties)
		except:
			pass
		
		p=multiprocessing.Process(target=self._t_restart)
		p.start()
		
		return n4d.responses.build_successful_call_response()
		
	#def end_operations
	
	def get_samba_id(self):

		try:
			pprocess = subprocess.Popen(['net','getlocalsid'],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
			sambaid = pprocess.communicate()[0]
			aux = sambaid.split(":")[1]
			id=aux[1:len(aux)-1]
			return n4d.responses.build_successful_call_response(id)
		except:
			return n4d.responses.build_failed_call_response()
	
		
	#def get_samba_id	
	
	def _t_restart(self):
		
		time.sleep(1)
		os.system("kill -9 $(cat /run/n4d/token)")
		return n4d.responses.build_successful_call_response()
	
#class ZeroServerWizardManager

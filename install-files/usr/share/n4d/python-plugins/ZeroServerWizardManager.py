import os
import multiprocessing
import time
import subprocess
import lliurex.net

class ZeroServerWizardManager:
	
	def __init__(self):
		
		pass
		
	#def init 
	
	
	def end_operations(self):

		objects["ZCenterVariables"].set_configured("zero-server-wizard")
		objects["VariablesManager"].write_file()
		os.system("systemctl restart resolvconf")
		os.system("systemctl restart dnsmasq")
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
		
		return True
		
	#def end_operations
	
	def get_samba_id(self):

		try:
			pprocess = subprocess.Popen(['net','getlocalsid'],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
			sambaid = pprocess.communicate()[0]
			aux = sambaid.split(":")[1]
			id=aux[1:len(aux)-1]
			return id
		except:
			return None
	
		
	#def get_samba_id	
	
	def _t_restart(self):
		
		time.sleep(1)
		
		os.system("kill -9 $(cat /tmp/.n4d_pid)")
	
	
#class ZeroServerWizardManager

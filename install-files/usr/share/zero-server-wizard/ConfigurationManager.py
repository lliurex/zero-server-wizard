# -*- coding: utf-8 -*-
import ConfigParser
import os

ZSW_LOG="/var/log/zero-server-wizard/zsw-log"

class ConfigurationManager:
	
	def __init__(self,base_dir):
		
		
		self.servers = {}
		file_list=os.listdir(base_dir)
		file_list.sort()
		
		for f in sorted(file_list):
			if f.find(".")!=0:
				server={}
				config = ConfigParser.ConfigParser()
				config.optionxform=str
				config.read(base_dir + "/" + f)

				try:
					server["id"]=config.get("SETUP","server_id")
					server["class_name"]=config.get("SETUP","class_name")
					server["server_name_en"]=config.get("SETUP","server_name")
					server["server_name_es"]=config.get("SETUP","server_name[es]")
					server["server_name_qcv"]=config.get("SETUP","server_name[qcv]")
					server["info_en"]=config.get("SETUP","info")
					server["info_es"]=config.get("SETUP","info[es]")
					server["info_qcv"]=config.get("SETUP","info[qcv]")
					server["folder"]=config.get("SETUP","folder")
					server["icon"]=config.get("SETUP","icon")
					self.servers[server["id"]]=server
					
				except Exception as e:
					f2=open(ZSW_LOG,"a")
					f2.write("[!] Error reading " + str(base_dir) + str(file) + " " + str(e) + "[!]\n")
					print("[!] Error reading " + str(base_dir) + str(file) + " " + str(e) + "[!]\n")
					f2.close()
			
		
	#def init

	def print_servers(self):
		
		for server in self.servers:
		
			print ""
			print server.id
			print server.server_name["en"]
			print server.server_name["es"]
			print server.server_name["qcv"]
			print server.info["en"]
			print server.info["es"]
			print server.info["qcv"]
			print server.folder
			print server.icon
		
	#def print_servers

	
#class ConfigurationManager

if __name__=="__main__":
	
	cm=ConfigurationManager("/srv/svn/pandora/zero-server-wizard/trunk/install-files/etc/zero-server-wizard/enabled.d/")
	cm.print_servers()



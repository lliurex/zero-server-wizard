# -*- coding: utf-8 -*-
import configparser as ConfigParser
import os
import os.path
import sys

ZSW_LOG="/var/log/zero-server-wizard/zsw-log"

class TemplateManager:
	
	def __init__(self):
		
		pass
		
	#def _init__
	
	def get_info(self,file,server_info):
		
		if os.path.exists(file):
			file_path=file
		else:
			if os.path.exists(os.getcwd()+"/"+file):
				file_path=os.getcwd()+"/"+file
			else:
				file_path=None
				
		
		if file_path!=None:
		
			try:
				config = ConfigParser.ConfigParser()
				config.optionxform=str
				config.read(file_path)
				template={}
				template["id"]=config.sections()[0]
				if template["id"] not in server_info:
					return None
				'''
				for variable in server_info[template["id"]]["variables"]:
					template[variable]=config.get(template["id"],variable)
				'''
				for variable in config.items(template["id"]):
					x,y=variable
					if y=="" or y=="None":
						y=None
						
					template[x]=y
					
					
				return template 
				
			except Exception as e:
				
				print(e)
				return None
			
		
		
	#def get_info
	
	
#class TemplateManager


if __name__=="__main__":
	
	t=TemplateManager(sys.argv[1])
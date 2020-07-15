# -*- coding: utf-8 -*-

import os
import os.path
import sys
import datetime
import signal
import platform

#CUSTOM IMPORTS
import ConfigurationManager
import TemplateManager
try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk, Gdk, GObject
	
	GUI_READY=True
	
except:
	
	GUI_READY=False



import independent
import master
import slave


#VARIABLES
signal.signal(signal.SIGINT, signal.SIG_DFL)

CONF_PATH="/etc/zero-server-wizard/enabled.d/"
ZSW_LOG="/var/log/zero-server-wizard/zsw-log"


class Core:
	
	def __init__(self,mode="cli",template=None):
	
		print("[CORE] Initializing ZSW Core...")
		self.lang=self.get_lang()
		self.servers=self.load_configuration_files(CONF_PATH)
		
		self.platform=platform.machine()
		
		if mode!="cli" and mode!="gui":
				mode="gui"
		self.mode=mode
		
		if template!=None:
			self.template=self.parse_template_file(template)
		else:
			self.template=None

		self.independent=independent.Independent(self)			
		self.master=master.Master(self)
		self.slave=slave.Slave(self)
		
			
		print("[CORE] " + self.mode.upper() + " MODE READY")
		if self.template!=None:
					
			print("[CORE] Loading " + self.template["id"] + " module...")
			try:
				execfile(self.servers[self.template["id"]]["folder"],locals())
			except Exception as e:
				print(e)
				self.log("[CORE] Error loading " + self.template["id"])
				sys.exit(1)
				
			id=self.template["id"]
			s=locals()[self.servers[id]["class_name"]](self,self.servers[id])
			
			f=open("/etc/n4d/key")
			key=f.readline().strip("\n")
			f.close()
			self.template["masterkey"]=key
			
			
			if mode=="cli":
				ret=s.execute(self.template)
				if ret:
					print("[CORE] Initialization complete!!")
				else:
					print("[CORE] [!] Initialization failed [!]")
		
		if self.mode=="cli" and self.template==None:
			print("[CORE][!] Cli mode needs a template file to start initialization.")
			sys.exit(0)
		
		if self.mode=="gui":
			self.template={}
			
			f=open("/etc/n4d/key")
			key=f.readline().strip("\n")
			f.close()
			self.template["masterkey"]=key			
			
			self.start_gui()
			
			
	
	#def __init__
	
	def start_gui(self):
		
		builder = Gtk.Builder()
		builder.set_translation_domain("zero-server-wizard")
		
		self.builder=builder
		
		if os.path.exists("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/main.glade"):
			builder.add_from_file("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/main.glade")
		else:
			builder.add_from_file("/usr/share/zero-server-wizard/rsrc/main.glade")
		
		
		
			
		self.window=builder.get_object("window1")
		self.window.set_name("Window2")
		self.window.connect("destroy",self.close_window)
		self.notebook=builder.get_object("notebook1")
		
		
		#background-image: -gtk-gradient (linear,	left top, left bottom, from (#f86f05),  to (#8f4103));
		#background-image: -gtk-gradient (linear,	left top, left bottom, from (rgba(255,255,255,1)),  to (rgba(210,210,210,1)));
		#background-image: -gtk-gradient (linear,	left top, right top, from (rgba(255,255,255,1)),  to (rgba(210,210,210,0)));

		css = """
		
		#Window2 {
			background-image: -gtk-gradient (linear,	left top, left bottom, from (#f86f05),  to (#d17e08));
		}
		
	
		entry:insensitive
		{
			color: #000000;
			background-color: #cccccc;
		}
		
		textview text
		{
			color: #282828;
		}
		
		notebook{
			
			background-image: -gtk-gradient (linear,	left top, left bottom, from (rgba(255,255,255,1)),  to (rgba(250,250,250,1)));
		}


		"""
		
		self.style_provider=Gtk.CssProvider()
		self.style_provider.load_from_data(css)
		
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.window_box=builder.get_object("box1")


		self.exit_button=builder.get_object("quit_button")
		self.exit_button.set_name("Button")
		self.exit_button.connect("clicked",self.close_window)
		
		self.window.show_all()
		
		if "INDEPENDENT" in self.servers:
			self.independent.start_gui()
		else:
			self.notebook.get_nth_page(0).hide()
			
		if "MASTER" in self.servers:
			self.master.start_gui()
		else:
			self.notebook.get_nth_page(1).hide()
			
			
		if "SLAVE" in self.servers:
			self.slave.start_gui()
		else:
			self.notebook.get_nth_page(2).hide()	
		
		GObject.threads_init()
		Gtk.main()
		GObject.threads_leave()
		
	#def start_gui
	
	def apply_clicked(self,widget):
		
		try:
			self.template=self.parse_template_file(self.file_chooser.get_filename())
		except Exception as e:
			self.msg_label.set_text("Error parsing template")

	#def apply_clicked
	
	
	def populate_buttons(self):
		
		for server in self.servers:
			button=Gtk.Button(server)
			button.show()
			#button.set_name("Button")
			button.connect("clicked",self.button_click,server)
			self.buttons_box.pack_start(button,False,False	,5)
		
	#def populate_buttons

	
	def button_click(self,widget,id):
		
		print("[CORE] Loading " + id+ " module...")
		try:
			execfile(self.servers[id]["folder"]+"/main.py",locals())
		except Exception as e:
			print(e)
			self.log("[CORE] Error loading " + id)
			sys.exit(1)
				
		s=locals()[self.servers[id]["class_name"]](self,self.servers[id])
		s.start_gui(False)
		
	#def button_click
	
	
	def close_window(self,widget):
		
		Gtk.main_quit()
		sys.exit(0)
		
	#def close_window

	
	def log(self,line):
		
		log_file="/tmp/zsw"
		f=open(log_file,"a")
		f.write( "[ "+datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S") + " ] " + line + "\n")
		f.close()
		
	#def log	
	
	
	def get_lang(self):
		
		print("[CORE] Getting system language...")
		lang=os.environ["LANG"].split("_")[0].split(".")[0]
		if lang!="en" and lang!="es" and lang!="qcv":
			return "en"
		else:
			return lang
		
	#def get_lang

	
	def load_configuration_files(self,conf):
		
		print("[CORE] Reading configuration files...")
		c=ConfigurationManager.ConfigurationManager(conf)
		return c.servers
		
	#def load_configuration_files

	
	def parse_template_file(self,template_file):
		
		print("[CORE] Parsing template file...")
		self.tm=TemplateManager.TemplateManager()
		tmp=self.tm.get_info(template_file,self.servers)
		if tmp!=None:
			print("[CORE] Template for server type " + tmp["id"] + " loaded.")
			'''
			for key in tmp:
				if key!="id":
					print("\t"+key+"="+tmp[key])
			'''
		return tmp
		
	#def template_file

	
	
#class Core


def try_root():
	
	try:
		
		f=open("/etc/n4d/key")
		f.close()
		
		return True
		
		
	except:
		
		print("You need root privileges to run Zero-Server-Wizard.")
		
		if GUI_READY:
			
			try:
				label = Gtk.Label("You need root privileges to run Zero-Server-Wizard.")
				dialog = Gtk.Dialog("Warning", None, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
				dialog.vbox.pack_start(label,True,True,10)
				label.show()
				dialog.set_border_width(6)
				response = dialog.run()
				dialog.destroy()				
			except Exception as e:
				print e
		
		return False


def usage():
	print("USAGE:")
	print("\t/usr/share/zero-server-wizard/core.py -m {cli|gui} -t TEMPLATE_FILE")

if __name__=="__main__":
	
	
	if try_root():
	
		mode=None
		template=None
		
		counter=0
		for item in sys.argv:
			if item=="-m" or item=="--mode":
				try:
					mode=sys.argv[counter+1]
				except Exception as e:
					print e
					usage()
					sys.exit(1)
			if item=="-t" or item=="--template":
				try:
					template=sys.argv[counter+1]
				except Exception as e:
					usage()
					sys.exit(1)
		
		
			counter+=1
			
		
		if mode!=None:
			
			core=Core(mode,template)

		else:
			usage()


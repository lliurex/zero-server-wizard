import os
import os.path
import datetime
import subprocess
import sys
import multiprocessing


import lliurex.net
try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk,Gdk,GLib
except:
	pass

import gettext
gettext.textdomain('zero-server-wizard')
_=gettext.gettext


DNS1="172.27.111.5"
DNS2="172.27.111.6"

class Independent:
	
	
	def __init__(self,core,server_conf=None):
		
		self.id="INDEPENDENT"
		self.scripts_path="/usr/share/zero-server-wizard/types/independent/actions/"
		self.template={}
		if server_conf!=None:
			try:
				for item in server_conf["variables"]:
					self.template[item]=None
			except:
				pass
				

		
		self.core=core
		
	#def __init__
	
	def start_gui(self,standalone=False):
		
		self.standalone=standalone
		
		builder=self.core.builder

		
		self.apply_button=builder.get_object("apply_button")
		self.internal_speed_label=builder.get_object("internal_iface_speed_label")
		self.external_speed_label=builder.get_object("external_iface_speed_label")
		self.password_entry=builder.get_object("password_entry")
		self.password_entry1=builder.get_object("password_entry1")
		self.password_entry.connect("changed",self.password_changed)
		self.password_entry1.connect("changed",self.password_changed)
		self.srv_name_entry=builder.get_object("srv_name_entry")
		self.srv_domain_entry=builder.get_object("srv_domain_entry")
		self.internal_combobox=builder.get_object("internal_combobox")
		self.internal_combobox.set_name("Button")
		self.external_combobox=builder.get_object("external_combobox")
		
		self.internal_ip_entry=builder.get_object("srvip_entry")
		self.internal_mask_entry=builder.get_object("internal_mask_entry")
		self.external_ip_entry=builder.get_object("external_ip_entry")
		self.external_mask_entry=builder.get_object("external_mask_entry")
		self.external_gateway_entry=builder.get_object("external_gateway_entry")
		self.dns1_entry=builder.get_object("dns1_entry")
		self.dns2_entry=builder.get_object("dns2_entry")
		self.pass_label=builder.get_object("pass_label")
		self.dhcp_radiobutton=builder.get_object("dhcp_radiobutton")
		self.dhcp_radiobutton.connect("toggled",self.radio_button_changed)
		self.manual_radiobutton=builder.get_object("manual_radiobutton")
		self.manual_expander=builder.get_object("manual_expander")
		self.manual_expander.set_sensitive(False)
		self.apply_button.connect("clicked",self.apply_clicked)
		self.apply_button.set_sensitive(False)
		self.apply_button.set_name("Button")
		
		
		self.set_default_gui_values()
		

		if standalone:
			
			Gtk.main()

		
	#def start_gui
	
	def radio_button_changed(self,widget):

		self.manual_expander.set_sensitive(not self.dhcp_radiobutton.get_active())
		self.manual_expander.set_expanded(not self.dhcp_radiobutton.get_active())
		
	#def radio_button_changed
	
	def password_changed(self,widget):
		
		if self.password_entry.get_text()!=self.password_entry1.get_text():
			self.pass_label.set_markup("<span fgcolor='red'>" + _("Passwords do not match") +"</span>")
			self.apply_button.set_sensitive(False)
		else:
			self.pass_label.set_markup("")
			self.apply_button.set_sensitive(True)
			

		
	#def
	
	def set_default_gui_values(self):
		
		self.iiface_model=Gtk.ListStore(str)
		self.eiface_model=Gtk.ListStore(str)
		
		self.internal_combobox.set_model(self.iiface_model)
		self.external_combobox.set_model(self.eiface_model)
		rendi=Gtk.CellRendererText()
		self.internal_combobox.pack_start(rendi,True)
		self.internal_combobox.add_attribute(rendi,"text",0)
		self.internal_combobox.connect("changed",self.get_link_speed,0)
		rende=Gtk.CellRendererText()
		self.external_combobox.pack_start(rende,True)
		self.external_combobox.add_attribute(rende,"text",0)
		self.external_combobox.connect("changed",self.get_link_speed,1)
		self.interfaces=lliurex.net.get_devices_info()		
		
		
		for item in self.interfaces:
			if "eth" in item["name"]:
				self.iiface_model.append([item["name"]])
				self.eiface_model.append([item["name"]])
				
			
		self.internal_combobox.set_active(0)
		if len(self.iiface_model)>1:
			self.external_combobox.set_active(1)
		else:
			self.external_combobox.set_active(0)
			
		
		self.srv_domain_entry.set_text(self.template.setdefault("srv_domain_name","aula1"))
		self.internal_ip_entry.set_text(self.template.setdefault("srv_ip","10.2.1.254"))
		self.internal_mask_entry.set_text(self.template.setdefault("internal_mask","255.255.255.0"))
		self.dns1_entry.set_text(DNS1)
		self.dns2_entry.set_text(DNS2)
		
		try:
			
			f=open("/etc/hostname")
			line=f.readline().strip("\n")
			f.close()
			self.srv_name_entry.set_text(self.template.setdefault("srv_name",line))
		except:
			pass
			
		
		
	#def set_default_gui_values
	
	def apply_clicked(self,widget):
		

		self.get_gui_values()
		
		
	#def apply_clicked
	
	def get_gui_values(self):
		
		iter=self.internal_combobox.get_active_iter()
		if iter!=None:
			self.template["internal_iface"]=self.iiface_model.get(iter,0)[0]
		else:
			self.template["internal_iface"]=None
		iter=self.external_combobox.get_active_iter()
		if iter!=None:
			self.template["external_iface"]=self.eiface_model.get(iter,0)[0]
		else:
			self.template["external_iface"]=None
		
		self.template["adminpassword"]=self.password_entry.get_text()
		self.template["srv_name"]=self.srv_name_entry.get_text()
		self.template["srv_name"]=''.join(e for e in self.template["srv_name"] if e.isalnum())
		self.template["srv_domain_name"]=self.srv_domain_entry.get_text()
		self.template["srv_domain_name"]=''.join(e for e in self.template["srv_domain_name"] if e.isalnum())
		self.template["srv_ip"]=self.internal_ip_entry.get_text()
		self.template["internal_mask"]=self.internal_mask_entry.get_text()
		if self.dhcp_radiobutton.get_active():
			self.template["external_mode"]="dhcp"

		else:
			self.template["external_mode"]="manual"

		self.template["external_ip"]=self.external_ip_entry.get_text()
		self.template["external_mask"]=self.external_mask_entry.get_text()
		self.template["external_gateway"]=self.external_gateway_entry.get_text()
		self.template["dns1"]=self.dns1_entry.get_text()
		self.template["dns2"]=self.dns2_entry.get_text()
		
		self.check_values()
	
	
	def check_values(self):
		

			error_msg=""
			'''
			if self.template["internal_iface"]==self.template["external_iface"]:
				error_msg+="* External and internal interfaces must be different.\n"
			'''
			if not lliurex.net.is_valid_ip(self.template["srv_ip"]):
				error_msg+="* " + _("Internal IP must be a valid IP.")+"\n"

			if not lliurex.net.is_valid_ip(self.template["internal_mask"]):
				error_msg+="* " + _("Internal mask must be a valid IP.") + "\n"
				
			if self.template["srv_name"]=="":
				error_msg+="* " + _("Server name cannot be an empty string.") + "\n"
			if self.template["srv_domain_name"]=="":
				error_msg+="* " + _("Server domain name cannot be an empty string.") +"\n"
			
			
			if self.template["external_mode"]=="manual":

				if self.template["external_ip"]=='' or not lliurex.net.is_valid_ip(self.template["external_ip"]):
					error_msg+="* " + _("External IP must be a valid IP.")+"\n"
				if self.template["external_mask"]=="" or not lliurex.net.is_valid_ip(self.template["external_mask"]):
					error_msg+="* " + _("External mask must be a valid IP.")+"\n"
				if self.template["external_gateway"]=="" or not lliurex.net.is_valid_ip(self.template["external_gateway"]):
					error_msg+="* " + _("External gateway must be a valid IP.")+"\n"
				
				
			if self.template["dns1"]=="" or not lliurex.net.is_valid_ip(self.template["dns1"]):
				error_msg+="* " + _("DNS1 must be a valid IP.")+"\n"
			if self.template["dns2"]=="" or not lliurex.net.is_valid_ip(self.template["dns2"]):
				error_msg+="* " + _("DNS2 must be a valid IP.")+"\n"
				
			if error_msg!="":
				builder = Gtk.Builder()
				if os.path.exists("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/warning.glade"):
					builder.add_from_file("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/warning.glade")
				else:
					builder.add_from_file("/usr/share/zero-server-wizard/rsrc/warning.glade")
					
					
				window=builder.get_object("window1")
				msg_label=builder.get_object("msg_label")
				close_button=builder.get_object("close_button")
				def hide(widget):
					window.destroy()
				close_button.connect("clicked",hide)
				msg_label.set_text(error_msg.strip("\n"))
				window.show()				
			
			else:
				
				builder=Gtk.Builder()
				if os.path.exists("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/progress_window.glade"):
					builder.add_from_file("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/progress_window.glade")
				else:
					builder.add_from_file("/usr/share/zero-server-wizard/rsrc/progress_window.glade")				
					
					
				self.error_msg=None
				window=builder.get_object("window1")
				review_textview=builder.get_object("textbuffer1")
				exec_textview=builder.get_object("textbuffer2")
				apply_button=builder.get_object("apply_button")
				close_button=builder.get_object("close_button")
				pbar=builder.get_object("progressbar1")
				terminal_box=builder.get_object("scrolledwindow2")
				understand_cb=builder.get_object("understand_checkbutton")
				
								
				#ret_textview=builder.get_object("ret_textview")
				widgets=[close_button,pbar]
				self.pulsating=False
				
				
				msg=""
				
				msg+="[ "+"SERVER NAME"+" ] = " + self.template["srv_name"] + "\n"
				msg+="[ "+"SERVER DOMAIN NAME"+" ] = " + self.template["srv_domain_name"] + "\n"
				msg+="[ "+"INTERNAL INTERFACE"+" ] = " + self.template["internal_iface"] + "\n"
				msg+="[ "+"INTERNAL IP"+" ] = " + self.template["srv_ip"] + "\n"
				msg+="[ "+"INTERNAL MASK"+" ] = " + self.template["internal_mask"] + "\n"
				msg+="[ "+"EXTERNAL INTERFACE"+" ] = " + self.template["external_iface"] + "\n"
				msg+="[ "+"EXTERNAL MODE"+" ] = " + self.template["external_mode"] + "\n"
				if self.template["external_mode"]!="dhcp":
					msg+="[ "+"EXTERNAL IP"+" ] = " + self.template["external_ip"] + "\n"
					msg+="[ "+"EXTERNAL MASK"+" ] = " + self.template["external_mask"] + "\n"
					msg+="[ "+"EXTERNAL GATEWAY"+" ] = " + self.template["external_gateway"] + "\n"
				msg+="[ "+"DNS"+" ] = " + str(self.template["dns1"]) + ", " + str(self.template["dns2"])+ "\n"
					

				
				review_textview.set_text(msg)
					
				
				
				def pulsating():
					pbar.pulse()
					
					try:
						f=open("/tmp/.zsw-log","r")
						tmp="".join(f.readlines())
						if self.msg_thread!=tmp:
							self.msg_thread=tmp
							exec_textview.set_text(tmp)
							
						f.close()
					except:
						pass
						
					
					
					if not os.path.exists("/tmp/.zsw-on"):
						pbar.set_fraction(1)
						close_button.set_sensitive(True)
						
						
						
						if os.path.exists("/tmp/.zsw-error"):
						
							f=open("/tmp/.zsw-error","r")
							self.error_msg=f.readline()
							f.close()
							os.remove("/tmp/.zsw-error")
						
							builder = Gtk.Builder()
							if os.path.exists("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/warning.glade"):
								builder.add_from_file("/srv/svn/pandora/zero-server-wizard/trunk/install-files/usr/share/zero-server-wizard/rsrc/warning.glade")
							else:
								builder.add_from_file("/usr/share/zero-server-wizard/rsrc/warning.glade")
								
								
							window2=builder.get_object("window1")
							msg_label=builder.get_object("msg_label")
							close_button2=builder.get_object("close_button")
							def hide(widget):
								window2.destroy()
							close_button2.connect("clicked",hide)
							msg_label.set_markup("<b>"+self.error_msg+"</b>")
							window2.set_title("Error")
							window2.show()	
							
							return False
							
						else:
							label = Gtk.Label(_("Initialization complete. A reboot is required."))
							dialog = Gtk.Dialog("Zero Server Wizard", None, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
							img=Gtk.Image.new_from_stock(Gtk.STOCK_APPLY,Gtk.IconSize.DIALOG)
							hbox=Gtk.HBox()
							hbox.pack_start(img,True,True,5)
							hbox.pack_start(label,True,True,5)
							hbox.show_all()
							dialog.vbox.pack_start(hbox,True,True,10)
							label.show()
							dialog.set_border_width(6)
							response = dialog.run()

							sys.exit(0)
						
						
						
					return True
				
				def apply_clicked(widget,cb):
					self.pulsating=True
					f=open("/tmp/.zsw-on","w")
					f.close()
					self.msg_thread=""
					self.prv_msg=None
					widget.set_sensitive(False)
					cb.set_sensitive(False)
					t=multiprocessing.Process(target=self.execute,args=(self.template,True,))
					#t.daemon=True
					t.start()
					close_button.set_sensitive(False)
					GLib.timeout_add(100,pulsating)
					
				def destroy(uno,dos):
					try:
						if self.pulsating:
							return True
						else:
							window.destroy()
					except:
						pass
						

					
				#def apply_clicked
				
				
				def close(widget):
					window.destroy()

				
				def understand_changed(widget,button):
					
					button.set_sensitive(widget.get_active())
					
				#def understand_changed


				understand_cb.connect("toggled",understand_changed,apply_button)
				apply_button.connect("clicked",apply_clicked,understand_cb)
				close_button.connect("clicked",close)
				window.connect("delete_event",destroy)
				
				window.show()
				
				pass
				#def init_done
				

	#def check_values
	
	def get_link_speed(self,widget,id):
		
		tree_iter = widget.get_active_iter()
		if tree_iter != None:
			model = widget.get_model()
			try:
				speed=lliurex.net.get_device_info(model[tree_iter][0])["Speed"][0]
			except:
				speed="Unknown speed"
			if id==0:
				self.internal_speed_label.set_text(speed)
			else:
				self.external_speed_label.set_text(speed)
				
		
	#def get_link_speed
	
	def external_mode_signal(self,widget):
		
		self.manual_external_box.set_sensitive(not self.dhcp_radiobutton.get_active())
		
	#def ems
	
	
	def close_window(self,widget):
		if self.standalone:
			Gtk.main_quit()
		
		
	#def close_window
	
	
	def execute(self,template,gui=False):
		
		print("[INDEPENDENT] Executing independent configuration...")
			
		#self.template=template
		self.log("Executing Independent configuration...")

		self.core.template=dict(self.core.template.items() + self.template.items())
		self.template=self.core.template
		
		if not self.template.has_key("remote_ip"):
			self.template["remote_ip"]="localhost"
		
		
		if os.path.exists("/tmp/.zsw-log"):
			os.remove("/tmp/.zsw-log")
		
		for f in sorted(os.listdir("/usr/share/zero-server-wizard/types/independent/actions/")):
			if os.path.isfile(self.scripts_path+f):
				
				try:
					if f.endswith(".py"):
						self.log("Excuting " + f + " ...")
						print("[INDEPENDENT] Executing " + f + " ...")
						if not gui:
							exec(open(self.scripts_path+f).read(),locals())
						else:
							
							#.set_text(ret_textview.get_buffer().get_text(ret_textview.get_buffer().get_start_iter(),ret_textview.get_buffer().get_end_iter(),True)+ "\npor aqui")
							#msg+=("[INDEPENDENT] Executing " + f + " ... ")
							f_=open("/tmp/.zsw-log","a")
							f_.write("[INDEPENDENT] Executing " + f + " ... ")
							f_.close()
							exec(open(self.scripts_path+f).read(),locals())
							f_=open("/tmp/.zsw-log","a")
							f_.write(" OK\n")
							f_.close()
							


							
				except Exception as e:
					print("[ERROR!] " + str(e))

					try:
						f=open("/tmp/.zsw-error","w")
						f.write(e.message)
						f.close()
					except:
						pass
					
					if os.path.exists("/tmp/.zsw-on"):
						os.remove("/tmp/.zsw-on")
					return False
		
		if gui:
			if os.path.exists("/tmp/.zsw-on"):
				os.remove("/tmp/.zsw-on")
		
		return True	
		
	#def execute
	
	def log(self,line):
		
		independent_log="/tmp/independent"
		f=open(independent_log,"a")
		f.write( "[ "+datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S") + " ] " + line + "\n")
		f.close()
		
		
	#def log
	
	
	
	
#class Independent

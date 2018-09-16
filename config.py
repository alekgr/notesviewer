#! /usr/bin/env python

import os
import vardata 
from repo import *
import ConfigParser


def loadconfig():
	""" load config file into the OPTIONS dictionary """
	
	global OPTIONS

	#return False if there is no config file
	if not verifyconfigfile(): 
		return False	
	else:	
		#read config file
		config = ConfigParser.ConfigParser()
		config.read(vardata.config_file_path)

		#return False if no setttings section
		if not config.has_section('settings'):
			return False
		else:
			#load each setting option if available else it will go with default
			if config.has_option('settings', 'graphical'):
				vardata.OPTIONS['graphical']	=	config.get('settings','graphical')
			if config.has_option('settings', 'verbose'):
				vardata.OPTIONS['verbose']   	=	config.get('settings','verbose')
			if config.has_option('settings', 'editor'):
				vardata.OPTIONS['editor']		=	config.get('settings','editor')
			if config.has_option('settings', 'color_err'):
				vardata.OPTIONS['color_err'] 	=	config.get('settings','color_err')
			if config.has_option('settings', 'color_cata'):
				vardata.OPTIONS['color_cata']	=	config.get('settings','color_cata')
			if config.has_option('settings', 'color_note'):
				vardata.OPTIONS['color_note']	=	config.get('settings','color_note')
			if config.has_option('settings', 'data_location'):
				vardata.OPTIONS['data_location'] =  config.get('settings','data_location')

	#return as True
	return  True


def setdefaultconfig():
	""" set the default configuration.. overwriting old configuration"""	


	#add setting and options
	config = ConfigParser.ConfigParser()
	config.add_section("settings")
	config.set("settings", "graphical", vardata.GRAPHICAL_DEFAULT)
	config.set("settings", "verbose", vardata.VERBOSE_DEFAULT)
	config.set("settings", "editor", vardata.EDITOR_DEFAULT)
	config.set("settings", "color_err", vardata.COLOR_ERR_DEFAULT)
	config.set("settings", "color_cata", vardata.COLOR_CATA_DEFAULT)
	config.set("settings", "color_note", vardata.COLOR_NOTE_DEFAULT) 
	config.set("settings", "data_location", vardata.DATA_DEFAULT)

	#write to config_file
	with open(vardata.config_file_path,"wb") as fp:
		config.write(fp)


def verifyconfigfile():
	"""verify if config file is found """
	if os.path.isfile(vardata.config_file_path) == True:
		return True
	else:
		return False

def verify_key(key):
	" verify if the key is a valid option """

	for k in OPTIONS.keys():
		if key == k:
			return True	
	return False

def verify_key_value(key, val):
	"""verify if a value is a valid option for a key"""

	if key == "graphical" or key == "verbose":
		if val == "true" or val == "false":
			return True
		else:
			return False
	if key == "editor":
		if val in EDITORS:
			return True
		else:
			return False
	if key == "color_err" or key == "color_cata" or key == "color_note":
		if val in COLORS:
			return True
		else:
			return False

	return False

def checksection(conf,section):
	""" check to see if config has a section"""
	conf.read(config_file_path)
	if conf.has_section(section):
		return True
	else:
		return False	

def showconfig():
	""" Main funcation for showconfig() """

	if verifyconfigfile() == False:
		print("There is no "+config_file_path)
		return False

	config = ConfigParser.ConfigParser()
	config.read(vardata.config_file_path)

	#get items from config
	items = dict(config.items("settings"))
	for key,value in zip( items.keys(),items.values()): 
		print(key+":"+value)	

def printconfigoptoin(conf, option):
	""" print an option"""	
	print(conf.get('settings',option))

def set_data_location():
	
	global base_catagory_path

	if get_data_location_type() == "file":
		vardata.base_catagory_path = get_data_location_source()		

	if get_data_location_type() == "git":
		vardata.base_catagory_path = vardata.repo_dir
		if not os.path.isdir(vardata.base_catagory_path):
			os.mkdir(vardata.base_catagory_path)
		if not os.path.exists(vardata.base_catagory_path+"/"+".git"):
			note_clone(get_data_location_source(), vardata.base_catagory_path)

def get_data_location_source():
	return vardata.OPTIONS['data_location'].split(":",1)[1]

def get_data_location_type():
	return vardata.OPTIONS['data_location'].split(":")[0]

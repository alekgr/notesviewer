#!/usr/bin/env python

import os
import pprint
import re
import sys
import vardata 
from config import *


def getcatagoriespath():
	"""return a list of note catagroies as directory paths"""
	dirlist=[];

	for files in os.walk(vardata.base_catagory_path):
		if not re.search(".git", files[0]):
			dirlist.append(files[0])

	return(dirlist)

def getcatagories():

	"""return a list of catagories from directory path"""

	stripedlist=[]
	
	print(vardata.base_catagory_path)	
	dirpathstr = getcatagoriespath()
	length=len(vardata.base_catagory_path)

	for strindex in dirpathstr:
			stripforwardslash = strindex[length:]		
   		 	stripedpath = stripcatagorypath(stripforwardslash)
			if(strindex != vardata.base_catagory_path):
				stripedlist.append(stripedpath)

	return stripedlist

def stripcatagorypath(catagorystring):
	""" return the last base of catagorysstr"""	
	
	catagorylist = catagorystring.split('/')	
	catagorylistlength=len(catagorylist)	
	return(catagorylist[catagorylistlength-1])


def getnotes(catagory):
	filelist=[]

	for dirname,subdir, files in os.walk(vardata.base_catagory_path):
			filelist.append(files)

	return filelist

def getnotecatagory(note):

	catagory_list=[]

	for root,directories,files in os.walk(vardata.base_catagory_path):
		if note in files:
			catagory_list.append(root) 
		
	return(catagory_list)

def print_list_per_line(mylist):
	for f in mylist:
		print(f)

def cm_version():

	""" print version """
	print("Version is "+str(vardata.VERSION))

def cm_add(name, scope, verbose):
	"""add a catagory or note"""

	#add a note
	if scope == "note":
		path = vardata.base_catagory_path+"/"+name
		if not os.path.exists(os.path.dirname(path)):
			print("path does not exist")
			return False
		if os.path.exists(path) == False:
			os.mknod(path)
			return True
		else:
			print("note already exists")
			return False

def cm_list(scope, verbose):

	if scope == 'catagory':
		print_list_per_line(getcatagories())
	if scope == 'note':
		for dirs, subdirs, files in os.walk(vardata.base_catagory_path):
			if os.path.basename(dirs) != '.git':
				print(os.path.basename(dirs))
			else:
				break
			for fileindex in files:
				print("\t"+"--->"+os.path.basename(fileindex))

def cm_showconfig():
	
	showconfig()

def cm_setdefaultconfig():

	setdefaultconfig() 

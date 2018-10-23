#!/usr/bin/env python
from __future__ import print_function
import os
import pprint
import re
import sys
import shutil
import vardata 
import note
import utils
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

def cm_add(name, verbose):
	"""add a note"""

	meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name
	content_path=vardata.base_catagory_path+"/"+"content"+"/"+name

	os.mknod(meta_path)
	os.mknod(content_path)

def cm_insert(name, title):

	note_path = utils.getpath(name)	

	if not os.path.exists(note_path):	
		print(name+" does not exist")
		return False

	if os.path.isdir(note_path):
		print(name+" "+"seems to be a catagory")
		return False

	if not note.verifynoteheader(name):
		print(name+" does not seem to be a noteviewer note")
		return False

	print("Enter your notes (CTRL/D) to exit:  ")
	lines = sys.stdin.readlines()


	#full_text = "\n******"+"\n"+"#"+title+"\n"+text+"\n"+"******"+"\n"

	fp = open(note_path,"a")	
	fp.write("\n")
	fp.write("\n"+"******"+"\n")
	fp.write("#"+title+"\n")
	
	for line in lines:
		fp.write(line)
	fp.write("******"+"\n")

	#fp.write(full_text)

	fp.close()

def cm_delete(name, scope, verbose):
	
	#delete  a note or catagory

	path = vardata.base_catagory_path+"/"+name

	if not os.path.exists(path):
		print(name+" does not exist")
		return False
		
	elif os.path.exists(path) == True:
		if scope == "note":
			if not os.path.isfile(path):
				print(name+" "+"does not seem to be a note")
				return False
				
			prompt = raw_input("Are you sure you want to delete "+name+" (yes/no) ")	
			if prompt == "yes":
				os.remove(path)
				return True
			else:
				return False 
		if scope == "catagory":
			if not os.path.isdir(path):
				print(name+" "+"does not seem to be a catagory")
				return False
			if not directoryempty(path):
				prompt = raw_input("Are you sure you want to delete "+name+" catagory and any notes and directories (yes/no) ")
				if prompt == 'yes':
					shutil.rmtree(path)
			else:
				prompt = raw_input("Are you sure you want to delete "+name+" (yes/no) ")
				os.rmdir(path)
				
def cm_list(verbose):
	""" print nameo of the notes"""
	
	print_list_per_line(os.listdir(vardata.base_catagory_path+"/"+"meta"))
	if(verbose == True):
		print("---------")
		print("Total notes: ",end="")
		print(len(os.listdir(vardata.base_catagory_path+"/"+"meta")))

def cm_showconfig():
	
	showconfig()

def cm_setdefaultconfig():

	setdefaultconfig() 

def directoryempty(path):
	if len(os.listdir(path))>0:
		return False
	else:
		return True


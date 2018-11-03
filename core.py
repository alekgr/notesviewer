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
import uuid
import tempfile
import subprocess
from config import *


def edit_file(content):
	"""open a file and return result"""

	#Get the user's editor
	editor = vardata.OPTIONS['editor']
	
	#Open the content with a temp file and send the reult back
	with tempfile.NamedTemporaryFile("a+") as tmpfile:
		tmpfile.write(content)
		tmpfile.flush()
		subprocess.check_call([editor, tmpfile.name])
		output = tmpfile.read()

	return(output)

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
	"""Insert a note with a title"""

	#paths
	meta_path = vardata.base_catagory_path+"/"+"meta"+"/"+name
	content_path = vardata.base_catagory_path+"/"+"content"+"/"+name

	#check if the  note is present
	if not os.path.exists(meta_path):
		print("The note "+name+" does not exist -- bye") 
		return

	#create uuid for the note
	note_uuid = uuid.uuid4()

	#edit the file
	content = edit_file('')
	content = content[:-1]

	#convert the content into a string	
	str_content =""
	str_content  = str_content.join(content)
	str_content = repr(str_content)	
	str_content = str_content.replace("'","")		
	
	#open meta and content files
	fp_meta = open(meta_path, "a")
	fp_content = open(content_path, "a")

	#write to meta
	meta_buffer_string = "uuid:"+str(note_uuid)+" "+"title:"+title
	fp_meta.write(meta_buffer_string+"\n")

	#write to content
	content_buffer_string = "uuid:"+str(note_uuid)+" "+"content:"+str_content
	fp_content.write(content_buffer_string+"\n")

	#close files
	fp_meta.close()
	fp_content.close()

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



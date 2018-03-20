#! /usr/bin/env python


from __future__ import print_function
import os
import re
import utils 

def verifynoteheader(note):
	
	#get note path
	note_path = utils.getpath(note)
	
	#open the file
	fp = open(note_path,"r")

	#read the first line
	line = fp.readline()

	#close fp
	fp.close()

	#strip white charcaters from the end of line
	line = line.rstrip()

	if line=="******"+os.path.basename(note)+" notes"+"******":
		return True	
	else:
		return False

def createnoteheader(note):

	#get note path
	note_path = utils.getpath(note)
	print(note_path)
	#open the file for writting
	fp = open(note_path,"w")

	fp.write("******"+os.path.basename(note)+" notes"+"******")	
	fp.close()



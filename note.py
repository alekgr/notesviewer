#! /usr/bin/env python


from __future__ import print_function
import re
import utils 

def verifynoteheader(note):
	
	#get note path
	note_path = utils.getpath(note)
	
	#open the file
	fp = open(note_path,"r")

	#read the first line
	line = fp.readline()

	#strip white charcaters from the end of line
	line = line.rstrip()

	if line=="******"+note+" notes"+"******":
		print("match")
	else:
		print("no match")

	fp.close()


def createnoteheader(note):

	#get note path
	note_path = utils.getpath(note)
	print(note_path)
	#open the file for writting
	fp = open(note_path,"w")

	fp.write("******"+note+" notes"+"******")	
	fp.close()



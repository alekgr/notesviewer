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
import codecs
from config import *

def get_uuid(str):
	return(str.split(" ",1)[0])

def get_title(str):
	return(str.split(" ",1)[1])

def get_content(str):
	return(str.split(" ",1)[1])

def remove_newline(str):
	return(str.replace("\n",""))

def remove_first_and_last_chars(s):
    """remove first and last chars"""

    s = s[1:]
    s = s[:-1]
    return(s)

def get_content_by_uuid(content_lines, uuid):
		
	for line in content_lines:
		u = get_uuid(line)	
		u = u.split(":")[1]
		if u == uuid:
			c = get_content(line)
			c = c.split(":")[1]
			return(c)
	return(0)	

def edit_file(content):
	"""open a file and return result"""

	#Get the user's editor
	editor = vardata.OPTIONS['editor']
	
	#Open the content with a temp file and send the reult back
	with tempfile.NamedTemporaryFile("a+") as tmpfile:
		tmpfile.write(content)
		tmpfile.flush()
		subprocess.check_call([editor, tmpfile.name])
                tmpfile.seek(0)
		output = tmpfile.read()
	return(output)

def validate_content_index(index, name):

	meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name

	meta_fp = open(meta_path)
	lines = meta_fp.readlines()

	i = 0
	for line in lines:
		i = i+1 

	meta_fp.close()

	if index >= 1 and index <= i: 
		return True	
	else:
		return False

def getuuidbyindex(lines, index):
	"""get uuid for a index into list"""
	
	ctr=1
	for line in lines:
		if ctr == index: 
                    line = get_uuid(line)
                    line = line.split(":")[1]
                    return line
                ctr = ctr+1


def removeuuidfromlist(lines, uuid):
    """remove uuid line from list"""

    for i, line in enumerate(lines): 
        line = get_uuid(line)    
        line = line.split(":")[1]
        if line == uuid:
            note = lines.pop(i)
            return(note)

    return(False)	

def print_content(content_line):

    #print("Content-> ",end="")
    l = content_line.split("\\n") 
    for i in l: 
        print(i)

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

def cm_edit(entry, note):
        """edit  a note entry"""
        
        meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+note
	content_path=vardata.base_catagory_path+"/"+"content"+"/"+note

        if not os.path.exists(meta_path):
            print("TRhe note "+note+" does not exist -- bye")
            return(False)

        if not os.path.exists(content_path):
            print("The note  "+note+" content does not exist -- bye")
            return(False)

	if validate_content_index(entry, note) == False:
            print("entry number is incorrect")	
            return(False)
        else:
            fp_content = open(content_path)
            content_lines = fp_content.readlines()
            
            content_uuid = getuuidbyindex(content_lines, entry)
            content_string = get_content_by_uuid(content_lines, content_uuid)
            content_string = content_string.replace("\\n","\n")
            content_string = edit_file(content_string)
           
            #remove newline and apostrophe
            c = content_string
            c = content_string.strip()
            c = repr(c)
            c = remove_first_and_last_chars(c)
           
            #close fp
            fp_content.close()
           
            #fill content_lines to one that we edited
            content_lines [entry-1] = "uuid"+":"+content_uuid+" "+"content"+":"+c+"\n"
            
            #convert content_lines list to string
            str_content_lines = ""
            str_content_lines = str_content_lines.join(content_lines)

            #write back to content file
            fp_content = open(content_path, "w+")
            fp_content.write(str_content_lines)
            fp_content.close()


def cm_delete(name):
	"""delete a note""" 	

	#paths
	meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name
	content_path=vardata.base_catagory_path+"/"+"content"+"/"+name

	#if meta_path does not exist
	if not os.path.exists(meta_path):
		print(name+" Note does not exist")
		if os.path.exists(content_path):
			os.remove(content_path)
		return False

	#if meta_path exists
	else:
		prompt = raw_input("Are you sure you want to delete "+name+" (yes/no) ")	#prompt
		prompt = prompt.lower()
		if prompt == "yes":
			os.remove(meta_path) #remove meta_path
			if os.path.exists(content_path): #remove if there is a content_path
				os.remove(content_path)
			print("Deleted the "+name+" note")
			return True
		else:
			print("Did not delete "+name+ " note")
			return False	

def cm_remove(entry, name):
	"""remove entry function"""

	meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name
	content_path=vardata.base_catagory_path+"/"+"content"+"/"+name

	if validate_content_index(entry, name) == False:
            print("entry number is incorrect")	
            return False
        else:
            #open files(content and meta) for reading 
            fp_meta = open(meta_path,"r")
            fp_content = open(content_path, "r")
            meta_lines = fp_meta.readlines()
            content_lines = fp_content.readlines()
            uuid_meta = getuuidbyindex(meta_lines, entry)
            uuid_content = getuuidbyindex(content_lines, entry)
            removeuuidfromlist(meta_lines, uuid_meta)
            removeuuidfromlist(content_lines, uuid_content)
            string_meta = ''.join(meta_lines)
            string_content = ''.join(content_lines)
            fp_meta.close() 
            fp_content.close()
           
            #open files(content and meta) for writting
            fp_meta = open(meta_path,"w")   
            fp_content= open(content_path,"w")
            fp_meta.write(string_meta) 
            fp_content.write(string_content)
            fp_meta.close()

            return string_content

def cm_move(entry, fromnote, tonote):
        """move an  entry from fromnote to tonote"""

        #from note path
        from_meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+fromnote
	from_content_path=vardata.base_catagory_path+"/"+"content"+"/"+fromnote

        #to note path
        to_meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+tonote
	to_content_path=vardata.base_catagory_path+"/"+"content"+"/"+tonote
        
        #check if from path exists
        if not os.path.exists(from_meta_path):
		print(from_note_path+" from Note does not exist")
		return False

        #check if to  path exists
        if not os.path.exists(to_meta_path):
		print(to_note_path+" To Note does not exist bye .. ")
		return False

        #check if from content exists
        if not os.path.exists(from_content_path):
                print(from_content_path+" From Note content does not exist")
                return False

        #check if to content exists
        if not os.path.exists(to_content_path):
                print(to_content_path+" To Note content does not exist")
                return False

        
        #validate note entry from fromnote
	if validate_content_index(entry, fromnote) == False:
            print("entry number is incorrect")	
            return False
                
        
        #open files(content and meta) for reading 
        fp_meta_from = open(from_meta_path,"r")
        fp_content_from = open(from_content_path, "r")
        meta_lines = fp_meta_from.readlines()
        content_lines = fp_content_from.readlines()
        uuid_meta = getuuidbyindex(meta_lines, entry)
        uuid_content = getuuidbyindex(content_lines, entry)
        remove_note_meta = removeuuidfromlist(meta_lines, uuid_meta)
        remove_note_content = removeuuidfromlist(content_lines, uuid_content)
        string_meta = ''.join(meta_lines)
        string_content = ''.join(content_lines)
        fp_meta_from.close() 
        fp_content_from.close()
           
        #open files(content and meta) for writting
        fp_meta_from = open(from_meta_path,"w")   
        fp_content_from= open(from_content_path,"w")
        fp_meta_from.write(string_meta) 
        fp_content_from.write(string_content)
        fp_meta_from.close()
        fp_content_from.close() 


        #Insert a note with a title for the move"""

	#open meta and content files
	fp_meta = open(to_meta_path, "a")
	fp_content = open(to_content_path, "a")

	#write to meta
        fp_meta.write(remove_note_meta)

	#write to content
        fp_content.write(remove_note_content)

	#close files
	fp_meta.close()
	fp_content.close() 


def cm_list(verbose):
	""" print nameo of the notes"""
	
	print_list_per_line(os.listdir(vardata.base_catagory_path+"/"+"meta"))
	if(verbose == True):
		print("---------")
		print("Total notes: ",end="")
		print(len(os.listdir(vardata.base_catagory_path+"/"+"meta")))

def cm_display(note, short):
	"""display a note"""

	#Notes empty object
	class Notes:
		pass

	#note list
	notes = []
	index = 0 

	#paths
	meta_path = vardata.base_catagory_path+"/"+"meta"+"/"+note
	content_path = vardata.base_catagory_path+"/"+"content"+"/"+note

	#check if the  note is present
	if not os.path.exists(meta_path):
		print("The note "+note+" does not exist -- bye") 
		return

	#open meta and content files
	fp_meta = open(meta_path, "r")
	fp_content = open(content_path, "r")

	#read files
	meta_lines = fp_meta.readlines()
	content_lines = fp_content.readlines()

	#loop over list and print 
	for line in meta_lines:
		uuid = get_uuid(line)
		uuid = uuid.split(":")[1]
		title  = get_title(line)
		title  = remove_newline(title)
		title  = title.split(":")[1]
		content = get_content_by_uuid(content_lines, uuid)
		notes.append(Notes())
		notes[index].uuid = uuid
		notes[index].title = title
		notes[index].content = content
		if (short == True):
			print(index+1,end="")
                        print(" ", end="")
			print("-> ", end="")
			print(title)
		else:
			#print("----------")
			print(str(index+1)+") ", end="") 
                        print(">>> "+notes[index].title)
			#print("content-> "+notes[index].content,end="")
                        print_content(notes[index].content)
		index = index+1
		
	#close files
	fp_meta.close()
	fp_content.close()
	
def cm_showconfig():
	
	showconfig()

def cm_setdefaultconfig():

	setdefaultconfig() 

def directoryempty(path):
	if len(os.listdir(path))>0:
		return False
	else:
		return True



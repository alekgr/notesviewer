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
from termcolor import colored
from config import *

def get_note_name(uuid):

    notes = get_all_notes(ignore_empty=False)

    for n in notes: 
        meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+n
        meta_fp = open(meta_path)
	meta_lines = meta_fp.readlines()

        for line in meta_lines:
		u = get_uuid(line)
		u = u.split(":")[1]
                if  u == uuid:
                    meta_fp.close()
                    return(n)

	#close files
	meta_fp.close()


def get_note_uuid(note):
    return(note.uuid)

def get_searches_per_line(line):
        return(len(line)/4)

def get_search_number_line(line, num):
        size = get_searches_per_line(line)
        search_index = size-1
        search_index = search_index*3
        return(line[search_index],line[search_index+1],line[search_index+2])

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

def print_search_line(search_line):
    """print search line"""

    index=0
    matches = get_searches_per_line(search_line)
    content = search_line[2]

    for c in content:
        print_char(c, index, search_line)
        index=index+1
    #print("\n",end="")

def print_char(char, index, search_line):
    """print a char match"""

    inside = False 
    matches  = get_searches_per_line(search_line) 
    
    for i in range(matches):
        begin = i*4
        end   = (i*4)+1

        if index >= search_line[begin]:
            if index <= search_line[end]:
                inside = True 
                break;

    if inside == True:
        print(colored(char, "red"),end="")
    if inside == False:
        print(char,end="")
     
def get_content_by_uuid(content_lines, uuid):
    """return a uuid from content_lines"""

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
        """validate an index for a note"""

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
    """print content of a note"""

    l = content_line.split("\\n") 
    for i in l: 
        print(colored(i,vardata.OPTIONS['color_content']))

def print_list_per_line(mylist):
    """print a list"""

    for f in mylist:
	print(colored(f,vardata.OPTIONS['color_note']))

def get_all_notes(ignore_empty=False):
    """return a list of all notes from meta"""

    notes = os.listdir(vardata.base_catagory_path+"/"+"meta")

    #remove the empty file from the notes list if we choose igonore
    if ignore_empty == True:
        for n in notes: 
            if os.stat(vardata.base_catagory_path+"/"+"meta"+"/"+n).st_size == 0:
                notes.remove(n)
        
    return(notes)

def load_notes_enteries(notes):
    """load list of notes into memory"""

    index = 0

    class Notes:
        pass
    
    all_notes_enteries = []

    for n in notes: 
        #get te the fp for each note
        meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+n
        content_path=vardata.base_catagory_path+"/"+"content"+"/"+n
        if  os.path.getsize(meta_path) > 0:
            fp_meta = open(meta_path)    
            meta_lines = fp_meta.readlines() 
        if os.path.getsize(content_path) > 0:
            fp_content = open(content_path)
            content_lines = fp_content.readlines() 
 
            for meta_line in meta_lines:
                uuid = get_uuid(meta_line) 
                uuid = uuid.split(":")[1]
                title = get_title(meta_line)
                title = title.split(":")[1]
                title = remove_newline(title)
                content = get_content_by_uuid(content_lines, uuid)
                content = remove_newline(content)
                all_notes_enteries.append(Notes())
                all_notes_enteries[index].uuid = uuid
                all_notes_enteries[index].title = title
                all_notes_enteries[index].note  = n
                all_notes_enteries[index].content = content
                index = index+1

    return(all_notes_enteries)

def split_multline_note_enteries(notes):
    """ if notes have multiple line split them into seperate enteries"""

    class Notes:
        pass

    splited_notes = []
      
    splited_index = 0
    for note in notes:
        content = note.content.split('\\n')
        if len(content) > 1:
               for c in content:
                   splited_notes.append(Notes())
                   splited_notes[splited_index].uuid = note.uuid
                   splited_notes[splited_index].title = note.title
                   splited_notes[splited_index].note   = note.note
                   splited_notes[splited_index].content = c
                   splited_index = splited_index+1 
        else:
                splited_notes.append(Notes())    
                splited_notes[splited_index].uuid = note.uuid
                splited_notes[splited_index].title = note.title
                splited_notes[splited_index].note  = note.note
                splited_notes[splited_index].content = note.content
                splited_index = splited_index+1

    return(splited_notes)
    
def regex_string(note_enteries,regex):
    """regex notes_eneries"""

    search_list = [] 
    search_lists = []

    #loop over not enteries
    for note_entry in note_enteries:
        del search_list[:]
        for match in re.finditer(regex, note_entry.content):
            start = match.start() 
            end   = match.end()
            search_list.append(start)
            search_list.append(end)
            search_list.append(note_entry.content)
            search_list.append(note_entry.uuid)
        if search_list:
            search_lists.append(list(search_list))
  
    return(search_lists)
    
def cm_version():
    """ print version """
    
    print(colored("Version is "+str(vardata.VERSION),vardata.OPTIONS['color_msg']))

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
		print(colored("The note "+name+" does not exist -- bye", vardata.OPTIONS['color_err'])) 
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
            print(colored("The note "+note+" does not exist -- bye",vardata.OPTIONS['color_err']))
            return(False)

        if not os.path.exists(content_path):
            print(colored("The note  "+note+" content does not exist -- bye", vardata.OPTIONS['color_err']))
            return(False)

	if validate_content_index(entry, note) == False:
            print(colored("entry number is incorrect -- bye",vardata.OPTIONS['color_err']))	
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
		print(colored(name+" Note does not exist",vardata.OPTIONS['color_err']))
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
			print(colored("Deleted the "+name+" note",vardata.OPTIONS['color_msg']))
			return True
		else:
			print(colored("Did not delete "+name+ " note", vardata.OPTIONS['color_err']))
			return False	

def cm_remove(entry, name):
	"""remove entry function"""

	meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name
	content_path=vardata.base_catagory_path+"/"+"content"+"/"+name

	if validate_content_index(entry, name) == False:
            print(colored("entry number is incorrect", vardata.OPTIONS['color_err']))	
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
		print(colored(from_note_path+" from Note does not exist", vardata.OPTIONS['color_err']))
		return False

        #check if to  path exists
        if not os.path.exists(to_meta_path):
		print(colored(to_note_path+" To Note does not exist -- bye  ",vardata.OPTIONS['color_err']))
		return False

        #check if from content exists
        if not os.path.exists(from_content_path):
                print(colored(from_content_path+" From Note content does not exist -- bye",vardata.OPTIONS['color_err']))
                return False

        #check if to content exists
        if not os.path.exists(to_content_path):
                print(colored(to_content_path+" To Note content does not exist",vardata.OPTIONS['color_err']))
                return False

        
        #validate note entry from fromnote
	if validate_content_index(entry, fromnote) == False:
            print(colored("entry number is incorrect -- bye",vardata.OPTIONS['color_err']))	
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
		print(colored("---------",vardata.OPTIONS['color_msg'])) 
		print(colored("Total notes: ",vardata.OPTIONS['color_msg']),end="")
		print(colored(len(os.listdir(vardata.base_catagory_path+"/"+"meta")),vardata.OPTIONS['color_msg']))

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
		print(colored("The note "+note+" does not exist -- bye", vardata.OPTIONS['color_err'])) 
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
			print(colored(title,vardata.OPTIONS['color_title']))
		else:
			#print("----------")
			print(str(index+1)+") ", end="") 
                        print(">>> "+colored(notes[index].title,vardata.OPTIONS['color_title']))
			#print("content-> "+notes[index].content,end="")
                        print_content(notes[index].content)
		index = index+1
		
	#close files
	fp_meta.close()
	fp_content.close()

def cm_search(regex, note, verbose):
    """main search function""" 

    #index for search starts at 1
    index = 1

    #by defatul set it true 
    search_all_notes=True

    #split note argument by comma into notes
    n = note[0]
    notes = n.split(",")

    #cheking for multiple argument with all
    if len(notes) > 1:
        for i in notes:
            if i == "all":
                print("Ambiguity between all and notes")
                return(False)

    #check and set the search_all_notes
    else:
        if notes[0] == "all":
            search_all_notes = True
            
        else:
            search_all_notes = False  
     
    #if we choose all notes 
    if search_all_notes == True:
        notes = get_all_notes(True) 
    
    #load notes info and split if multi line enteries 
    notes_info = load_notes_enteries(notes)
    notes_info = split_multline_note_enteries(notes_info)
   
    #regex the string
    searches = regex_string(notes_info, regex)

    #print output
    for i in searches:
         print(str(index)+ ")", end="")
         print_search_line(i)
         print("\n",end="")
         note_name = get_note_name(i[3])
         print("("+colored(note_name,"green")+")",end="")
         index = index+1
    
def cm_showconfig():
    """show config"""	

    showconfig()

def cm_setdefaultconfig():

	setdefaultconfig() 

def directoryempty(path):
	if len(os.listdir(path))>0:
		return False
	else:
		return True



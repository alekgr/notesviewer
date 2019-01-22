#! /usr/bin/env python3

from termcolor import colored
import os 
import re
import vardata
from file import *


def getpath(name):
        return vardata.base_catagory_path+"/"+name

def is_a_member_of_list(l,item):
    """ utility function to see if item is member of a list"""
  
    is_a_member = False
    
    for i in l:
        if i == item:
            is_a_member = True
            break

    return(is_a_member)

def get_note_name(uuid):

    notes = get_all_notes(ignore_empty=False)

    for n in notes: 
        meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+n
        meta_fp = open_note("meta", n, "r")
        meta_lines = meta_fp.readlines()

        for line in meta_lines:
                u = get_uuid(line)
                u = u.split(":")[1]
                if  u == uuid:
                    meta_fp.close()
                    return(n)

        #close files
        close_note(meta_fp)

def get_all_notes(ignore_empty=False):
    """return a list of all notes from meta"""

    notes = os.listdir(vardata.base_catagory_path+"/"+"meta")

    #remove the empty file from the notes list if we choose igonore
    if ignore_empty == True:
        for n in notes: 
            if os.stat(vardata.base_catagory_path+"/"+"meta"+"/"+n).st_size == 0:
                notes.remove(n)
        
    return(notes)

def get_uuid(str):
        return(str.split(" ",1)[0])

def get_title(str):
        return(str.split(" ",1)[1])

def get_content(str):
        return(str.split(" ",1)[1])

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

def remove_newline(str):
        return(str.replace("\n",""))

def remove_first_and_last_chars(s):
    """remove first and last chars"""

    s = s[1:]
    s = s[:-1]
    return(s)

def removeuuidfromlist(lines, uuid):
    """remove uuid line from list"""

    for i, line in enumerate(lines): 
        line = get_uuid(line)    
        line = line.split(":")[1]
        if line == uuid:
            note = lines.pop(i)
            return(note)

    return(False) 

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
        print(colored(char, vardata.OPTIONS['color_search_string']),end="")
    if inside == False:
        print(char,end="")

def print_content(content_line):
    """print content of a note"""

    l = content_line.split("\\n") 
    for i in l: 
        print(colored(i,vardata.OPTIONS['color_content']))


def get_searches_per_line(line):
        return(len(line)//4)

def get_search_number_line(line, num):
        size = get_searches_per_line(line)
        search_index = size-1
        search_index = search_index*3
        return(line[search_index],line[search_index+1],line[search_index+2])

def validate_content_index(index, name):
        """validate an index for a note"""

        meta_path=vardata.base_catagory_path+"/"+"meta"+"/"+name

        meta_fp = open_note("meta", name, "r")
        lines = meta_fp.readlines()

        i = 0
        for line in lines:
                i = i+1 

        #meta_fp.close()
        close_note(meta_fp)

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


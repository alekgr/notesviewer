#!/usr/bin/env python3

import vardata
import os
import error
from termcolor import colored

modes=("r","w","a","w+")

def open_note(file_context, note, mode):
        """open the meta and return a a fp"""

        #set the path for file_context
        if file_context == 'meta':
            path=vardata.base_catagory_path+"/"+"meta"+"/"+note
        elif file_context == 'content':
            path=vardata.base_catagory_path+"/"+"content"+"/"+note
        elif file_context == 'link':
            path=vardata.base_catagory_path+"/"+"link"+"/"+note 
        elif file_context == 'tag':
            path=vardata.base_catagory_path+"/"+"tags"+"/"+note 
        else:
            return(error.ERROR_WRONG_NOTE_FILE_CONTEXT)

        if not mode in modes: 
            return(error.ERROR_WRONG_MODE)

        fp = open(path,mode)

        if fp == None:
            print(colored("Error while trying to open "+note+" --bye",vardata.OPTIONS['color_err']))

        return fp 

def close_note(fp):
        """ close a file pointer"""
        fp.close()

def verify_note(note, file_context):
        """ check note """
        
        path = getnotepath(note, file_context)
        
        if os.path.exists(path):
            return True 
        else:
            return False

def verify_empty_note(note, file_context):
        """ check note if empty """

        if os.stat(getnotepath(note,file_context)).st_size == 0:
            return True
        else:
            return False
             
def getnotepath(note, file_context):         
        """ return note's path by file_context"""    

        if file_context == 'meta':
            return vardata.base_catagory_path+"/"+"meta"+"/"+note
        elif file_context == 'content':
            return vardata.base_catagory_path+"/"+"content"+"/"+note
        elif file_context == 'link':
            return vardata.base_catagory_path+"/"+"link"+"/"+note 
        elif file_context == 'tag':
            return vardata.base_catagory_path+"/"+"tags"+"/"+note 
        else:
            return(error.ERROR_WRONG_NOTE_FILE_CONTEXT)


def print_msg(color, msg):
        """ print msg at color base """

        print(colored(msg, color))
        

def print_err_msg(msg):
        """ print error msg with correct color"""   

        print(colored(msg, vardata.OPTIONS['color_err']))

def print_info_msg(msg):
        """ print info msg with correct color"""

        print(colored(msg, vardata.OPTIONS['color_msg']))

def print_list_per_line(mylist):
    """print a list"""

    for f in mylist:
        print(colored(f,vardata.OPTIONS['color_note']))


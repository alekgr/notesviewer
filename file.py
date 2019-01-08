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


        #check if file exists
        if not os.path.exists(path):
            print(colored("The note "+note+" "+file_context+" file does not exist -- bye",vardata.OPTIONS['color_err']))
            exit() 

        fp = open(path,mode)

        if fp == None:
            print(colored("Error while trying to open "+note+" --bye",vardata.OPTIONS['color_err']))

        return fp 

def close_note(fp):
        """ close a file pointer"""
        fp.close()

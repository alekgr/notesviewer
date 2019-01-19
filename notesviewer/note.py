#!/usr/bin/env python3

import subprocess
import tempfile
import os
from  utils import *
from  file  import *

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
            fp_meta = open_note("meta", n, "r")
            meta_lines = fp_meta.readlines() 
        if os.path.getsize(content_path) > 0:
            fp_content = open_note("content", n, "r")
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
 

def inspect_note(note):
    """ check note for any inconsistencies or corruption"""

    note_error = {'meta':True, 'content':True, 'link':True, 'tags':True}   
   
    note_error['meta'] = verify_note(note, "meta")
    note_error['content'] = verify_note(note, "content")
    note_error['link']    = verify_note(note, "link")
    note_error['tags']    = verify_note(note,  "tag")
   
    return note_error

def get_note_uuids(note):
    """ check index between meta and content """ 

    meta_uuid = [] 
    content_uuid = []
    match_uuids = []

    meta_fp     = open_note("meta", note, "r")
    content_fp  = open_note("content", note, "r")
   
    meta_lines      = meta_fp.readlines()
    content_lines   = content_fp.readlines()
    

    for line in meta_lines:
        m_uuid  = get_uuid(line)
        m_uuid = m_uuid.split(":")[1]
        meta_uuid.append(m_uuid)
        
         
    for line in content_lines:
        c_uuid = get_uuid(line)
        c_uuid = c_uuid.split(":")[1]
        content_uuid.append(c_uuid)
       

    close_note(meta_fp)
    close_note(content_fp)

    return meta_uuid, content_uuid

import sys
import uuid
import error
import stat
from note import *
from utils import *
from config import showconfig,setdefaultconfig
from  file import *


def cm_version():
    """ print version """
    
    print(colored("Version is "+str(vardata.VERSION),vardata.OPTIONS['color_msg']))
    note_status = inspect_note("testing2")
    print(note_status['meta'])

def cm_add(name, verbose):
        """add a note"""

        #file permission
        mode = 0o600 | stat.S_IRUSR

        meta_path       =   getnotepath(name, "meta")
        content_path    =   getnotepath(name, "content")
        tag_path        =   getnotepath(name, "tag") 
        link_path       =   getnotepath(name, "link")

        #create the note files

        if verify_note(name, "meta") == True:
            print_err_msg("The note "+name+" already exists")
            exit(error.ERROR_META_FILE_ALREADY_EXISTS)
        else:
            os.mknod(meta_path,mode)
            os.mknod(content_path,mode)
            os.mknod(tag_path,mode)
            os.mknod(link_path,mode)
            print_info_msg("Added "+name+" note")
        
def cm_insert(name, title):
        """Insert a note with a title"""

        # verfiy note
        if verify_note(name, "meta") == False:
            print_err_msg("The meta note "+name+" does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)
        if verify_note(name, "content") == False:
            print_msg("The content "+name+" does not exist -- bye")
            exit(error.ERROR_NO_CONTENT_FILE)

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
        fp_meta    = open_note("meta", name, "a") 
        fp_content  = open_note("content", name, "a")

        #write to meta
        meta_buffer_string = "uuid:"+str(note_uuid)+" "+"title:"+title
        fp_meta.write(meta_buffer_string+"\n")

        #write to content
        content_buffer_string = "uuid:"+str(note_uuid)+" "+"content:"+str_content
        fp_content.write(content_buffer_string+"\n")

        #close files
        close_note(fp_meta)
        close_note(fp_content)

def cm_edit(entry, note):
        """edit  a note entry"""
        
        # verfiy note
        if verify_note(note, "meta") == False:
            print_err_msg("The meta note "+note+" does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)
        if verify_note(note, "content") == False:
            print_msg("The content "+note+" does not exist -- bye")
            exit(error.ERROR_NO_CONTENT_FILE)

        if validate_content_index(entry, note) == False:
            print(colored("entry number is incorrect -- bye",vardata.OPTIONS['color_err']))     
            return(False)
        else:
            fp_content = open_note("content", note, "r") 
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
            close_note(fp_content)
           
            #fill content_lines to one that we edited
            content_lines [entry-1] = "uuid"+":"+content_uuid+" "+"content"+":"+c+"\n"
            
            #convert content_lines list to string
            str_content_lines = ""
            str_content_lines = str_content_lines.join(content_lines)

            #write back to content file
            fp_content = open_note("content", note, "w+")
            fp_content.write(str_content_lines)
            close_note(fp_content)


def cm_delete(name):
        """delete a note"""     

        if verify_note(name, "meta") == False:
            print_err_msg("The meta note "+name+" does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)
        else:
            prompt = input("Are you sure you want to delete "+name+" (yes/no) ")
            prompt = prompt.lower()
            if prompt == "yes":
                os.remove(getnotepath(name, "meta"))
                if verify_note(name, "content") == True:
                    os.remove(getnotepath(name, "content"))
                if verify_note(name, "link") == True:
                    os.remove(getnotepath(name, "link"))
                if verify_note(name, "tag") == True:
                    os.remove(getnotepath(name, "tag"))

                print_info_msg("Deleted "+name+" note") 

def cm_remove(entry, name):
        """remove entry function"""

       # verfiy note and entry 
        if verify_note(name, "meta") == False:
            print_err_msg("The meta note "+name+" does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)
        if verify_note(name, "content") == False:
            print_msg("The content "+name+" does not exist -- bye")
            exit(error.ERROR_NO_CONTENT_FILE)
        if validate_content_index(entry, name) == False:
            print_err_msg("Note entry number is incorrect")
            exit(error.ERROR_INVALID_INDEX)

        else:
            fp_meta =  open_note("meta", name, "r")
            fp_content = open_note("content", name, "r")
            meta_lines = fp_meta.readlines()
            content_lines = fp_content.readlines()
            uuid_meta = getuuidbyindex(meta_lines, entry)
            uuid_content = getuuidbyindex(content_lines, entry)
            removeuuidfromlist(meta_lines, uuid_meta)
            removeuuidfromlist(content_lines, uuid_content)
            string_meta = ''.join(meta_lines)
            string_content = ''.join(content_lines)
            close_note(fp_meta)
            close_note(fp_content)
           
            #open files(content and meta) for writting
            fp_meta = open_note("meta", name, "w")
            fp_content = open_note("content", name, "w")
            fp_meta.write(string_meta) 
            fp_content.write(string_content)
            close_note(fp_meta)
            close_note(fp_content)

            print_info_msg("Removed "+name+" Note")
        
            return string_content

def cm_move(entry, fromnote, tonote):
        """move an  entry from fromnote to tonote"""
        
        if verify_note(fromnote, "meta") == False:
                print_err_msg("The fromnote "+fromnote+" does not exist -- bye")
                exit(error.ERROR_NO_META_FILE)

        if verify_note(tonote, "meta") == False:
                print_err_msg("The tonote "+tonote+" does not exist -- bye")
                exit(error.ERROR_NO_META_FILE)


        if verify_note(fromnote, "content") == False:
                print_err_msg("The fromnote "+fromnote+" content does not exist --bye")
                exit(error.ERROR_NO_CONTENT_FILE)


        if verify_note(tonote, "content") == False:
                print_err_msg("The tonote "+tonote+" content does not exist --bye")
                exit(error.ERROR_NO_CONTENT_FILE)

        
        #validate note entry from fromnote
        if validate_content_index(entry, fromnote) == False:
            print(colored("entry number is incorrect -- bye",vardata.OPTIONS['color_err']))     
            return False
                
        
        #open files(content and meta) for reading 
        fp_meta_from    = open_note("meta",fromnote,"r") 
        fp_content_from = open_note("content", fromnote,"r")

        meta_lines = fp_meta_from.readlines()
        content_lines = fp_content_from.readlines()
        uuid_meta = getuuidbyindex(meta_lines, entry)
        uuid_content = getuuidbyindex(content_lines, entry)
        remove_note_meta = removeuuidfromlist(meta_lines, uuid_meta)
        remove_note_content = removeuuidfromlist(content_lines, uuid_content)
        string_meta = ''.join(meta_lines)
        string_content = ''.join(content_lines)
        close_note(fp_meta_from)
        close_note(fp_content_from)

           
        #open files(content and meta) for writting
        fp_meta_from    = open_note("meta",fromnote,"w")
        fp_content_from = open_note("content",fromnote,"w")
        fp_meta_from.write(string_meta) 
        fp_content_from.write(string_content)
        close_note(fp_meta_from)
        close_note(fp_content_from)


        #Insert a note with a title for the move"""

        #open meta and content files
        fp_meta = open_note("meta", tonote, "a")
        fp_content = open_note("content", tonote, "a")

        #write to meta
        fp_meta.write(remove_note_meta)

        #write to content
        fp_content.write(remove_note_content)

        print_info_msg("The note entry "+str(entry)+" at "+fromnote+" has been moved to "+tonote)

        #close files
        close_note(fp_meta)
        close_note(fp_content)


def cm_addtags(note, tag):
        """ adding tags to note file"""

        duplicate_tags = [] 

        #get all the tags
        tags = tag.split(',')
  
        if verify_note(note, "meta") == False:
            print_err_msg(note+" Note does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)
        
        if verify_note(note, "tag") == False:
            print_err_msg(note+ " Tag file does not exist -- bye") 
            exit(error.ERROR_NO_META_FILE)
    
        #read tags for existing tag
        fp_tags_read = open_note("tag", note, "r") 
        lines=fp_tags_read.readlines()
        for line in lines:
            line = remove_newline(line) 
            for t in tags:
                if t == line:
                   duplicate_tags.append(t)
                   break; 
        #close tag file
        close_note(fp_tags_read)

        #open tag file 
        fp_tags  = open_note("tag", note, "a")
       
        #write tag(s) to tag file
        for t in tags:
            if is_a_member_of_list(duplicate_tags,t) == True:
                print(colored(t+" is already a tag",vardata.OPTIONS['color_msg']))
            else:
                fp_tags.write(t+"\n") 
                print_info_msg("Added "+"#"+t+" tag")
        #close tag file  
        close_note(fp_tags)

def cm_tags(note):
        """show tags for a note"""


        if verify_note(note, "meta") == False:
            print_err_msg(note+ " Note does not exist --bye")
            exit(error.ERROR_NO_META_FILE)

        if verify_note(note, "tag") == False:
            print_err_msg(note+ " Tag file does not exist --bye")
            exit(error.ERROR_NO_TAG_FILE)

        fp_tags = open_note("tag", note, "r")

        lines = fp_tags.readlines()
        for line in lines:
            line = "#"+line
            print(colored(line,vardata.OPTIONS['color_msg']),end="")

        close_note(fp_tags) 


def cm_removetags(note, tags):
        """ remove tag(s) for a note """

        removed_lines = []

        tag_list = tags.split(',')

        if verify_note(note, "meta") == False:
            print_err_msg(note+ " Note does not exist --bye")
            exit(error.ERROR_NO_META_FILE)
        
        if verify_note(note, "tag") == False:
            print_err_msg(note+ " Note tag file does not exist --bye")
            exit(error.ERROR_NO_TAG_FILE)

        #open file and readlines
        fp_tags = open_note("tag", note, "r")
        lines = fp_tags.readlines()

        #move item's not to be removed
        for line in lines:
            line = remove_newline(line)
            if is_a_member_of_list(tag_list,line) == False:
                removed_lines.append(line)  

        #write to tag file 
        fp_tags_removed = open_note("tag", note, "w")
        removed_tag_strings = '\n'.join(removed_lines)
        removed_tag_strings = removed_tag_strings+"\n"
        fp_tags_removed.write(removed_tag_strings)

        print_info_msg("Removed "+tags)

        #close files 
        close_note(fp_tags)
        close_note(fp_tags_removed)
         
def cm_list(verbose):
        """ print nameo of the notes"""

        notes = os.listdir(vardata.base_catagory_path+"/"+"meta")
        if verbose == False:
            print_list_per_line(os.listdir(vardata.base_catagory_path+"/"+"meta"))

        else:
            for note in notes:
                if verify_empty_note(note,"meta") == True:
                    print_msg(vardata.OPTIONS['color_note'],note+" "+"(empty)")
                else:
                    path_meta = getnotepath(note, "meta")
                    path_content = getnotepath(note, "content")
                    path_tags    = getnotepath(note, "tag")
                    path_links    = getnotepath(note, "link")
                    size_meta = os.stat(path_meta)
                    size_content = os.stat(path_content)
                    size_tags   = os.stat(path_tags)
                    size_link   = os.stat(path_links)
                    size_total = size_meta.st_size+size_content.st_size+size_tags.st_size+size_link.st_size
                    print_msg(vardata.OPTIONS['color_note'], note+" ("+str(size_total)+"b)") 

        
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
        #        return

        if verify_note(note, "meta") == False:
            print_err_msg("The note "+note+" does not exist -- bye")
            exit(error.ERROR_NO_META_FILE)

        if verify_empty_note(note, "meta"):
            print_info_msg("Empty note")
            exit(error.ERROR_OK)


        #open meta and content files
        fp_meta    = open_note("meta", note, "r") 
        fp_content = open_note("content", note, "r")

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
        close_note(fp_meta)
        close_note(fp_content)

def cm_search(regex, note):
    """main search function""" 

    #index for search starts at 1
    index = 1

    #by defatul set it true 
    search_all_notes=True

    #split note argument by comma into notes
    #n = note[0]
    notes = note.split(",")

    

    #cheking for multiple argument with all
    if len(notes) > 1:
        for i in notes:
            if i == "all":
                print_err_msg("Ambiguity between all and notes")
                exit(error.ERROR_SEARCH_NOTE_AMBIGUITY)
            elif verify_note(i, "meta") == False:
                print_err_msg("The note "+i+" does not exist -- bye")

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
         note_name = get_note_name(i[3])
         print(" ("+colored(note_name,vardata.OPTIONS['color_search_notename'])+")")
         index = index+1

def cm_check():
   
    print("Checking notes files..")

    notes = os.listdir(vardata.base_catagory_path+"/"+"meta")   
   
    for n in notes:
        status = inspect_note(n)
        print("Checking "+n)
        
        if status['meta'] == True:
            print_info_msg("meta..OK")
        else:
            print_err_msg('meta..MISSING') 

        if status['content'] == True:
            print_info_msg("content..OK")
        else:
            print_err_msg('content..MISSING') 

        if status['link'] == True:
            print_info_msg("link..OK")
        else:
            print_err_msg('link..MISSING')  
       
        if status['tags'] == True:
            print_info_msg("tags..OK")
        else:
            print_err_msg('tags..MISSING') 

    print("\n")
   
    #check for index mismatch
    print("Chekcing notes metadata..")
    for note in notes: 
        print("checking "+note)
        #ignore empty notes
        if verify_empty_note(note, "meta") == True:
            print_info_msg(note+ "(Ignoring ..empty)")
            continue
        meta_uuid, content_uuid = get_note_uuids(note)
        meta_size = len(meta_uuid)
        content_size = len(content_uuid)
        if meta_size == content_size:
            for index in range(meta_size):
                if meta_uuid[index] == content_uuid[index]:
                    print_info_msg(meta_uuid[index]+"..,passed")
                else:
                    print_err_msg(meta_uuid[index]+"...not passed")
        else:
            print_err_msg("Note entry mismatch")

def cm_showconfig():
    """show config"""   

    showconfig()

def cm_info():
    """info display pyton and modueles version"""
    
    print("Major Version:"+str(sys.version_info.major))
    print("Minor Version:"+str(sys.version_info.minor))
    print("Micro Version:"+str(sys.version_info.micro))
    print("Release Version:"+str(sys.version_info.releaselevel))
    print("Serial Release number:"+str(sys.version_info.serial))
    print(sys.version)
    print("Platform:"+sys.platform)
    print("Os name:"+os.name)

def cm_setdefaultconfig():

        setdefaultconfig() 


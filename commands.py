from core import *

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
                prompt = input("Are you sure you want to delete "+name+" (yes/no) ")        #prompt
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



def cm_addtags(note, tag):
        """ adding tags to note file"""

        duplicate_tags = [] 

        #get all the tags
        tags = tag.split(',')
  
        meta_path = vardata.base_catagory_path+"/"+"meta"+"/"+note
        tag_path = vardata.base_catagory_path+"/"+"tags"+"/"+note

        #check if meta path exists
        if not os.path.exists(meta_path):
                print(colored(note+"Note does not exist", vardata.OPTIONS['color_err']))
                return False

        #check if tags file exists
        if not os.path.exists(tag_path):
                print(colored(note+"Tags note file does not exist", vardata.OPTIONS['color_err']))
                return False
        

        #read tags for existing tag
        fp_tags_read=open(tag_path,"r")
        lines=fp_tags_read.readlines()
        for line in lines:
            line = remove_newline(line) 
            for t in tags:
                if t == line:
                   duplicate_tags.append(t)
                   break; 
        #close tag file
        fp_tags_read.close()

        #open tag file 
        fp_tags = open(tag_path, "a")
       
        #write tag(s) to tag file
        for t in tags:
            if is_a_member_of_list(duplicate_tags,t) == True:
                print(colored(t+" is already a tag",vardata.OPTIONS['color_msg']))
            else:
                fp_tags.write(t+"\n") 
                print(colored("Added "+t, vardata.OPTIONS['color_msg']))
        #close tag file  
        fp_tags.close() 

def cm_tags(note):
        """show tags for a note"""

        meta_path = vardata.base_catagory_path+"/"+"meta"+"/"+note
        tag_path = vardata.base_catagory_path+"/"+"tags"+"/"+note

        #check if meta path exists
        if not os.path.exists(meta_path):
            print(colored(note+"Note does not exist", vardata.OPTIONS['color_err']))
            return False
        
        #check if tags file exists
        if not os.path.exists(tag_path):
                print(colored(note+"Tags note file does not exist", vardata.OPTIONS['color_err']))
                return False

        fp_tags = open(tag_path, "r")

        lines = fp_tags.readlines()
        for line in lines:
            line = "#"+line
            print(colored(line,vardata.OPTIONS['color_msg']),end="")


def cm_removetags(note, tags):
        """ remove tag(s) for a note """

        removed_lines = []

        tag_list = tags.split(',')

        meta_path = vardata.base_catagory_path+"/"+"meta"+"/"+note
        tag_path = vardata.base_catagory_path+"/"+"tags"+"/"+note

        #check if meta path exists
        if not os.path.exists(meta_path):
            print(colored(note+"Note does not exist", vardata.OPTIONS['color_err']))
            return False
        
        #check if tags file exists
        if not os.path.exists(tag_path):
                print(colored(note+"Tags note file does not exist", vardata.OPTIONS['color_err']))
                return False

        #open file and readlines
        fp_tags = open(tag_path, "r")
        lines = fp_tags.readlines()

        #move item's not to be removed
        for line in lines:
            line = remove_newline(line)
            if is_a_member_of_list(tag_list,line) == False:
                removed_lines.append(line)  

        #write to tag file 
        fp_tags_removed=open(tag_path, "w")         
        removed_tag_strings = '\n'.join(removed_lines)
        removed_tag_strings = removed_tag_strings+"\n"
        fp_tags_removed.write(removed_tag_strings)

        #close files 
        fp_tags.close()
        fp_tags_removed.close()
         
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
         note_name = get_note_name(i[3])
         print(" ("+colored(note_name,vardata.OPTIONS['color_search_notename'])+")")
         index = index+1
    
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


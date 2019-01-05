""" global variable list """

from os.path import expanduser

home = expanduser("~")
program_name="noteviewer"


#global constant variables
interactive_commands = [        ['list_catagories', 'edit', 'search', 'settings', 'version', 'quit'],
                                                                ['graphical on', 'Scope', 'verbose on', 'exit','quit'],                  
                                                                ['global', 'catagory', 'note', 'comment','exit','quit'] ]
#command mode
command_mode = interactive_commands[0] 

#config file
config_file = "config"
config_file_path = home+"/"+"."+program_name+"/"+config_file

#buffer location where all the work is being done 
repo_dir = home+"/"+"notes"

base_catagory_path="test"

#version
VERSION = 1.0


GRAPHICAL_DEFAULT = False 
VERBOSE_DEFAULT = False 
EDITOR_DEFAULT = "vim"
COLOR_ERR_DEFAULT = "red"
COLOR_MSG_DEFAULT = "grey"
COLOR_NOTE_DEFAULT  = "yellow"
COLOR_NOTE_TITLE_DEFAULT    = "blue"
COLOR_NOTE_CONTENT_DEFAULT  = "green"
COLOR_SEARCH_STRING_DEFAULT = "blue"
COLOR_SEARCH_NOTE_DEFAULT   = "green"
DATA_DEFAULT = "file"+":"+home+"/"+"notes"

EDITORS = ['vim','emacs']
COLORS  = ['red','blue','green','yellow', 'black','white']

protocol_git  = "git"
protocol_file = "file" 

OPTIONS  = {
        "graphical":            GRAPHICAL_DEFAULT,
        "verbose":                      VERBOSE_DEFAULT,
        "editor":                       EDITOR_DEFAULT,
        "color_err":            COLOR_ERR_DEFAULT,
        "color_msg":            COLOR_MSG_DEFAULT,
        "color_note":           COLOR_NOTE_DEFAULT,
        "color_title":          COLOR_NOTE_TITLE_DEFAULT,
        "color_content":        COLOR_NOTE_CONTENT_DEFAULT,
        "color_search_string":  COLOR_SEARCH_STRING_DEFAULT,
        "color_search_notename":COLOR_SEARCH_NOTE_DEFAULT,
        "data_location":        DATA_DEFAULT
        }



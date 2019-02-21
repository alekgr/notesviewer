""" Module file """

import os
import stat
from termcolor import colored
import notesviewer.vardata
import notesviewer.error

MODES = ("r", "w", "a", "w+")


def open_note(file_context, note, mode):
    """open the meta and return a a fp"""

    # set the path for file_context
    if file_context == 'meta':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta" + "/" + note
    elif file_context == 'content':
        path = (notesviewer.vardata.NOTES_ROOT_PATH + "/"
                + "content" + "/" + note)
    elif file_context == 'link':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link" + "/" + note
    elif file_context == 'tag':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags" + "/" + note
    else:
        return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT

    if mode not in MODES:
        return notesviewer.error.ERROR_WRONG_MODE

    fileptr = open(path, mode)

    if fileptr is None:
        print(colored("Error while trying to open " + note + " --bye",
                      notesviewer.vardata.OPTIONS['color_err']))

    return fileptr


def close_note(filepointer):
    """ close a file pointer"""
    filepointer.close()


def create_config_file():
    """ create config file """

    mode = 0o600 | stat.S_IRUSR

    error = os.mknod(notesviewer.vardata.CONFIG_FILE_PATH, mode)
    if error is not None:
        print_err_msg("There was error creating config file "+ notesviewer.vardata.CONFIG_FILE_PATH)
        exit(-1)
    else:
        print_info_msg("Created config file at "+notesviewer.vardata.CONFIG_FILE_PATH)
        notesviewer.commands.setdefaultconfig()

def verify_note(note, file_context):
    """ check note """
    path = getnotepath(note, file_context)
    if os.path.exists(path):
        return True
    return False


def verify_empty_note(note, file_context):
    """ check note if empty """

    if os.stat(getnotepath(note, file_context)).st_size == 0:
        return True
    return False


def getnotepath(note, file_context):
    """ return note's path by file_context"""

    if file_context == 'meta':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta" + "/" + note
    if file_context == 'content':
        return  \
            notesviewer.vardata.NOTES_ROOT_PATH + "/" + "content" + "/" + note
    if file_context == 'link':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link" + "/" + note
    if file_context == 'tag':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags" + "/" + note
    return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT


def print_msg(color, msg):
    """ print msg at color base """

    print(colored(msg, color))


def print_err_msg(msg):
    """ print error msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_err']))


def print_info_msg(msg):
    """ print info msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_msg']))


def print_list_per_line(mylist):
    """print a list"""

    for index in mylist:
        print(colored(index, notesviewer.vardata.OPTIONS['color_note']))

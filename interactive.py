#!/usr/bin/env python3


from  vardata import *
from  core import *
from  commands import *
import argparse
import curses
import readline 
import configparser


def checkinput(text):

        global command_mode

        for index       in command_mode:
                if text == index:
                                return True
        return False

def interactive():
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
        prompt=""
        while input != 'quit':
                readline.set_completer(completer)
                readline.parse_and_bind("tab: complete")
                prompt = input(">>> ")       
                if checkinput(prompt) == False:
                        print("Unknown Command")
                else:
                        process_interactive_command(prompt)              

def process_interactive_command(input):

        if input == "version":
                cm_version()
        if input == "settings":
                print("Choose your settings..")
                cm_setcommand_mode(1)   
        if input == "scope":
                cm_setcommand_mode(2) 
        if input == "exit":
                if command_mode == commands_settings:
                                cm_setcommand_mode(1)

def completer(text, state):
        """ custome completer function for readline autocompletion      """
        cmnds = [x for x in command_mode if x.startswith(text)]
        
        try:
                return cmnds[state]

        except IndexError:
                return None

def cm_add(ignored):
        
        """ add command """
        pass


def cm_setcommand_mode(mode):
        """ set command to point to list index """

        global command_mode
        if mode == 0:
                command_mode = interactive_commands[0]  
        if mode == 1:
                command_mode =  interactive_commands[1]
        if mode == 2:
                command_mode = interactive_commands[2]
                
def get_mode():
        """ return command_mode list index """  

        count = 0
        for i in interactive_commands:
                if i == command_mode:
                        return(count)
                count = count+1                 


#!/usr/bin/env python


if __name__ == "__main__":

	from vardata import *
	from interactive import *
	from core import *
	from config import *


	def ParseArguments():

		#create the root parser
		parser = argparse.ArgumentParser()

		#create subparser
		subparser  = parser.add_subparsers(dest='cmd')

		#version command
		version_parser = subparser.add_parser('version')
		
		#add
		add_parser = subparser.add_parser('add')
		add_parser.add_argument('name', action='store')
		add_parser.add_argument('--verbose', '-v', action='store_true')	

		
		#insert
		add_parser = subparser.add_parser('insert')
		add_parser.add_argument('name', action='store')
		add_parser.add_argument('title', action='store')


		#delete
		delete_parser = subparser.add_parser('delete')
		delete_parser.add_argument('name', action='store')

		#list
		list_parser = subparser.add_parser('list')
		list_parser.add_argument('--verbose', '-v', action='store_true')

		#display
		display_parser = subparser.add_parser('display')
		display_parser.add_argument('note', action='store')
		display_parser.add_argument('--short', '-s', action='store_true')

		#showconfig
		showconfig_parser = subparser.add_parser('showconfig')

		#setdefaultconfig
		setdefaultconfig_parser = subparser.add_parser('setdefaultconfig')

		#search
		search_parser = subparser.add_parser('search')
		search_parser.add_argument('what', action='store')
		search_parser.add_argument('object', action='store', choices=['all', 'catagory','note','title'], default='all')
		search_parser.add_argument('--verbose', '-v', action='store_true')

		#interactive
		interactive_parser = subparser.add_parser('interactive')

		#parse user arguments
		args = vars(parser.parse_args())
		process_args(args)


	def process_args(argument):
		if argument['cmd'] == 'version':
			cm_version()
		elif argument['cmd'] == 'list':
			cm_list(argument['verbose'])
		elif argument['cmd'] == 'add':
			cm_add(argument['name'], argument['verbose'])
		elif argument['cmd'] == 'insert':
			cm_insert(argument['name'], argument['title'])
		elif argument['cmd'] == 'delete':
			cm_delete(argument['name'])
		elif argument['cmd'] == 'display':
			cm_display(argument['note'],argument['short'])
		elif argument['cmd'] == 'showconfig':
			cm_showconfig()	
		elif argument['cmd'] == 'setdefaultconfig':
			cm_setdefaultconfig()
		elif argument['cmd'] == 'search':
			print('searching')
		elif argument['cmd'] == 'interactive':
			interactive()
			
	loadconfig() 
	set_data_location()
	ParseArguments()


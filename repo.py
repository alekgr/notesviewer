#! /usr/bin/env python

import os
from git import Repo

def  note_clone(url, directory):

	if not os.path.isdir(directory+"/"+".git"):
		Repo.clone_from(url, directory)

def cleanuplocalrepository():
	pass

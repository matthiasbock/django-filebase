#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os

def recurse( path ):
	print path
	os.system('wget http://127.0.0.1/filebase/ --post-data="path='+path+'" --quiet --output-document=- > /dev/zero')
	for item in os.listdir( path ):
		d = path.rstrip("/")+"/"+item
		if os.path.isdir( d ):
			recurse( d )

recurse( os.getcwd() )

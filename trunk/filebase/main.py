# -*- coding: iso-8859-15 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from Django.globals import *
from Django.filebase.models import *

from FileBase import *

# http://code.google.com/p/pyftpdlib/
# http://code.google.com/p/pyfilesystem/
# http://code.google.com/p/mogilefs/

def index( request ):
	try:
		request.session["path"] = request.session["path"]+"/"+request.GET.get("path")
		return HttpResponseRedirect(".")
	except:
		request.session["path"] = "/"

	params = { "path":request.session["path"] }
	return render_to_response("index.html", params)


def filesystem( request ):
	params			= {}
	params["Folders"]	= []
	params["Files"]		= []

	request.session["path"] = "/home/user"

	for entry in sorted( os.listdir( request.session["path"] ) ):
		fullpath = os.path.join(request.session["path"], entry)
		if os.path.isdir( fullpath ):
			params["Folders"].append( entry )
		elif os.path.isfile( fullpath ):
			params["Files"].append( entry )

	return render_to_response("filesystem.html", params)


def database( request ):
	params = {}
#	params["boxes"]			= []

#	FolderLeft			= request.GET.get("FolderLeft")
#	params["boxes"].append( { "Folders":Folders.objects.using( FileBaseDB ).filter( parent=FolderLeft ), "Files":Files.objects.using( FileBaseDB ).filter( folder=FolderLeft ) } )

	return render_to_response("database.html", params)


def details( request ):
	return None

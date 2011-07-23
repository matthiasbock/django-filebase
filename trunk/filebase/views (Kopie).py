# -*- coding: iso-8859-15 -*-

from FileBase.main.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import os
import hashlib
import zlib
import magic
import time
import urllib

def largefileMD5( filename ):
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()

def Adler32( filename ):
	CRC = ""
	chunksize = 102400 # 100*1024
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(chunksize), ''): 
			a = long(zlib.adler32( chunk ) & 0xffffffff)
			b1 = a >> 24
			b2 = (a >> 16) & 255
			b3 = (a >> 8) & 255
			b4 = a & 255
			CRC = CRC + chr(b1) + chr(b2) + chr(b3) + chr(b4)
	return CRC

def handlefile( f, Parent, _directories, _adler32, _thumbnails ):
	s = f.split("/")
	Name = s[len(s)-1]
	new = False

	Bytes = os.path.getsize( f )		# Bytes, MD5 ? ...
	MD5 = largefileMD5( f )
	try:					# kennen wir diesen Content schon ?
		C = Content.objects.get( bytes=Bytes, md5=MD5 )
	except:
		C = None
	if C == None:				# Nein:
		new = True
		if _adler32:
			adler32 = Adler32( f )
		else:
			adler32 = None
		Magic = magic.open( magic.MAGIC_NONE )
		Magic.load()
		MIME =  Magic.file( f )
		Magic.close()
		if _thumbnails:
			pass # später: Windows EXE-Icon extrahieren, JPEG-Thumbnails extrahieren, BMP-Thumbnails erzeugen ...
		else:
			Thumbnail = None
			ThumbExt = None
		C = Content.objects.create( bytes=Bytes, md5=MD5, adler32_100kb=adler32, mime=MIME, thumbnail=Thumbnail, thumbext=ThumbExt )
		C = Content.objects.get( bytes=Bytes, md5=MD5 )

	Change = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( os.path.getctime(f) ))		# Zeitstempel der Datei abrufen
	Access = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( os.path.getatime(f) ))
	Modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( os.path.getmtime(f) ))
	try:
		F = Files.objects.get( name=Name, lastmodification=Modification, content=C.id )		# haben wir diese Datei schon in der DB?
	except:
		F = None
	if F == None:				# Nein:
		new = True
		F = Files.objects.create( name=Name, created=Change, lastaccess=Access, lastmodification=Modification, content=C.id )
		F = Files.objects.get( name=Name, lastmodification=Modification, content=C.id )

	if _directories:
		try:
			FF = FileFolder.objects.get( file=F.id, folder=Parent )		# wissen wir schon, wo diese Datei ist?
		except:
			FF = None
		if FF == None:				# Nein:
			FF = FileFolder.objects.create( file=F.id, folder=Parent )
	else:
		FF = None

	return new, F, C

def recurse( path, _recursive, _files, _adler32, _directories, _thumbnails, files, Parent ): 		# Ordner rekursiv einlesen
	List = os.listdir( path )									# vor der Prozessierung bissel sortieren
	FileList = []
	DirList = []
	path = path.decode("UTF-8")
	for Name in List:
		Name = Name.decode("UTF-8")
		f = path+"/"+Name
		f = f.encode("UTF-8")
		if os.path.isfile( f ):
			FileList.append( Name )
		elif os.path.isdir( f ):
			DirList.append( Name )
	FileList = sorted( FileList )
	DirList = sorted( DirList )
	List = FileList + DirList
	for Name in List:										# für alle Verzeichniseinträge ...
		f = path+"/"+Name
		f = f.encode("UTF-8")

		if os.path.isfile( f ) and _files:		#   ist es eine Datei:
			new, F, C = handlefile( f, Parent, _directories, _adler32, _thumbnails )
			if new:
				files.append( {"name":F.name, "created":F.created, "lastaccess":F.lastaccess, "lastmodification":F.lastmodification, "content":C} )

		elif os.path.isdir( f ):			#   ist es ein Ordner:
			if _directories:
				try:
					D = Folders.objects.get( name=Name, parent=Parent )	# haben wir diesen Ordner schon in der DB?
				except:
					D = None
				if D == None:				# Nein:
					Modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( os.path.getmtime(f) ))
					D = Folders.objects.create( name=Name, created=Modification, parent=Parent )
					D = Folders.objects.get( name=Name, parent=Parent )
			if _recursive:
				files = recurse( f, _recursive, _files, _adler32, _directories, _thumbnails, files, D.id )
	return files

def recurser( request ):
	params = {}
	if request.method == "GET":
		return render_to_response("path.html")
	elif request.method == "POST":		
		path = request.POST.get("path").rstrip("/")
		try:
			_recursive = request.POST.get("recursive") != None
		except:
			_recursive = False
		try:
			_files = request.POST.get("files") != None
		except:
			_files = False
		try:
			_adler32 = request.POST.get("adler32") != None
		except:
			_adler32 = False
		try:
			_directories = request.POST.get("directories") != None
		except:
			_directories = False
		try:
			_thumbnails = request.POST.get("thumbnails") != None
		except:
			_thumbnails = False
		params["files"] = recurse( path, _recursive, _files, _adler32, _directories, _thumbnails, [], 1 )
		return render_to_response("results.html", params)

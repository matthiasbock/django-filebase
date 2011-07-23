# -*- coding: iso-8859-15 -*-

from Django.globals import *
from Django.filebase.models import *

import os
import hashlib
import zlib
import time
import datetime


def largefileMD5( filename ):					# MD5-Summe einer Datei erstellen
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()


def Adler32( filename ):					# Adler32-Summe einer Datei erstellen
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


class Folder:

	def __init__(self, ID=None, Path=None):
		self.DEBUG = ""
		self.ID = None
		if ID is not None:
			self.LoadID( ID )
		if Path is not None:
			self.LoadPath( Path )

	def LoadID( ID ):									# Lade den Datenbankeintrag eines Ordners
		self.DEBUG += "Loading database folder #"+str(ID)+" ...\n"
		try:
			self.QueryResult = Folders.objects.using( FileBaseDB ).get( id=ID )
		except:
			self.DEBUG += "Error: Folder not found\n"
			return False
		self.ID		= self.QueryResult.id
		self.Parent	= self.QueryResult.parent
		self.Name	= self.QueryResult.name
		self.Path	= None
		self.Exists	= None
		return True


	def LoadPath( Path, AddMissing=True ):						# Lade einen Ordner anhand des Pfades
											# Erstelle -falls nötig- fehlende Datenbankeinträge
		self.DEBUG += "Loading folder "+Path+" ...\n"
		Path = Path.strip("/").split("/")

		# ...
		# finde den tiefsten Ordner, der in der Datenbank existiert
		# starte mit dem ersten Ordner, der ja Parent=0 hat
		# fahre fort mit dem nächsten, der als Parent den ersten hat
		# usw...
		# bis keine Übereinstimmung mehr gefunden wird
		# bist du noch nicht am Ende der Ordnerkette, erstelle die fehlenden Glieder
		Parent = 0
		CurrentPath = ""
		for i in range(0, len(Path)):
			CurrentPath = CurrentPath+"/"+Path[i]
			try:				# finde den Ordner nach Namen und Parent
				self.QueryResult = Folders.objects.using( FileBaseDB ).get( parent=Parent, name=Path[i] )
				self.DEBUG += CurrentPath+": #"+str( self.QueryResult.id )+"\n"
			except:				# nicht gefunden
				self.DEBUG += "Folder unknown: "+Path[i]+"\n"
				if AddMissing:
					LastSync = datetime.now()
					if os.path.exists( CurrentPath ):
						Created = os.path.getmtime( CurrentPath )
					else:
						Created = LastSync
					self.QueryResult = Folders.objects.using( FileBaseDB ).create( parent=Parent, name=Path[i], created=Created, lastsync=LastSync )
					self.DEBUG += "Created: #"+str( self.QueryResult.id )+"\n"
				else:
					return False
					break
			Parent = self.QueryResult.id
		return True


	def getPath():									# in welchem Verzeichnis befindet sich die Datei laut Datenbank
		if self.ID is None:
			return None
		if self.Path is not None:
			return self.Path
		self.Path = "/"+self.Name
		folder = self.Parent
		while folder != 0:
			try:
				F = Folders.objects.using( FileBaseDB ).get( id=folder )
				self.Path = "/" + F.name + self.Path
				folder = F.parent
			except:
				folder = 0
		self.DEBUG += "Path is "+self.Path+"\n"
		return self.Path


	def checkPresence():
		if self.ID is None:
			return None
		if self.Exists is not None:
			return self.Exists
		self.getPath()
		self.Exists = os.path.exists( self.Path )
		if self.Exists:
			self.DEBUG += "Folder is present at the specified location.\n"
		else:
			self.DEBUG += "Folder was not found at the specified location.\n"
		return self.Exists


class File:

	def __init__(self, ID=None, Path=None):
		self.DEBUG = ""
		self.ID = None
		if ID is not None:
			self.LoadID( ID )
		if Path is not None:
			self.LoadPath( Path )


	def LoadID( ID ):									# object aus einem Datenbankeintrag laden
		self.DEBUG += "Loading database file #"+str(ID)+" ...\n"
		try:
			self.QueryResult = Files.objects.using( FileBaseDB ).get( id=ID )
		except:
			self.DEBUG += "Error: File not found\n"
			return False
		self.ID		= self.QueryResult.id
		self.Folder	= self.QueryResult.folder
		self.Path	= None
		self.FullPath	= None
		self.Exists	= None
		self.FileName	= self.QueryResult.filename
		self.FileSize	= self.QueryResult.filesize
		self.MD5	= self.QueryResult.md5
		self.Integrity	= None
		self.DEBUG += "Found "+self.FileName+", "+str(self.FileSize)+" bytes\n"
		return True


	def LoadPath( Path ):
		self.DEBUG += "Loading file "+Path+" ...\n"
		return False


	def Reload():
		return self.LoadID( self.ID )


	def getPath():									# in welchem Verzeichnis befindet sich die Datei laut Datenbank
		if self.ID is None:
			return None
		if self.Path is not None:
			return self.Path
		self.Path = ""
		folder = self.Folder
		while folder != 0:
			try:
				F = Folders.objects.using( FileBaseDB ).get( id=folder )
				self.Path = "/" + F.name + self.Path
				folder = F.parent
			except:
				folder = 0
		self.DEBUG += "Path is "+self.Path+"\n"
		return self.Path


	def getFullPath():								# voller Pfad inkl. Dateiname
		if self.ID is None:
			return None
		if self.FullPath is not None:
			return self.FullPath
		self.getPath( ID )
		self.FullPath = os.path.join( self.Path, self.FileName )
		self.DEBUG += "Full path to file is "+self.FullPath+"\n"
		return self.FullPath


	def Move( newpath ):								# verschiebe die Datei in ein anderes Verzeichnis
		if self.ID is None:
			return None
		self.getFullPath()
		self.DEBUG += "Moving file from "+ self.FullPath +" to "+ newpath +" ...\n"
		folder = Folder( Path=newpath, AddMissing=True )
		self.DEBUG += folder.DEBUG
		self.Folder			= folder.id
		self.QueryResult.folder		= folder.id
		self.QueryResult.LastSync	= datetime.now()
		self.QueryResult.SyncResult	= "moved"
		self.QueryResult.save()


	def Compare( path ):							# vergleiche die Datei mit einer anderen, True wenn identisch
		if self.ID is None:
			return None
		self.DEBUG += "Comparing file to "+path+" ...\n"
		fsize = os.path.getsize( path )
		if fsize == self.FileSize:
			self.DEBUG += "File size is equal.\n"
			if self.MD5 is not None:
				md5 = largefileMD5( path )
				if md5 == self.MD5:
					self.DEBUG += "MD5 matches.\n"
					identical = True
				else:
					self.DEBUG += "MD5 mismatch: "+md5+", database file has "+self.MD5+".\n"
					identical = False
			else:
				self.DEBUG += "No MD5 stored. Assuming files are equal.\n"
				identical = True
		else:
			self.DEBUG += "Size mismatch: " +str( fsize )+" bytes, database file has "+str( self.FileSize )+" bytes.\n"
			identical = False
		return identical


	def RecoverMissing():								# versuche die Datei wiederzufinden und den neuen Pfad zu speichern
		success	= False
		top	= "/home"
		maxtime	= 60
		start	= time.time()
		ending	= "completed unsuccessfully"
		self.DEBUG += "Searching folder "+top+" ...\n"
		for root, dirs, files in os.walk( top ):
			if self.FileName in files:
				path = os.path.join( root, self.FileName )
				self.DEBUG += "Hit: "+path+"\n"
				if self.Compare( path ):
					self.Move( path )
					success = True
					ending = "succeeded"
					break
			if time.time() - start > maxtime:
				ending = "interrupted"
				break
		self.DEBUG += "Search "+ending+" after "+str( time.time()-start )+" seconds.\n"
		return success


	def checkPresence( Recover=True ):							# prüfe, ob die Datei vorhanden ist
		if self.ID is None:
			return None
		if self.Exists is not None:
			return self.Exists
		self.getFullPath()
		self.Exists = os.path.exists( self.FullPath )
		if self.Exists:
			self.DEBUG += "File is present at the specified location.\n"
		else:
			self.DEBUG += "File was not found at the specified location.\n"
			self.QueryResult.LastSync	= datetime.now()
			self.QueryResult.SyncResult	= "deleted"
			self.QueryResult.save()
			if Recover:
				self.RecoverMissing()
		return self.Exists


	def checkIntegrity():									# prüfe, ob die Datei unverändert ist
		if self.ID is None:
			return None
		if self.Integrity is not None:
			return self.Integrity
		self.checkPresence( Recover=False )	# prüft nur ob Datei vorhanden, sucht sie nicht
		if not self.Exists:
			return False
		self.Integrity = self.Compare( self.FullPath )
		self.QueryResult.LastSync = datetime.now()
		if self.Integrity:
			self.DEBUG += "File integrity confirmed.\n"
			self.QueryResult.SyncResult = "unmodified"
		else:
			self.DEBUG += "File was modified.\n"
			self.QueryResult.SyncResult = "modified"
		self.QueryResult.save()
		return self.Integrity



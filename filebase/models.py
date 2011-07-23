# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Files(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    folder = models.IntegerField(db_column='Folder') # Field name made lowercase.
    filename = models.CharField(max_length=1500, db_column='FileName') # Field name made lowercase.
    created = models.DateTimeField(db_column='Created') # Field name made lowercase.
    lastmodification = models.DateTimeField(db_column='LastModification') # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize') # Field name made lowercase.
    md5 = models.CharField(max_length=96, db_column='MD5', blank=True) # Field name made lowercase.
    filetype = models.CharField(max_length=1500, db_column='FileType', blank=True) # Field name made lowercase.
    thumbnail = models.TextField(db_column='Thumbnail', blank=True) # Field name made lowercase.
    lastsync = models.DateTimeField(db_column='LastSync') # Field name made lowercase.
    syncresult = models.CharField(max_length=30, db_column='SyncResult') # Field name made lowercase.
    class Meta:
        db_table = u'Files'

class Folders(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    parent = models.IntegerField(db_column='Parent') # Field name made lowercase.
    name = models.CharField(max_length=1500, db_column='Name') # Field name made lowercase.
    created = models.DateTimeField(db_column='Created') # Field name made lowercase.
    lastsync = models.DateTimeField(db_column='LastSync') # Field name made lowercase.
    class Meta:
        db_table = u'Folders'


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Exes(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    file = models.IntegerField(db_column='File') # Field name made lowercase.
    icon = models.TextField(db_column='Icon') # Field name made lowercase.
    class Meta:
        db_table = u'EXEs'

class Files(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    folder = models.IntegerField(null=True, db_column='Folder', blank=True) # Field name made lowercase.
    filename = models.CharField(max_length=1500, db_column='Filename') # Field name made lowercase.
    created = models.DateTimeField(null=True, db_column='Created', blank=True) # Field name made lowercase.
    modified = models.DateTimeField(null=True, db_column='Modified', blank=True) # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='Filesize') # Field name made lowercase.
    md5 = models.CharField(max_length=96, db_column='MD5', blank=True) # Field name made lowercase.
    filetype = models.CharField(max_length=1500, db_column='Filetype', blank=True) # Field name made lowercase.
    mime = models.CharField(max_length=300, db_column='MIME', blank=True) # Field name made lowercase.
    thumbnail = models.TextField(db_column='Thumbnail', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Files'

class Folders(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    parent = models.IntegerField(db_column='Parent') # Field name made lowercase.
    name = models.CharField(max_length=1500, db_column='Name') # Field name made lowercase.
    created = models.DateTimeField(db_column='Created') # Field name made lowercase.
    class Meta:
        db_table = u'Folders'

class Jpegs(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    file = models.IntegerField(db_column='File') # Field name made lowercase.
    exif = models.TextField(db_column='EXIF', blank=True) # Field name made lowercase.
    thumbnail = models.TextField(db_column='Thumbnail', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'JPEGs'


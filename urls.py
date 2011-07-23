from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	(r'^filebase/$',				'Django.filebase.main.index'),
	(r'^filebase/filesystem$',			'Django.filebase.main.filesystem'),
	(r'^filebase/database$',			'Django.filebase.main.database'),
	(r'^filebase/details$',				'Django.filebase.main.details'),
	(r'^filebase/Passwords/$',			'Django.filebase.passwords.index'),
	(r'^filebase/Passwords/results$',		'Django.filebase.passwords.results'),
#	(r'^filebase/recurser$',			"Django.filebase.views.recurser"),
#	(r'^filebase/jumper$',				"Django.filebase.views.jumper"),
)


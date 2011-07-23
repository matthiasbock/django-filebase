# -*- coding: iso-8859-15 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from Django.globals import *
from Django.FileBase.models import *

from FileBase import *


def index( request ):
	params = {}
	params["passwords"] = Passwords.objects.using( FileBaseDB ).all()
	return render_to_response("passwordlist.html", params)


def results( request ):
	params = {}
	return render_to_response("passwordresults.html", params)



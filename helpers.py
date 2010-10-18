from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from decimal import *
from math import floor
from django.template import RequestContext
import logging, traceback
#import simplejson
#from django.contrib import auth
from django.http import HttpRequest
#from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core import serializers
from django.views.defaults import server_error
import re
from operator import itemgetter, attrgetter

def sort_by_values(items, reverse=True):

	items = items.items()
	
	items.sort(key = itemgetter(1), reverse=reverse)

	return items
	
def strip_commas(item):
	regex = re.compile("[\,]")
	replace = ""
	return regex.sub(replace, item)

def strip_unicode(string):
  import unicodedata
  return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore')
		
def is_ajax_request(request):
	
	if request.META:
		if 'HTTP_X_REQUESTED_WITH' in request.META:
			if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
				return True
	
	return False

def flash_error(request, msg):
	flash(request, msg, msg_type='error')

def flash_success(request, msg):
	flash(request, msg, msg_type='success')
			
def flash(request, msg, msg_type='success'):
	logging.debug("in flash")
	if request.user:
		if msg_type == 'error':
			request.session['error'] = msg
		elif msg_type == 'notice':
			request.session['notice'] = msg
		else:
			if request.user.is_authenticated():
				request.user.message_set.create(message=msg)
			else:
				request.session['success'] = msg
			
def param(request, name, default=''):
    """Shortcut for getting a parameter value"""
    return request.REQUEST.get(name, default).strip()

def generic_error(request, msg=None):
	#print("A generic error has occurred")
	if not msg:
		msg = "An error has occurred"
	#raise Http404, msg
	logging.error("ERROR: %s" % msg)
	return render(
		'includes/error.html', 
		request, 
		locals()
	)
		
def map_select(objects, name="name", type="list"):
	if type == 'list':
		obj_list = list([(i.id, getattr(i, name)) for i in objects])
		obj_list.insert(0, ("", "Please choose..."))
		return obj_list
	else:
		string = " ".join(["<option value='%s'>%s</option>" % (i.id, getattr(i, name)) for i in objects])
		return "<option value=''>Please choose...</option>"+string
	
def jsonify(dictionary):
	response = None
	mimetype = 'text/javascript'
	data = None
	try:
		data = simplejson.dumps(dictionary, sort_keys=True)
		#response = HttpResponse(simplejson.dumps(dictionary, sort_keys=True), mimetype=mimetype)
	except Exception, (e):
		#PathException("Couldn't JSONify data, trying serializer", e)
		try:
			data = serializers.serialize("json", dictionary)
			#response = HttpResponse(serializers.serialize("json", dictionary), mimetype=mimetype)
		except Exception, (e):
			print("Couldn't serialize data, either", e)
			
	return HttpResponse(data, mimetype=mimetype)
	
def render(url, request, opts={}):
	opts['error'] = None
	#if 'error' in request.session:
	#	opts['error'] = request.session['error']
	#	request.session['error'] = None
	#return render_to_response(url, request)
		
	return render_to_response(url, context_instance=RequestContext(request, opts))

def redirect(url):
	return HttpResponseRedirect(url)
	
def fail(request, template_name):
	return server_error(request, template_name)
	
def paginate(obj_list, this_page, url, per_page=5):
	p = Pagination(obj_list, this_page, url, per_page)
	paginate = p.paginate()
	return paginate	
	
def unique(thelist):
	uniquedict = {}
	for i in thelist:
		uniquedict[i] = 0
	return uniquedict.keys()

def underscore(value):
    return value.replace(' ','_')

def ununderscore(value):
    return value.replace('_',' ')

def get_quiz_by_name(name):
	return get_object_or_404(Quiz, name__iexact=name)
	
def go_back(request):
	REDIRECT_TO = ""
	if 'HTTP_REFERER' in request.META:
		REDIRECT_TO = request.META['HTTP_REFERER']
	else:
		REDIRECT_TO = settings.LOGIN_REDIRECT_URL
		
	return redirect(REDIRECT_TO)
	


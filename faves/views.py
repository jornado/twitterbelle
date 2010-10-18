from helpers import *
from lib.userparser import UserParser
from lib.faveparser import FaveParser
from django.http import HttpResponse
from google.appengine.api import memcache
import logging
from datetime import datetime
from urllib2 import HTTPError
from faves.models import *

def index(request):

	views = View.all()
	views.order("-view_count")
	views = views.fetch(10)
	
	return render(
		'faves/index.html', 
		request, 
		locals()
	)
	
def about(request):

	return render(
		'faves/about.html', 
		request, 
		locals()
	)
	
def contact(request):

	return render(
		'faves/contact.html', 
		request, 
		locals()
	)
	
def process(request, screen_name='poeks', start_page=10):
	
	number_of_faves = int(start_page) * 20
	try:
		p = UserParser(screen_name)
	except Exception, e:
		logging.error("UserParser error: %s" % e.msg)
		return generic_error(request, "Something broke in UserParser!")
		
	try:
		twit = p.get_user()
	except HTTPError, e:
		logging.error("HTTPError: %s" % e.msg)
		return generic_error(request, e.msg)
	except Exception, e:
		logging.error("Other error: %s" % e.msg)
		return generic_error(request, "Something broke in p.get_user!")
		
	faves_ajax_cache, stats, cache_name = get_cached(screen_name, start_page)
	if stats:
		cache_age = 1
	
	return render(
		'faves/process.html', 
		request, 
		locals()
	)

def faves_ajax(request, screen_name='poeks', start_page=10):

	faves_ajax_cache, stats, cache_name = get_cached(screen_name, start_page)

	if faves_ajax_cache is not None:

		logging.debug("Successfully Returning Memcache")
		

	else:
	
	
		p = FaveParser(screen_name, int(start_page))
		faves = p.process_faves()

		response_data = p.htmlify(faves)

		faves_ajax_cache = response_data
		add_to_cache(cache_name, faves_ajax_cache)

	return HttpResponse(faves_ajax_cache)


def user_not_found(request, screen_name):
	logging.error("user_not_found. %s" % screen_name)
	return render(
		'includes/user_not_found.html', 
		request, 
		locals()
	)
	
def get_cached(screen_name, start_page):
	
	# stats: {'hits': 13, 'items': 3, 'bytes': 85877, 'oldest_item_age': 16615.014935970306, 'misses': 30, 'byte_hits': 370870} 
	
	cache_name = _get_cache_name(screen_name, start_page)
	logging.debug("Will try to fetch %s Memcache..." % cache_name)
	faves_ajax_cache = memcache.get(cache_name)
	stats = memcache.get_stats()
	
	if faves_ajax_cache is not None:
		return faves_ajax_cache, stats, cache_name
	else:
		return None, None, cache_name
	
def _get_cache_name(screen_name, start_page):
	return "faves_ajax_%s_%d" % (screen_name, start_page)
	
def add_to_cache(cache_name, cache_data):
	duration = 60*60*24*7 # a week
	now = datetime.today()
	
	cache_data = "<script>window.cache_age = '%s'</script>%s" % (now, cache_data)
	
	if not memcache.add(cache_name, cache_data, duration):
		logging.error("Memcache set failed.")
		return True
	else:
		logging.debug("Memcache set successful.")
		return None

def delete_from_cache(request, screen_name):
	
	cache_name = _get_cache_name(screen_name, 10)
	memcache.delete(cache_name)
	cache_name = _get_cache_name(screen_name, 25)
	memcache.delete(cache_name)
	cache_name = _get_cache_name(screen_name, 50)
	memcache.delete(cache_name)
	cache_name = _get_cache_name(screen_name, 100)
	memcache.delete(cache_name)
	
	return process(request, screen_name)
	
# DISPATCHERS

def faves_ajax_small(request, screen_name):
	return faves_ajax(request, screen_name, 10)

def faves_ajax_medium(request, screen_name):
	return faves_ajax(request, screen_name, 25)

def faves_ajax_large(request, screen_name):
	return faves_ajax(request, screen_name, 50)

def faves_ajax_xlarge(request, screen_name):
	return faves_ajax(request, screen_name, 100)
						
def small(request, screen_name):
	return process(request, screen_name, 10)
	
def medium(request, screen_name):
	return process(request, screen_name, 25)
		
def large(request, screen_name):
	return process(request, screen_name, 50)
	
def xlarge(request, screen_name):
	return process(request, screen_name, 100)	
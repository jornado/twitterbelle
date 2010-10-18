from lib.BeautifulSoup import BeautifulSoup
import urllib2
from django.conf import settings
import re
from lib.exception import PoeksException
from lib.BeautifulSoup import BeautifulSoup
import urllib2

class Parser:

	def __init__(self):
		pass
		
	def open_url(self, page):

		try:
			this_url = "%s%s" % (self.url, page)
			return urllib2.urlopen(this_url)
		except:
			raise Exception
			
	def get_element(self, search_string, search_type='id', search_contents='string', search_method='method'):
		
		try:
			el = self.soup.findAll(**{search_type:search_string})
		except:
			raise Exception
			
		retval = ""
		try:
			
			if search_method == 'dict':
				retval = el[0][search_contents]
			else:
				retval = getattr(el[0], search_contents)
			
		except Exception, e:
			#PoeksException(e, "Couldn't do that thing with el %s" % el)
			#print "get_element: Couldn't do that thing with el %s search_string %s" % (el, search_string)
			pass
			
		return retval
		
	def get_elements(self, search_string, search_type='id', search_contents='string', search_method='method'):

		els = self.soup.findAll(**{search_type:search_string})
		
		elements = []
		for el in els:
			
			retval = ""
			try:

				if search_method == 'dict':
					retval = el[search_contents]
					#print "dict: "+retval
				else:
					retval = getattr(el, search_contents)
					#print "method: "+retval
			except Exception, e:
				#PoeksException(e, "Couldn't do that thing with el %s" % el)
				#print "Oops"
				pass
		
			elements.append(retval)

		return elements


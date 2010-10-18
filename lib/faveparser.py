from lib.BeautifulSoup import BeautifulSoup
from lib.userparser import UserParser
import urllib2
from django.conf import settings
import re
from faves.models import *
from helpers import *
from operator import itemgetter, attrgetter
from django.template.loader import render_to_string
from datetime import datetime 
from lib.belle import Belle
from lib.bitly import Api as Bitly

class FaveParser(UserParser):

	def __init__(self, screen_name, pages=2):
		UserParser.__init__(self, screen_name)
		
		self.max_chars = 140
		self.screen_name = screen_name
		self.belle = Belle()
		self.url = "%s/%s/%s" % (settings.TWITTER['base']+self.screen_name, settings.TWITTER['faves'], settings.TWITTER['page'])
		self.page = 1
		self.max_fave_page = pages
		self.per_page = 20
		self.favorites = []
		self.faves = {}
		self.images = {}
		self.total_faves = 0
		self.last_fave = ""
		
	def process_faves(self):
		faves = self.get_page(self.page)
		#print faves
		return faves
			
	def get_page(self, page=1):
		
		#print "page: %d" % page
		
		self.page=page
		faves = self.belle.GetFavorites(self.screen_name, self.page)
		
		for fave in faves:
			
			self.total_faves += 1
			self.last_fave = fave.created_at
			
			if not fave.user.screen_name in self.faves:
				self.faves[fave.user.screen_name] = 1
				self.images[fave.user.screen_name] = fave.user.profile_image_url
				self.total_faves += 1
			else:
				self.faves[fave.user.screen_name] += 1
				self.total_faves += 1

			
		if page < (self.max_fave_page):
			return self.get_page(page+1)
			
		return self.faves

		
	def printify(self, faves):
		import pprint
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(faves)
		
	def jsify(self, faves):
		template = "faves/_fave_js.html"
		html = ""
		html += self.format(faves, template)
		return html
		#return "1,3,2"
		
	def htmlify(self, faves):
		template = "faves/_fave.html"
		now = datetime.today()
		now_format = now.strftime("%H:%M %p %B %d %z")
		html = "<script>"
		html += "window.total_faves = %d; window.last_fave = '%s and %s UTC';" % (self.total_faves, self.last_fave, now_format)
		html += "window.tweet_this_link = '<a href=\"http://twitter.com?status=%s\" target=\"_blank\">&#x266B; Tweet This &#x266B;</a>';" % self.get_tweet_this()
		html += "</script>"
		html += self.format(faves, template)
		return html
		
	def get_tweet_this(self):
		
		url = self.get_bitly_link()
		url_len = len(url)
		head = "Twitterbelle faves: "
		remaining_chars = self.max_chars - url_len - len(head)
		ten_faves = self.sort_faves()[:10]
		fave_string = ""
		for fave in ten_faves:
			if len(fave_string)+len(fave[0])<remaining_chars:
				fave_string += "@%s " % fave[0]

		html = "%s%s%s" % (head, fave_string, url)
		
		return html
		
		
	def get_bitly_link(self):
		try:
			bit_ly = Bitly(settings.BITLY['login'], settings.BITLY['api_key'])
			site = settings.APP_URL
			self.shortened_url = bit_ly.shorten("%s/%s/" % (site, self.screen_name))
			return self.shortened_url
		except Exception, e:
			return None
		
	def sort_faves(self):
		items = self.faves.items()
		items.sort(key = itemgetter(1), reverse=True)
		items = items[:50]
		
		return items
		
	def format(self, faves, template):
		
		items = self.sort_faves()
		
		html =""
		this_fave = 1
		
		for fave in items:
			username = fave[0]
			count = fave[1]
			if this_fave % 2 == 0:
				even_odd = 'even'
			else:
				even_odd = 'odd'
				
			template_dict = {
				'screen_name': username,
				'count': count,
				'this_fave': this_fave,
				'image': self.images[username],
				'even_odd': even_odd,
			}
			html += render_to_string(template, template_dict)
		
			this_fave += 1
			
		return html
		
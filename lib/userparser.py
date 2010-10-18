from lib.BeautifulSoup import BeautifulSoup
from lib.parser import Parser
import urllib2
from django.conf import settings
import re
#from lib.models import *
from helpers import *
from lib.belle import Belle
from faves.models import *

class UserParser(Parser):

	def __init__(self, screen_name):
		Parser.__init__(self)
		
		self.screen_name = screen_name
		self.belle = Belle()
		
	def get_user(self):
	
		t = Twit()
		t.get_or_create(screen_name=self.screen_name)
		
		v = View()
		v.update_or_create(screen_name=self.screen_name)
		
		return self.belle.GetUser(self.screen_name)

		
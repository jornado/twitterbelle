from lib.twitter import Api
import getopt
import os
import sys
from django.conf import settings
from django.utils import simplejson

class Belle(Api):
	
	def __init__(self, username=None):
		Api.__init__(self, settings.TWITTER['auth_user'], settings.TWITTER['auth_pswd'])

import datetime

class BaseObj(object):
	
	def create(self, **kwargs):
		
		for arg in kwargs:
			#print "setting %s to %s" % (arg, kwargs[arg])
			self.__setattr__(arg, kwargs[arg])
			
		return self
		
class Twit(BaseObj):
	
	def __init__(self):
		
		self.screen_name = ""
		self.id = 0
		self.image = ""
		self.followers = 0
		self.following = 0
		self.first_name = ""
		self.last_name = ""
		self.location = ""
		self.bio = ""
		self.webpage = ""
		self.tweet_count = 0
		
		BaseObj.__init__(self)
		

class Fave(BaseObj):
	
	def __init__(self):
		
		self.twit = None
		self.fave_count = 0
		self.first_fave = datetime.datetime
		
		BaseObj.__init__(self)
	
	def create(self, **kwargs):
		
		self = BaseObj.create(self)
		
		t = Twit()
		self.twit = t.create(**kwargs)

		return self
		
	def first_fave(self):
		
		if self.first_fave:
			return self.first_fave
		else:
			return datetime.datetime
			
			
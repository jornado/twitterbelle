from google.appengine.ext import db
from appengine_django.models import BaseModel
import logging

class BelleBase(db.Model):
		
	def print_all(self):
		results = self.all()
		
		for obj in results:
			print obj
			
	def delete_all(self):
		results = self.all()
		db.delete(results)
		
	def model_class(self):
		return self.__class__

	def get_or_create(self, query, **kwargs):

		existing_obj = query.fetch(1)

		if existing_obj:
			logging.debug("Returning existing %s" % (self.model_class()))
			return existing_obj[0]

		return self.create_new(**kwargs)
		
	def create_new(self, **kwargs):
		logging.debug("Creating new %s" % (self.model_class()))
		obj = self.__class__(**kwargs)
		obj.put()
		return obj
		
class Twit(BelleBase):
	screen_name = db.StringProperty()
	
	created_on = db.DateTimeProperty(auto_now_add=True)
	updated_on = db.DateTimeProperty(auto_now_add=True)
	
	def get_or_create(self, **kwargs):
		kwargs['screen_name'] = kwargs['screen_name'].lower()
		query = self.gql("WHERE screen_name = :screen_name",
			screen_name=kwargs['screen_name'])

		return BelleBase.get_or_create(self, query, **kwargs)
		
class View(BelleBase):
	screen_name = db.StringProperty()
	view_count = db.IntegerProperty()
	
	created_on = db.DateTimeProperty(auto_now_add=True)
	updated_on = db.DateTimeProperty(auto_now_add=True)
		
	def update_or_create(self, **kwargs):
		kwargs['screen_name'] = kwargs['screen_name'].lower()
		query = self.gql("WHERE screen_name = :screen_name",
			screen_name=kwargs['screen_name'])

		existing_obj = query.fetch(1)

		if existing_obj:
			logging.debug("Returning existing %s" % (self.model_class()))
			existing_obj[0].view_count = int(existing_obj[0].view_count) + 1
			existing_obj[0].put()
			return existing_obj[0]

		kwargs['view_count']=1
		return self.create_new(**kwargs)
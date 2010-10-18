import os

from django.conf.urls.defaults import *

urlpatterns = patterns('faves.views',
	url(r'^$', 
		view= 'index', 
		name='faves_index'
	),
	url(r'^about/$', 
		view= 'about', 
		name='faves_about'
	),
	url(r'^contact/$', 
		view= 'contact', 
		name='faves_contact'
	),
	url(r'^test/$', 
		view= 'test', 
		name='faves_test'
	),
	url(r'^emoji/$', 
		view= 'emoji', 
		name='emoji'
	),
	url(r'^delete_from_cache/(?P<screen_name>\w+)/$', 
		view= 'delete_from_cache',
		name='delete_from_cache'
	),
	
	url(r'^faves/(?P<screen_name>\w+)/small/$', 
		view= 'faves_ajax_small',
		name='faves_ajax_small'
	),
	url(r'^faves/(?P<screen_name>\w+)/medium/$', 
		view= 'faves_ajax_medium',
		name='faves_ajax_medium'
	),
	url(r'^faves/(?P<screen_name>\w+)/large/$', 
		view= 'faves_ajax_large',
		name='faves_ajax_large'
	),
	url(r'^faves/(?P<screen_name>\w+)/xlarge/$', 
		view= 'faves_ajax_xlarge',
		name='faves_ajax_xlarge'
	),
	
	url(r'^(?P<screen_name>\w+)/$', 
		view= 'process', 
		name='faves_process_small'
	),
	url(r'^(?P<screen_name>\w+)/small/$', 
		view= 'small', 
		name='faves_process_small'
	),
	url(r'^(?P<screen_name>\w+)/medium/$', 
		view= 'medium', 
		name='faves_process_medium'
	),
	url(r'^(?P<screen_name>\w+)/large/$', 
		view= 'large', 
		name='faves_process_large'
	),
	url(r'^(?P<screen_name>\w+)/xlarge/$', 
		view= 'xlarge', 
		name='faves_process_xlarge'
	),
	
	#url(r'^faves/(?P<screen_name>\w+)/(?P<start_page>\d+)/$', 
	#	view= 'faves_ajax', 
	#	name='faves_ajax'
	#),
	#url(r'^(?P<screen_name>\w+)/(?P<start_page>\d+)/$', 
	#	view= 'process', 
	#	name='faves_process'
	#),

)
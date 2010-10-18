import logging
import sys
import inspect

class PoeksException(Exception):
	
	def __init__(self, msg="", err="", level="warning"):
		
		self.get_trace(inspect.trace())
		
		try:
			err_string = "%s::%s::%s faulty_code(%s) type(%s) err(%s) msg(%s)" % (
				self.lineno,
				self.filename,
				self.enclosing_func,
				self.faulty_code,
				type(err), 
				err, 
				msg
			)
		except:
			logging.warning("Couldn't format exception: %s" % msg)

		if callable(getattr(logging, str(level))):
			func = getattr(logging, level)
			func(err_string)
		else:
			logging.warning(err_string)

	def get_trace(self, trace):
		try:
			trace = trace[0]
			self.frame = trace[0]
			self.filename = trace[1]
			self.lineno = trace[2]
			self.enclosing_func = trace[3]
			self.faulty_code = trace[4]
			self.something = trace[5]
		except:
			logging.warning("Couldn't get trace for %s" % trace)

class GenericException(Exception):
	"Generic Exception base class"
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
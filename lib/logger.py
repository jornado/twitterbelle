import logging

class Logger(object):
	
	def __init__(self, log_name, log_file, log_level):
		
		# Create logger
		self.logger = logging.getLogger(log_name)
		self.logger.setLevel(log_level)
		
		# Create console handler and set level to error
		ch = logging.StreamHandler()
		ch.setLevel(logging.ERROR)
		
		# Create file handler and set level to debug
		fh = logging.FileHandler(log_file)
		fh.setLevel(log_level) 
		
		# Create formatter
		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		
		# Add formatter to ch and fh
		ch.setFormatter(formatter)
		fh.setFormatter(formatter)
		
		# Add ch and fh to logger
		self.logger.addHandler(ch)
		self.logger.addHandler(fh)
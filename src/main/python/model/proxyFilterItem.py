class ProxyFilterItem(object):
	def __init__(self, func):
		self.func = func


	def filter(self, data):
		return self.func(data)

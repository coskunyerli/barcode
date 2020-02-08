class FilePath(object):
	def __init__(self):
		self._data = {}


	def setPath(self, key, value):
		self._data[key] = value


	def path(self, key, default = None):
		return self._data.get(key, default)


	def json(self):
		return self._data.copy()


	def fromJson(self, json_):
		if json_ is not None and isinstance(json_, dict) is True:
			self._data = json_

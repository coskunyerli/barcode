import PySide2.QtCore as QtCore


class DictList(QtCore.QObject):
	def __init__(self, parent = None):
		super(DictList, self).__init__(parent)
		# dict is used for check data is in or not
		self.__dict = {}
		# keys is used for insertion order
		self.__keys = []


	def __delitem__(self, key):
		del self.__dict[key]
		self.__keys.remove(key)


	def setItem(self, key, value):
		# set item to the DictList
		# value is added to the dict, key list is for insertion order
		self.__dict[key] = value
		self.__keys.append(key)


	def index(self, key):
		# get the index of the given object
		return self.__keys.index(key)


	def insert(self, key, value, index):
		# insert the object given array with given key
		self.__dict[key] = value
		self.__keys.insert(index, key)


	def delete(self, key):
		# delete object from the structure
		if self.__dict.get(key) is not None:
			self.__keys.remove(key)
			del self.__dict[key]


	def get(self, key):
		# get the item given key
		return self.__dict.get(key)


	def pop(self, index):
		# pop the item given index
		key = self.__keys.pop(index)
		# delete item with key
		del self.__dict[key]


	def __getitem__(self, index):
		# get data with index
		if isinstance(index, int):
			key = self.__keys[index]
			return self.get(key)
		elif isinstance(index, str):
			return self.get(index)


	def __len__(self):
		return self.__keys.__len__()


	def __contains__(self, item):
		return self.__dict.get(item) is not None


	def __iter__(self):
		return iter(self.__keys)


	def keys(self):
		return self.__keys


	def __str__(self):
		return 'OrderedList(%s)' % str(self.__dict)


	def values(self):
		return self.__dict.values()

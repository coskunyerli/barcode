import copy
import json

import PySide2.QtCore as QtCore


class ObjectDict(QtCore.QObject):
	dataChanged = QtCore.Signal(str, object)
	deepDataChanged = QtCore.Signal(list, object)


	def __init__(self, *args):
		super(ObjectDict, self).__init__()
		if len(args) == 1 and isinstance(args[0], ObjectDict):
			self.__dict = dict(args[0].__dict)
		else:
			self.__dict = dict(*args)


	def __setitem__(self, key, value):
		# get the old value
		old = self.get(key)
		# change data given key
		if isinstance(value, ObjectDict):
			self.__dict[key] = value.__dict
		else:
			self.__dict[key] = value
		# emit the signal
		self.dataChanged.emit(key, old)


	def __getitem__(self, item):
		return self.__dict[item]


	def copy(self):
		t = ObjectDict()
		t.__dict = self.__dict.copy()
		return t


	def __deepcopy__(self, memodict = {}):
		t = ObjectDict()
		t.__dict = copy.deepcopy(self.__dict)
		return t


	def __copy__(self):
		return self.copy()


	def __contains__(self, item):
		return item in self.__dict


	def __iter__(self):
		return iter(self.__dict)


	def keys(self):
		return self.__dict.keys()


	def values(self):
		return self.__dict.values()


	def clear(self):
		return self.__dict.clear()


	def node(self, key):
		item = self.get(key)
		if isinstance(item, dict):
			obj = ObjectDict()
			obj.__dict = item
			item = obj

		if item is None:
			item = ObjectDict()
		return item


	def get(self, key, default = None):
		item = self.__dict.get(key)
		if isinstance(item, ObjectDict):
			item = item.__dict

		if isinstance(item, dict):
			obj = ObjectDict()
			obj.__dict = item
			item = obj

		if item is None:
			return default
		return item


	def setNode(self, key):
		if key not in self:
			self[key] = {}

		return self[key]


	def pop(self, k):
		return self.__dict.pop(k)


	def popItem(self):
		return self.__dict.popitem()


	def update(self, __k, **kwargs):
		return self.__dict.update(__k, **kwargs)


	def fromkeys(self, seq):
		return self.__dict.fromkeys(seq)


	def setdefault(self, k, default):
		return self.__dict.setdefault(k, default)


	def isEmpty(self):
		return self.__len__() <= 0


	def __str__(self):
		return 'ObjectDict%s' % self.__dict.__str__()


	def __repr__(self):
		return self.__str__()


	def __eq__(self, other):
		return self.__dict == other.__dict


	def toJson(self):
		return json.dumps(self.__dict)


	def deepcopy(self):
		return self.__deepcopy__()


	def __len__(self):
		return len(self.__dict)


	@classmethod
	def dictToObjectDict(cls, dict_):
		objectDict = ObjectDict()
		for key in dict_:
			if isinstance(dict_[key], dict):
				objectDict[key] = cls.dictToObjectDict(dict_[key])
			else:
				objectDict[key] = dict_[key]

		return objectDict




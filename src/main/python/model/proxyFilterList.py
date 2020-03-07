class ProxyFilterList(object):
	def __init__(self):
		self.__filterList = {}


	def addFilter(self, name, filterItem):
		self.__filterList[name] = filterItem


	def deleteFilter(self, name):
		if name in self.__filterList:
			del self.__filterList[name]


	def filter(self, data):
		for name in self.__filterList:
			filterItem = self.__filterList[name]
			if filterItem.filter(data) is False:
				return False
		return True

import PySide2.QtCore as QtCore
from model.proxyFilterList import ProxyFilterList


class SearchProductModelProxy(QtCore.QSortFilterProxyModel):
	def __init__(self, parent = None):
		super(SearchProductModelProxy, self).__init__(parent)
		self.proxyFilter = ProxyFilterList()


	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow, 1, sourceParent)
		# barcodeIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
		product = index.data(QtCore.Qt.UserRole)
		return self.proxyFilter.filter(product)


	def addFilter(self, name, filterItem):
		self.beginResetModel()
		self.proxyFilter.addFilter(name, filterItem)
		self.endResetModel()


	def deleteFilter(self, name):
		self.beginResetModel()
		self.proxyFilter.deleteFilter(name)
		self.endResetModel()

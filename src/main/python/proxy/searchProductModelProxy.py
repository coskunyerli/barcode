import PySide2.QtCore as QtCore


class SearchProductModelProxy(QtCore.QSortFilterProxyModel):
	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow, 1, sourceParent)
		text = index.data()
		return self.filterRegExp().pattern().lower() in text.lower()

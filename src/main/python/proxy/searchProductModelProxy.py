import PySide2.QtCore as QtCore


class SearchProductModelProxy(QtCore.QSortFilterProxyModel):
	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow, 1, sourceParent)
		#barcodeIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
		text = index.data()
		#barcode = barcodeIndex.data()
		return (self.filterRegExp().pattern().lower() in text.lower())
	#barcode.startswith(self.filterRegExp().pattern().lower())

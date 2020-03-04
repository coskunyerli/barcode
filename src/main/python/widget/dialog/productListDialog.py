import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
import log
from model.sizeInfo import SizeInfo

from proxy.searchProductModelProxy import SearchProductModelProxy
from service.databaseService import DatabaseService
from widget.dialogNameWidget import DialogNameWidget
from widget.toast import Toast

from fontSize import FontSize

sizeInfo = SizeInfo(None, None)


class ProductListDialog(QtWidgets.QDialog, DatabaseService):

	@classmethod
	def setSizeInfo(cls, sizeInfo2):
		global sizeInfo
		sizeInfo = sizeInfo2


	@classmethod
	def sizeInfo(cls):
		return sizeInfo


	def __init__(self, model, parent = None):
		super(ProductListDialog, self).__init__(parent)
		self.resize(1000, 600)
		self.setModal(True)
		self.setWindowTitle('Products')
		# prent of SearchProductModelProxy should be main parent
		self.proxyModel = SearchProductModelProxy(parent)
		self.proxyModel.setSourceModel(model)

		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.mainLayout.setContentsMargins(8, 8, 8, 8)

		self.dialogNameLabel = DialogNameWidget(self)
		self.dialogNameLabel.setText('Product List')
		self.dialogNameLabel.setPointSize(FontSize.dialogNameLabelFontSize())
		self.dialogNameLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.productTableView = QtWidgets.QTableView(self)
		self.productTableView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
		self.productTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.productTableView.setModel(self.proxyModel)
		self.productTableView.customContextMenuRequested.connect(self.__showPopup)
		self.productTableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		self.searchWidget = QtWidgets.QWidget(self)
		self.searchWidgetLayout = QtWidgets.QHBoxLayout(self.searchWidget)
		self.searchWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.searchLineEdit = QtWidgets.QLineEdit(self.searchWidget)
		self.searchLineEdit.setObjectName('barcodeLineEdit')
		self.searchLineEdit.setPlaceholderText('Search With Name')

		self.searchWidgetLayout.addWidget(self.searchLineEdit)
		self.searchWidgetLayout.addItem(
				QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.footerWidget = QtWidgets.QWidget(self)
		self.footerWidgetLayout = QtWidgets.QHBoxLayout(self.footerWidget)
		self.footerWidgetLayout.setContentsMargins(0, 0, 0, 0)

		self.totalProductTextLabel = QtWidgets.QLabel(self.footerWidget)
		self.totalProductTextLabel.setText('Number Of Total Products')

		self.totalProductLabel = QtWidgets.QLabel(self.footerWidget)
		self.totalProductLabel.setText(str(model.rowCount()))

		self.currentProductNumberLabelText = QtWidgets.QLabel(self.footerWidget)
		self.currentProductNumberLabelText.setText('Number of Filtered Products')
		self.currentProductNumberLabel = QtWidgets.QLabel(self.footerWidget)
		self.currentProductNumberLabel.setText(str(self.proxyModel.rowCount()))

		self.footerWidgetLayout.addWidget(self.totalProductTextLabel)
		self.footerWidgetLayout.addWidget(self.totalProductLabel)

		self.footerWidgetLayout.addWidget(self.currentProductNumberLabelText)
		self.footerWidgetLayout.addWidget(self.currentProductNumberLabel)
		spacerItem = QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.footerWidgetLayout.addItem(spacerItem)

		self.mainLayout.addWidget(self.dialogNameLabel)
		self.mainLayout.addWidget(self.productTableView)
		self.mainLayout.addWidget(self.searchWidget)
		self.mainLayout.addWidget(self.footerWidget)

		self.searchLineEdit.editingFinished.connect(self.__searchTextChanged)

		self.searchLineEdit.setFocus()

		model.modelReset.connect(self.modelReset)
		model.rowsInserted.connect(self.modelReset)

		self.deleteShortCut = QtWidgets.QShortcut(self)
		self.deleteShortCut.setKey(QtGui.QKeySequence.Delete)
		self.deleteShortCut.activated.connect(self.remove)

		# update header sizes
		self.__updateSizes()


	def modelReset(self):
		self.totalProductLabel.setText(str(self.proxyModel.sourceModel().rowCount()))


	def closeEvent(self, event):
		headerView = self.productTableView.horizontalHeader()
		headerSizes = []
		for i in range(headerView.count()):
			headerSizes.append(int(headerView.sectionSize(i)))

		size = self.size()
		ProductListDialog.setSizeInfo(SizeInfo(size, headerSizes))
		super(ProductListDialog, self).closeEvent(event)


	def __searchTextChanged(self):
		self.proxyModel.setFilterRegExp(
				QtCore.QRegExp(self.searchLineEdit.text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString))

		self.currentProductNumberLabel.setText(str(self.proxyModel.rowCount()))
		self.searchLineEdit.selectAll()


	def __showPopup(self, pos):
		globalPos = self.productTableView.mapToGlobal(pos)
		indices = self.productTableView.selectedIndexes()
		if indices:
			menu = QtWidgets.QMenu(self)
			removeAction = menu.addAction('Remove')
			editAction = menu.addAction('Edit')
			action = menu.exec_(globalPos)

			if action == removeAction:
				messageBox = QtWidgets.QMessageBox.question(self, 'Delete Product', 'Are you sure?',
															QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
				if messageBox == QtWidgets.QMessageBox.Yes:
					self.__remove(indices)
			elif action == editAction:
				index = self.productTableView.currentIndex()
				self.__editProduct(index)


	def remove(self):
		# get selected indexes
		indices = self.productTableView.selectedIndexes()
		if indices:
			# if indexes exist, remove it
			messageBox = QtWidgets.QMessageBox.question(self, 'Delete Product', 'Are you sure?',
														QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
			if messageBox == QtWidgets.QMessageBox.Yes:
				self.__remove(indices)


	def __remove(self, indices):
		try:
			indices = sorted(list(filter(lambda index: index.column() == 0, indices)), key = lambda index: index.row())

			barcodeList = list(
					filter(lambda barcode: barcode, map(lambda index: index.data(), indices)))
			self.currentProductNumberLabel.setText(str(self.proxyModel.rowCount()))
			for productIndex in indices:
				product = productIndex.data(QtCore.Qt.UserRole)
				self.databaseService().delete(product)
			if self.databaseService().commit() is True:
				self.proxyModel.sourceModel().removeProductWithBarcode(barcodeList)
		except Exception as e:
			log.error(f'Product barcode list {indices} is not deleted in product model. Exception is {e}')
			Toast.error('Product Deleting Error', 'Product is not deleted successfully')


	def __editProduct(self, index):
		product = index.data(QtCore.Qt.UserRole)
		self.parent().showAddProductProduct(product)


	def __updateSizes(self):
		if ProductListDialog.sizeInfo() is not None and ProductListDialog.sizeInfo().isValid():
			self.resize(ProductListDialog.sizeInfo().size)
			headerView = self.productTableView.horizontalHeader()
			for i in range(len(ProductListDialog.sizeInfo().headerSizes)):
				headerView.resizeSection(i, int(ProductListDialog.sizeInfo().headerSizes[i]))

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
import log

from proxy.searchProductModelProxy import SearchProductModelProxy
from widget.dialogNameWidget import DialogNameWidget
from widget.toast import Toast

from fontSize import FontSize


class ProductListDialog(QtWidgets.QDialog):
	def __init__(self, model, parent = None):
		super(ProductListDialog, self).__init__(parent)
		self.resize(1000, 600)
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


	def modelReset(self):
		self.totalProductLabel.setText(str(self.proxyModel.sourceModel().rowCount()))


	def __searchTextChanged(self):
		self.proxyModel.setFilterRegExp(
				QtCore.QRegExp(self.searchLineEdit.text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString))

		self.currentProductNumberLabel.setText(str(self.proxyModel.rowCount()))
		self.searchLineEdit.selectAll()


	def __showPopup(self, pos):
		globalPos = self.productTableView.mapToGlobal(pos)
		index = self.productTableView.indexAt(pos)
		if index.isValid():
			menu = QtWidgets.QMenu(self)
			removeAction = menu.addAction('Remove')
			editAction = menu.addAction('Edit')
			action = menu.exec_(globalPos)

			if action == removeAction:
				messageBox = QtWidgets.QMessageBox.question(self, 'Delete Product', 'Are you sure?',
															QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
				if messageBox == QtWidgets.QMessageBox.Yes:
					self.__remove(index)
			elif action == editAction:
				self.__editProduct(index)


	def __remove(self, index):
		try:
			self.proxyModel.sourceModel().removeProduct(self.proxyModel.mapToSource(index))
			self.currentProductNumberLabel.setText(str(self.proxyModel.rowCount()))
		except Exception as e:
			log.error(f'Product {index} is not deleted in product model. Exception is {e}')
			Toast.error('Product Deleting Error', 'Product is not deleted successfully')


	def __editProduct(self, index):
		product = index.data(QtCore.Qt.UserRole)
		self.parent().addProductProduct(product)

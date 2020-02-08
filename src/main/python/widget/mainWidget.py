import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import core

from enums import BarcodeType, ProductType
from event.eventFilterObject import EventFilterForTableView
from model.dailyReceiptModel import DailyReceiptModel
from model.product import CustomProduct
from model.productModel import ProductModel
from model.soldProduct import SoldProduct, WeighableSoldProduct
from model.soldProductModel import SoldProductModel

from widget.breadCrumb import BreadCrumb, ModelBreadCrumbData
from widget.dialog.oldReceiptDialog import OldReceiptDialog
from widget.dialog.priceDialog import PriceDialog
from widget.dialog.productAddDialog import ProductAddDialog
from widget.dialog.productListDialog import ProductListDialog
from widget.footerWidget import FooterWidget
from widget.inputWidgetGroup import InputWidgetGroup
from widget.pushButton import PushButton
from widget.toast import Toast


class MainWidget(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(MainWidget, self).__init__(parent)
		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.setSpacing(0)
		self.topWidget = QtWidgets.QFrame(self)
		self.topWidget.setObjectName('topWidget')
		self.topWidgetLayout = QtWidgets.QHBoxLayout(self.topWidget)
		self.topWidgetLayout.setContentsMargins(0, 0, 4, 0)
		self.topWidgetLayout.setSpacing(1)
		self.scrollArea = QtWidgets.QScrollArea(self.topWidget)
		self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
		self.breadCrumbWidget = BreadCrumb(self)

		self.breadCrumbWidget.setItemCLass(ModelBreadCrumbData)
		self.breadCrumbWidget.setDefaultName('Receipt')

		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(self.breadCrumbWidget)

		self.priceButtonDialog = PushButton(self.topWidget)
		self.priceButtonDialog.setText('Product Price')
		self.priceButtonDialog.setFixedSize(QtCore.QSize(100, 80))

		self.productDialogButton = PushButton(self.topWidget)
		self.productDialogButton.setText('Product')
		self.productDialogButton.setFixedSize(QtCore.QSize(80, 80))

		self.incomeButton = PushButton(self.topLevelWidget())
		self.incomeButton.setText('Income')
		self.incomeButton.setFixedSize(QtCore.QSize(80, 80))

		self.exitButton = PushButton(self.topLevelWidget())
		self.exitButton.setText('Exit')
		self.exitButton.setFixedSize(QtCore.QSize(80, 80))

		self.topWidgetLayout.addWidget(self.scrollArea)
		spacerItem = QtWidgets.QSpacerItem(8, 8, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.topWidgetLayout.addItem(spacerItem)
		self.topWidgetLayout.addWidget(self.priceButtonDialog)
		self.topWidgetLayout.addWidget(self.productDialogButton)
		self.topWidgetLayout.addWidget(self.incomeButton)
		self.topWidgetLayout.addWidget(self.exitButton)

		self.centralWidget = QtWidgets.QWidget(self)
		self.centralWidgetLayout = QtWidgets.QHBoxLayout(self.centralWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setVerticalStretch(1)
		self.centralWidget.setSizePolicy(sizePolicy)
		self.centralWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.centralWidgetLayout.setSpacing(0)

		self.soldTableView = QtWidgets.QTableView(self.centralWidget)
		self.soldTableView.customContextMenuRequested.connect(self.showPopup)
		self.soldTableView.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.soldTableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.soldTableView.verticalHeader().setDefaultSectionSize(24)

		eventFilterObject = EventFilterForTableView(self)

		self.soldTableView.installEventFilter(eventFilterObject)
		self.productWidget = QtWidgets.QWidget(self.centralWidget)

		self.inputWidgetGroup = InputWidgetGroup(self.centralWidget)

		self.centralWidgetLayout.addWidget(self.soldTableView)
		self.centralWidgetLayout.addWidget(self.productWidget)

		self.totalPriceWidget = QtWidgets.QWidget(self)
		self.totalPriceWidgetLayout = QtWidgets.QHBoxLayout(self.totalPriceWidget)
		self.totalPriceWidgetLayout.setContentsMargins(0, 8, 8, 8)
		self.totalPriceWidgetLayout.setSpacing(8)
		self.totalPriceLabel = QtWidgets.QLabel(self.totalPriceWidget)
		self.totalPriceLabel.setObjectName('totalPriceLabel')
		self.totalPriceLabel.setText('Total Price')
		self.totalPriceTextEdit = QtWidgets.QLineEdit(self.totalPriceWidget)
		self.totalPriceTextEdit.setObjectName('totalPriceTextEdit')
		self.totalPriceTextEdit.setFixedHeight(100)
		self.totalPriceTextEdit.setReadOnly(True)
		self.totalPriceTextEdit.setFocusPolicy(QtCore.Qt.NoFocus)
		self.totalPriceTextEdit.setAlignment(QtCore.Qt.AlignCenter)
		font = self.totalPriceTextEdit.font()
		font.setPointSize(72)
		self.totalPriceTextEdit.setFont(font)

		self.totalPriceLabel.setFont(font)

		self.totalPriceWidgetLayout.addItem(
				QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.totalPriceWidgetLayout.addWidget(self.totalPriceLabel)
		self.totalPriceWidgetLayout.addWidget(self.totalPriceTextEdit)

		self.footerWidget = FooterWidget(self)
		self.footerWidget.setObjectName('footerWidget')

		self.mainLayout.addWidget(self.topWidget)
		self.mainLayout.addWidget(self.inputWidgetGroup)
		self.mainLayout.addWidget(self.centralWidget)
		self.mainLayout.addWidget(self.totalPriceWidget)
		self.mainLayout.addWidget(self.footerWidget)

		self.productModel = ProductModel()
		path = core.fbs.get_resource('product')
		self.productModel.setPath(path)
		self.dailySoldProduct = DailyReceiptModel()

		# self.newProductShortcut = QtWidgets.QShortcut(self)
		# self.newProductShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		# self.newProductShortcut.setKey(QtGui.QKeySequence('Ctrl+N'))
		# self.newProductShortcut.activated.connect(self.showNewProductDialog)

		self.removeProductShortcut = QtWidgets.QShortcut(self.soldTableView)
		self.removeProductShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.removeProductShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
		self.removeProductShortcut.activated.connect(self.deleteProduct)

		self.pressAsteriksShortcut = QtWidgets.QShortcut(self.soldTableView)
		self.pressAsteriksShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.pressAsteriksShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Asterisk))
		self.pressAsteriksShortcut.activated.connect(self.pressAsteriks)

		self.showProductListLeftShortcut = QtWidgets.QShortcut(self.soldTableView)
		self.showProductListLeftShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.showProductListLeftShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Left))
		self.showProductListLeftShortcut.activated.connect(self.showProductList)

		self.showProductListRightShortcut = QtWidgets.QShortcut(self.soldTableView)
		self.showProductListRightShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.showProductListRightShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Right))
		self.showProductListRightShortcut.activated.connect(self.showProductList)

		self.addProductToDialySoldProductShortcut = QtWidgets.QShortcut(self)
		self.addProductToDialySoldProductShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.addProductToDialySoldProductShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_F8))
		self.addProductToDialySoldProductShortcut.activated.connect(self.addProductToDialySoldProduct)

		self.oldProductDialog = OldReceiptDialog(self)
		self.productDialog = ProductListDialog(self.productModel, self)
		self.priceDialog = PriceDialog(self.productModel, self)
		self.productAddDialog = ProductAddDialog(self.productModel, self)

		self.showPriceDialogShortcut = QtWidgets.QShortcut(self)
		self.showPriceDialogShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.showPriceDialogShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_F4))
		self.showPriceDialogShortcut.activated.connect(self.__showPriceDialog)

		self.editProductShortcut = QtWidgets.QShortcut(self)
		self.editProductShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.editProductShortcut.setKey(QtGui.QKeySequence('Ctrl+S'))
		self.editProductShortcut.activated.connect(self.addProductProduct)

		self.initSignalsAndSlots()
		self.initialize()


	def addProductProduct(self, product = None):
		self.productAddDialog.setProduct(product)
		self.productAddDialog.show()
		self.productAddDialog.raise_()


	def showProductList(self):
		self.oldProductDialog.setModel(self.dailySoldProduct)
		if self.dailySoldProduct:
			self.oldProductDialog.show()


	# def showNewProductDialog(self):
	# 	dialog = NewProductDialog(self)
	# 	dialog.show()

	def addProductToDialySoldProduct(self):
		model = self.currentSoldProductModel()
		self.dailySoldProduct.addProduct(model.copy())
		model.clear()
		self.dailySoldProduct.save()


	def pressAsteriks(self):
		self.inputWidgetGroup.enableAmountWidget()


	def deleteProduct(self):
		index = self.soldTableView.currentIndex()
		if index.isValid():
			model = index.model()
			model.pop(index.row())


	def showPopup(self, pos):
		contextMenu = QtWidgets.QMenu()
		removeAction = contextMenu.addAction('Remove')
		globalPos = self.soldTableView.mapToGlobal(pos)

		action = contextMenu.exec_(globalPos)
		if action == removeAction:
			self.deleteProduct()


	def paintEvent(self, event):
		super(MainWidget, self).paintEvent(event)


	def initSignalsAndSlots(self):
		self.productDialogButton.clicked.connect(self.showProductDialog)
		self.inputWidgetGroup.barcodeChanged.connect(self.__addProductToView)
		self.breadCrumbWidget.currentIndexChanged.connect(self.__updateSoldProductModel)
		self.breadCrumbWidget.itemAdded.connect(self.__addModelToBreadCrumbItem)
		self.priceButtonDialog.clicked.connect(self.showPriceDialogShortcut.activated.emit)


	def initialize(self):
		self.breadCrumbWidget.setDefaultButtonSize(3)
		self.breadCrumbWidget.setCurrentIndex(0)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Asterisk:
			self.inputWidgetGroup.enableAmountWidget()
		elif event.text().isdigit():
			self.inputWidgetGroup.barcodeLineEdit().setFocus()
			self.inputWidgetGroup.barcodeLineEdit().keyPressEvent(event)
		elif event.key() == QtCore.Qt.Key_F1:
			self.breadCrumbWidget.setCurrentIndex(0)
		elif event.key() == QtCore.Qt.Key_F2:
			self.breadCrumbWidget.setCurrentIndex(1)
		elif event.key() == QtCore.Qt.Key_F3:
			self.breadCrumbWidget.setCurrentIndex(2)
		elif event.key() == QtCore.Qt.Key_F12:
			fKey, res = QtWidgets.QInputDialog.getInt(self, 'Receipt Number', 'Get a number for receipt', 1, 1, 12)
			if res:
				self.breadCrumbWidget.setCurrentIndex(fKey - 1)
		elif event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Right:
			self.showProductList()
		else:
			super(MainWidget, self).keyPressEvent(event)


	def __updateTotalPriceLabel(self, _):
		totalPrice = self.currentSoldProductModel().totalPrice()
		price = '%.2f₺' % totalPrice
		width = self.totalPriceTextEdit.fontMetrics().width(price)
		self.totalPriceTextEdit.setText(price)
		self.totalPriceTextEdit.setFixedWidth(width + 20)


	def __addProductToView(self, barcode):
		if barcode == BarcodeType.CUSTOM:
			distinct = True
			product = CustomProduct(self.inputWidgetGroup.price())
		else:
			distinct = False
			product = self.productModel.getProductWithBarcode(barcode)
		if product is not None:
			if self.productModel.productType(barcode) == ProductType.WEIGHABLE:
				soldProduct = WeighableSoldProduct(product.copy())
			else:
				soldProduct = SoldProduct(product.copy(), self.inputWidgetGroup.amount())
			if soldProduct.totalPrice() != 0:
				self.currentSoldProductModel().addProduct(soldProduct, distinct)
			else:
				Toast.warning('Product Warning', 'Price of product can not be 0')
		else:
			Toast.warning('Product Warning', 'Product does not exist')


	def showProductDialog(self):
		self.productDialog.show()
		self.productDialog.raise_()


	def __showPriceDialog(self):
		self.priceDialog.show()
		self.priceDialog.raise_()


	def __updateSoldProductModel(self, index):
		itemData = self.breadCrumbWidget.itemData(index)
		self.soldTableView.setModel(itemData.model())
		self.__updateTotalPriceLabel(None)


	def __addModelToBreadCrumbItem(self, itemData):
		model = SoldProductModel(self.productModel)
		model.totalPriceChanged.connect(self.__updateTotalPriceLabel)
		itemData.setModel(model)


	def currentSoldProductModel(self):
		itemData = self.breadCrumbWidget.currentItemData()
		if itemData is None:
			return None
		else:
			return itemData.model()

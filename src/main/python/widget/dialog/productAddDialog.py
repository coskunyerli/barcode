import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
from model.product import Product
from widget.toast import Toast


class ProductAddDialog(QtWidgets.QDialog):
	def __init__(self, model, parent = None):
		super(ProductAddDialog, self).__init__(parent)
		self.__product = None
		self.__model = model
		self.mainLayout = QtWidgets.QVBoxLayout(self)

		self.barcodeInfoFrame = QtWidgets.QFrame(self)
		self.barcodeInfoFrame.setObjectName('addProductFrame')
		self.barcodeFrameLayout = QtWidgets.QGridLayout(self.barcodeInfoFrame)
		self.barcodeFrameLayout.setContentsMargins(8, 8, 8, 8)

		self.barcodeLabel = QtWidgets.QLabel(self.barcodeInfoFrame)
		self.barcodeLabel.setText('Product Barcode')
		self.barcodeLineEdit = QtWidgets.QLineEdit(self.barcodeInfoFrame)

		self.productNameLabel = QtWidgets.QLabel(self.barcodeInfoFrame)
		self.productNameLabel.setText('Product Name')
		self.productNameLineEdit = QtWidgets.QLineEdit(self.barcodeInfoFrame)

		self.barcodeFrameLayout.addWidget(self.barcodeLabel, 0, 0)
		self.barcodeFrameLayout.addWidget(self.barcodeLineEdit, 0, 1)
		self.barcodeFrameLayout.addWidget(self.productNameLabel, 1, 0)
		self.barcodeFrameLayout.addWidget(self.productNameLineEdit, 1, 1)

		self.priceFrame = QtWidgets.QFrame(self)
		self.priceFrameLayout = QtWidgets.QGridLayout(self.priceFrame)
		self.priceFrameLayout.setContentsMargins(8, 8, 8, 8)

		self.vatLabel = QtWidgets.QLabel(self.priceFrame)
		self.vatLabel.setText('Value Text Added %')
		self.vatLineEdit = QtWidgets.QLineEdit(self.priceFrame)

		self.purchasePriceLabel = QtWidgets.QLabel(self.priceFrame)
		self.purchasePriceLabel.setText('Purchase Price')
		self.purchasePriceLineEdit = QtWidgets.QLineEdit(self.priceFrame)
		self.purchasePriceLineEdit.setValidator(QtGui.QDoubleValidator())

		self.sellingPriceLabel = QtWidgets.QLabel(self.priceFrame)
		self.sellingPriceLabel.setText('Selling Price')
		self.sellingPriceLineEdit = QtWidgets.QLineEdit(self.priceFrame)
		self.sellingPriceLineEdit.setValidator(QtGui.QDoubleValidator())

		self.profitLabel = QtWidgets.QLabel(self.priceFrame)
		self.profitLabel.setText('')
		#
		self.secondSellingPriceLabel = QtWidgets.QLabel(self.priceFrame)
		self.secondSellingPriceLabel.setText('Second Selling Price')
		self.secondSellingPriceLineEdit = QtWidgets.QLineEdit(self.priceFrame)
		self.secondSellingPriceLineEdit.setValidator(QtGui.QDoubleValidator())

		self.secondProfitLabel = QtWidgets.QLabel(self.priceFrame)
		self.secondProfitLabel.setText('')

		self.priceFrameLayout.addWidget(self.vatLabel, 0, 0)
		self.priceFrameLayout.addWidget(self.vatLineEdit, 0, 1)
		self.priceFrameLayout.addWidget(self.purchasePriceLabel, 1, 0)
		self.priceFrameLayout.addWidget(self.purchasePriceLineEdit, 1, 1)
		self.priceFrameLayout.addWidget(self.sellingPriceLabel, 2, 0)
		self.priceFrameLayout.addWidget(self.sellingPriceLineEdit, 2, 1)
		self.priceFrameLayout.addWidget(self.profitLabel, 2, 2)
		self.priceFrameLayout.addWidget(self.secondSellingPriceLabel, 3, 0)
		self.priceFrameLayout.addWidget(self.secondSellingPriceLineEdit, 3, 1)
		self.priceFrameLayout.addWidget(self.secondProfitLabel, 3, 2)

		self.buttonWidget = QtWidgets.QWidget(self)
		self.buttonWidgetLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
		self.buttonWidgetLayout.setContentsMargins(0, 0, 0, 0)
		#

		self.saveButton = QtWidgets.QPushButton(self)
		self.saveButton.setText('Save')

		self.newProductButton = QtWidgets.QPushButton(self.buttonWidget)
		self.newProductButton.setText('New Product (Ctrl+N)')

		self.productButton = QtWidgets.QPushButton(self.buttonWidget)
		self.productButton.setText('Products (F9)')

		self.buttonWidgetLayout.addWidget(self.newProductButton)
		self.buttonWidgetLayout.addWidget(self.productButton)

		self.mainLayout.addWidget(self.buttonWidget)
		self.mainLayout.addWidget(self.barcodeInfoFrame)
		self.mainLayout.addWidget(self.priceFrame)
		self.mainLayout.addWidget(self.saveButton)

		self.mainLayout.addItem(
				QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

		self.initSignalsAndSlots()

		self.__initProduct(self.product())
		self.barcodeLineEdit.setFocus()


	def initSignalsAndSlots(self):
		self.productButton.clicked.connect(self.__openProductDialog)
		self.newProductButton.clicked.connect(lambda: self.setProduct(None))
		self.saveButton.clicked.connect(self.__addOrUpdateProduct)

		self.barcodeLineEdit.editingFinished.connect(self.__changeCurrentProduct)

		self.sellingPriceLineEdit.textChanged.connect(self.__updateFirstProfit)
		self.secondSellingPriceLineEdit.textChanged.connect(self.__updateSecondProfit)
		self.purchasePriceLineEdit.textChanged.connect(self.__updateProfit)


	def __updateProfit(self):
		self.__updateFirstProfit(self.sellingPriceLineEdit.text())
		self.__updateSecondProfit(self.secondSellingPriceLineEdit.text())


	def __updateSecondProfit(self, text):
		if not text:
			return
		try:
			sellingPrice = float(text)
			purchasePrice = float(self.purchasePriceLineEdit.text())
			profit = str(round((100 * sellingPrice / purchasePrice) - 100, 2))
			self.secondProfitLabel.setText(f'{profit}%')
		except Exception as e:
			Toast.warning('Profit', 'Second Profit is not calculated properly', self.parent())


	def __updateFirstProfit(self, text):
		if not text:
			return
		try:
			sellingPrice = float(text)
			purchasePrice = float(self.purchasePriceLineEdit.text())

			profit = str(round((100 * sellingPrice / purchasePrice) - 100, 2))
			self.profitLabel.setText(f'{profit}%')
		except Exception as e:
			Toast.warning('Profit', 'Profit is not calculated properly', self.parent())


	def __openProductDialog(self):
		self.parent().showProductDialog()


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F9:
			self.__openProductDialog()
		elif event.modifiers() & QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_N:
			pass
		else:
			super(ProductAddDialog, self).keyPressEvent(event)


	def __initProduct(self, product):
		self.sellingPriceLineEdit.textChanged.disconnect(self.__updateFirstProfit)
		self.secondSellingPriceLineEdit.textChanged.disconnect(self.__updateSecondProfit)
		self.purchasePriceLineEdit.textChanged.disconnect(self.__updateProfit)
		if product is not None:
			self.barcodeLineEdit.setText(product.id())
			self.productNameLineEdit.setText(product.name())
			self.purchasePriceLineEdit.setText(str(product.purchasePrice()))
			self.sellingPriceLineEdit.setText(str(product.sellingPrice()))
			self.secondSellingPriceLineEdit.setText(str(product.secondSellingPrice()))
			self.vatLineEdit.setText(str(product.valueAddedTax()))
			self.__updateProfit()
		else:
			self.barcodeLineEdit.setText('')
			self.productNameLineEdit.setText('')
			self.purchasePriceLineEdit.setText('')
			self.sellingPriceLineEdit.setText('')
			self.vatLineEdit.setText('')
			self.secondSellingPriceLineEdit.setText('')

		self.sellingPriceLineEdit.textChanged.connect(self.__updateFirstProfit)
		self.secondSellingPriceLineEdit.textChanged.connect(self.__updateSecondProfit)
		self.purchasePriceLineEdit.textChanged.connect(self.__updateProfit)


	def __changeCurrentProduct(self):
		barcode = self.barcodeLineEdit.text()
		product = self.__model.getProductWithBarcode(barcode)
		self.setProduct(product)
		self.barcodeLineEdit.setText(barcode)


	def product(self):
		return self.__product


	def setProduct(self, product):
		self.__product = product
		self.__initProduct(product)


	def show(self):
		self.barcodeLineEdit.setFocus()
		super(ProductAddDialog, self).show()


	def __addOrUpdateProduct(self):
		# todo ekmek de sorun var farklı bir id ile kaydediyor ona bak bir.
		try:
			barcode = self.barcodeLineEdit.text()
			index = self.__model.getIndexWithBarcode(barcode)
			if index.isValid() is True:
				index.model().setData(index, self.__updateProductValue)
				Toast.success('Product Edit', 'Product is updated successfully', self.parent())
			else:
				barcode = self.barcodeLineEdit.text()
				name = self.productNameLineEdit.text()
				purchasePrice = float(self.purchasePriceLineEdit.text())
				sellingPrice = float(self.sellingPriceLineEdit.text())
				secondSellingPrice = float(self.secondSellingPriceLineEdit.text())
				valueTaxAdded = float(self.vatLineEdit.text())
				product = Product(barcode, name, str(purchasePrice), str(sellingPrice), secondSellingPrice, None,
								  str(valueTaxAdded))
				self.__model.addProduct(product)
				Toast.success('Product Add', 'New product is added successfully', self.parent())
		except Exception as e:
			print(f'Product is not added or updated successfully. Exception is {e}')
			Toast.error('Update Error', 'Product is not added or updated successfully', self.parent())

		self.setProduct(None)


	def __updateProductValue(self, product):
		name = self.productNameLineEdit.text()
		purchasePrice = float(self.purchasePriceLineEdit.text())
		sellingPrice = float(self.sellingPriceLineEdit.text())
		valueTaxAdded = float(self.vatLineEdit.text())
		secondSellingPrice = float(self.secondSellingPriceLineEdit.text())

		product.setName(name)
		product.setSellingPrice(sellingPrice)
		product.setPurchasePrice(purchasePrice)
		product.setValueAddedTax(valueTaxAdded)
		product.setSecondSellingPrice(secondSellingPrice)
		return True

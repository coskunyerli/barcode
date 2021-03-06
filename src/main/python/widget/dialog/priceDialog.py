import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
from enums import BarcodeType
from widget.dialogNameWidget import DialogNameWidget
from widget.toast import Toast

from fontSize import FontSize


class PriceDialog(QtWidgets.QDialog):
	def __init__(self, model, parent = None):
		super(PriceDialog, self).__init__(parent)
		self.__model = model
		self.setFixedWidth(500)
		self.setWindowTitle('Product Price')
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(8, 8, 8, 8)
		self.verticalLayout.setSpacing(8)

		self.dialogNameLabel = DialogNameWidget(self)
		self.dialogNameLabel.setText('Product Price')
		self.dialogNameLabel.setPointSize(FontSize.dialogNameLabelFontSize())
		self.dialogNameLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.barcodeLineEdit = QtWidgets.QLineEdit(self)
		self.barcodeLineEdit.setObjectName('barcodeLineEdit')
		self.barcodeLineEdit.setPlaceholderText('Barcode')
		self.infoWidget = QtWidgets.QFrame(self)

		self.infoWidgetLayout = QtWidgets.QHBoxLayout(self.infoWidget)
		self.infoWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.infoWidgetLayout.setSpacing(0)

		self.barcodeLabel = QtWidgets.QLabel(self.infoWidget)
		self.barcodeLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.productNameLabel = QtWidgets.QLabel(self.infoWidget)
		self.productNameLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.barcodeLabelText = QtWidgets.QLabel(self.infoWidget)
		self.barcodeLabelText.setText('Barcode:')
		self.barcodeLabel.setObjectName('barcodeLabel')
		self.productNameLabelText = QtWidgets.QLabel(self.infoWidget)
		self.productNameLabelText.setText('Product Name:')
		self.productNameLabel.setObjectName('productLabel')

		self.lineItem = QtWidgets.QFrame(self.infoWidget)
		self.lineItem.setFixedWidth(1)
		self.lineItem.setObjectName('lineItem')
		self.infoWidgetLayout.addWidget(self.barcodeLabelText)
		self.infoWidgetLayout.addWidget(self.barcodeLabel)
		self.infoWidgetLayout.addWidget(self.lineItem)
		self.infoWidgetLayout.addWidget(self.productNameLabelText)
		self.infoWidgetLayout.addWidget(self.productNameLabel)

		self.priceWidget = QtWidgets.QWidget(self)
		self.priceWidgetLayout = QtWidgets.QHBoxLayout(self.priceWidget)
		self.priceWidgetLayout.setContentsMargins(0, 5, 0, 0)
		self.priceWidgetLayout.addItem(
				QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

		self.priceLabel = QtWidgets.QLineEdit(self)
		self.priceLabel.setObjectName('totalPriceTextEdit')
		self.priceLabel.setReadOnly(True)
		self.priceLabel.setFocusPolicy(QtCore.Qt.NoFocus)
		self.priceLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.priceWidgetLayout.addWidget(self.priceLabel)
		font = self.priceLabel.font()
		font.setPointSize(FontSize.totalPriceInPriceDialogFontSize())
		self.priceLabel.setFont(font)

		self.verticalLayout.addWidget(self.dialogNameLabel)
		self.verticalLayout.addWidget(self.barcodeLineEdit)
		self.verticalLayout.addWidget(self.infoWidget)
		self.verticalLayout.addWidget(self.priceWidget)

		# update size
		totalPrice = 0.0
		price = '%.2f₺' % float(totalPrice)
		width = self.priceLabel.fontMetrics().width(price)
		self.priceLabel.setText(price)
		self.priceLabel.setFixedWidth(width + 20)

		self.showProductShortcut = QtWidgets.QShortcut(self.priceLabel)
		self.showProductShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))
		self.showProductShortcut.activated.connect(self.__updatePriceLabel)

		self.closeProductShortcut = QtWidgets.QShortcut(self)
		self.closeProductShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.closeProductShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_F4))
		self.closeProductShortcut.activated.connect(self.close)

		self.__model.dataChanged.connect(self.__updateProductPrice)


	def __updateProductPrice(self):
		barcode = self.barcodeLabel.text()
		product = self.__model.getProductWithBarcode(barcode)
		if product is not None:
			self.barcodeLabel.setText(product.barcode())
			self.productNameLabel.setText(product.name())
			totalPrice = product.sellingPrice()
			price = '%.2f₺' % float(totalPrice)
			width = self.priceLabel.fontMetrics().width(price)
			self.priceLabel.setText(price)
			self.priceLabel.setFixedWidth(width + 20)


	def __updatePriceLabel(self):
		barcode = self.barcodeLineEdit.text()
		if barcode == BarcodeType.INVALID:
			return

		if barcode == BarcodeType.CUSTOM:
			Toast.warning('Product Warning', 'Barcode can not be zero')
			return
		product = self.__model.getProductWithBarcode(barcode)
		if product is not None:
			self.barcodeLabel.setText(product.barcode())
			self.productNameLabel.setText(product.name())
			totalPrice = product.sellingPrice()
			price = '%.2f₺' % float(totalPrice)
			width = self.priceLabel.fontMetrics().width(price)
			self.priceLabel.setText(price)
			self.priceLabel.setFixedWidth(width + 20)

		else:
			Toast.warning('Product Warning', 'Product does not exist')

		self.barcodeLineEdit.selectAll()

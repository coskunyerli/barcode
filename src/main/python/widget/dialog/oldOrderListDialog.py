import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
from model.order import Order
from model.sizeInfo import SizeInfo
from model.soldProductModel import SoldProductModel
from service.databaseService import DatabaseService
from widget.dialogNameWidget import DialogNameWidget

from fontSize import FontSize

currentIndex = 0
sizeInfo = SizeInfo(None, None)


class OldReceiptDialog(QtWidgets.QDialog, DatabaseService):

	@classmethod
	def setSizeInfo(cls, sizeInfo2):
		global sizeInfo
		sizeInfo = sizeInfo2


	@classmethod
	def sizeInfo(cls):
		return sizeInfo


	def __init__(self, parent = None):
		super(OldReceiptDialog, self).__init__(parent)
		self.resize(800, 300)
		self.setModal(True)
		self.setWindowTitle('Sold Product')
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(8, 4, 8, 2)
		self.verticalLayout.setSpacing(4)

		self.dialogNameLabel = DialogNameWidget(self)
		self.dialogNameLabel.setText('Sold Products')
		self.dialogNameLabel.setPointSize(FontSize.dialogNameLabelFontSize())
		self.dialogNameLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.soldProductLabelView = QtWidgets.QTableView(self)

		self.soldProductLabelView.setFocusPolicy(QtCore.Qt.NoFocus)
		self.infoWidget = QtWidgets.QWidget(self)
		self.infoWidgetLayout = QtWidgets.QHBoxLayout(self.infoWidget)
		self.infoWidgetLayout.setContentsMargins(8, 4, 8, 4)

		self.infoWidgetIndexInfoLineEdit = QtWidgets.QLineEdit(self.infoWidget)
		validator = QtGui.QIntValidator()
		self.infoWidgetIndexInfoLineEdit.setValidator(validator)
		self.infoWidgetIndexInfoLineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.infoWidgetIndexInfoLineEdit.setObjectName('indexInfoLineEdit')
		self.infoWidgetIndexInfoLabelText = QtWidgets.QLabel(self.infoWidget)
		self.infoWidgetIndexInfoLabelText.setText('Product')

		self.dateInfoLabelText = QtWidgets.QLabel(self.infoWidget)
		self.dateInfoLabelText.setText('Date:')
		self.dateInfoLabel = QtWidgets.QLabel(self.infoWidget)

		self.infoWidgetLayout.addWidget(self.infoWidgetIndexInfoLabelText)
		self.infoWidgetLayout.addWidget(self.infoWidgetIndexInfoLineEdit)
		self.infoWidgetLayout.addWidget(self.dateInfoLabelText)
		self.infoWidgetLayout.addWidget(self.dateInfoLabel)

		self.priceLabel = QtWidgets.QLineEdit(self.infoWidget)
		self.priceLabel.setObjectName('totalPriceTextEdit')
		self.priceLabel.setReadOnly(True)
		self.priceLabel.setFocusPolicy(QtCore.Qt.NoFocus)
		self.priceLabel.setAlignment(QtCore.Qt.AlignCenter)
		font = self.priceLabel.font()
		font.setPointSize(FontSize.dialogNameLabelFontSize())
		self.priceLabel.setFont(font)

		self.infoWidgetLayout.addItem(
				QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.infoWidgetLayout.addWidget(self.priceLabel)

		self.verticalLayout.addWidget(self.dialogNameLabel)
		self.verticalLayout.addWidget(self.soldProductLabelView)
		self.verticalLayout.addWidget(self.infoWidget)
		self.__dailySoldProduct = None

		self.infoWidgetIndexInfoLineEdit.editingFinished.connect(self.__updateCurrentIndex)

		self.__updateHeaderSizes()
		orderListDatabase = self.databaseService().query(Order).limit(2000).all()
		orderList = []
		for databaseOrder in orderListDatabase:
			order = Order.fromDatabase(databaseOrder)
			model = SoldProductModel()
			model.setOrder(order)
			model.setReadOnly(True)
			orderList.append(model)

		self.setModel(orderList)


	def __updateCurrentIndex(self):
		index = int(self.infoWidgetIndexInfoLineEdit.text())
		if 0 <= index < len(self.__dailySoldProduct):
			self.setCurrentProductIndex(index)
			self.setFocus()


	def model(self):
		return self.soldProductLabelView.model()


	def setModel(self, model):
		self.__dailySoldProduct = model
		self.__update()


	def setCurrentProductIndex(self, index):
		global currentIndex
		currentIndex = (index % len(self.__dailySoldProduct))
		self.__update()


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Left:
			index = currentIndex
			self.setCurrentProductIndex(index - 1)
		elif event.key() == QtCore.Qt.Key_Right:
			index = currentIndex
			self.setCurrentProductIndex(index + 1)
		else:
			super(OldReceiptDialog, self).keyPressEvent(event)


	def closeEvent(self, event):
		headerView = self.soldProductLabelView.horizontalHeader()
		headerSizes = []
		for i in range(headerView.count()):
			headerSizes.append(int(headerView.sectionSize(i)))

		size = self.size()
		OldReceiptDialog.setSizeInfo(SizeInfo(size, headerSizes))
		super(OldReceiptDialog, self).closeEvent(event)


	def __update(self):
		index = currentIndex
		if self.__dailySoldProduct:
			model = self.__dailySoldProduct[index]
			width = self.priceLabel.fontMetrics().width(str(index))
			self.infoWidgetIndexInfoLineEdit.setText(str(index))
			self.infoWidgetIndexInfoLineEdit.setFixedWidth(width + 20)

			self.soldProductLabelView.setModel(model)

			totalPrice = self.model().totalPrice()
			price = '%.2f₺' % totalPrice
			width = self.priceLabel.fontMetrics().width(price)
			self.priceLabel.setText(price)
			self.priceLabel.setFixedWidth(width + 20)

			self.dateInfoLabel.setText(model.date().strftime("%d/%m/%Y, %H:%M:%S"))
			self.__updateHeaderSizes()


	def __updateHeaderSizes(self):
		if OldReceiptDialog.sizeInfo() is not None and OldReceiptDialog.sizeInfo().isValid():
			self.resize(OldReceiptDialog.sizeInfo().size)
			headerView = self.soldProductLabelView.horizontalHeader()
			for i in range(len(self.sizeInfo().headerSizes)):
				headerView.resizeSection(i, int(self.sizeInfo().headerSizes[i]))

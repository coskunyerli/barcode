import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets
from model.order import Order
from model.sizeInfo import SizeInfo
from model.soldProductModel import SoldProductModel
from service.databaseService import DatabaseService
from widget.soldOrderListWidget import SoldOrderListWidget

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
		self.verticalLayout.setSpacing(0)
		self.soldListViewWidget = SoldOrderListWidget(self)

		orderListDatabase = self.databaseService().query(Order).limit(2000).all()
		orderList = []
		for databaseOrder in orderListDatabase:
			order = Order.fromDatabase(databaseOrder)
			model = SoldProductModel()
			model.setOrder(order)
			model.setReadOnly(True)
			orderList.append(model)

		self.soldListViewWidget.setModel(orderList)

		global currentIndex
		currentIndex = len(orderList) - 1

		self.soldListViewWidget.setCurrentProductIndex(currentIndex)
		self.verticalLayout.addWidget(self.soldListViewWidget)

		self.__updateHeaderSizes()

		self.soldListViewWidget.currentIndexChanged.connect(self.__updateHeaderSizes)
		self.soldListViewWidget.soldProductLabelView.horizontalHeader().sectionResized.connect(self.__saveHeaderSizes)


	def keyPressEvent(self, event):
		global currentIndex
		if event.key() == QtCore.Qt.Key_Left:
			self.soldListViewWidget.setCurrentProductIndex(currentIndex - 1)
			currentIndex = currentIndex - 1
		elif event.key() == QtCore.Qt.Key_Right:
			self.soldListViewWidget.setCurrentProductIndex(currentIndex + 1)
			currentIndex = currentIndex + 1
		else:
			super(OldReceiptDialog, self).keyPressEvent(event)


	def closeEvent(self, event):
		size = self.size()
		OldReceiptDialog.sizeInfo().size = size
		super(OldReceiptDialog, self).closeEvent(event)


	def __updateHeaderSizes(self):
		if OldReceiptDialog.sizeInfo() is not None and OldReceiptDialog.sizeInfo().isValid():
			self.resize(OldReceiptDialog.sizeInfo().size)
			headerView = self.soldListViewWidget.soldProductLabelView.horizontalHeader()
			for i in range(len(self.sizeInfo().headerSizes)):
				headerView.resizeSection(i, int(self.sizeInfo().headerSizes[i]))


	def __saveHeaderSizes(self, index, old, new):
		OldReceiptDialog.sizeInfo().headerSizes[index] = new

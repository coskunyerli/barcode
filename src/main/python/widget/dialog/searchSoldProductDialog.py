import datetime

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
from delegate.searchSoldProductDelegate import SearchSoldProductDelegate
from model.db.databaseOrder import DatabaseOrder
from model.db.databaseSoldProduct import DatabaseSoldProduct
from model.order import Order
from model.orderModel import OrderModel
from model.sizeInfo import SizeInfo
from model.soldProductModel import SoldProductModel
from service.databaseService import DatabaseService
from sqlalchemy import desc
from widget.soldOrderListWidget import SoldOrderListWidget


class ListView(QtWidgets.QListView):
	currentIndexChanged = QtCore.Signal(QtCore.QModelIndex)


	def currentChanged(self, current, previous):
		super(ListView, self).currentChanged(current, previous)
		if current != previous:
			self.currentIndexChanged.emit(current)


sizeInfo = SizeInfo(None, None)


class SearchSoldProductDialog(QtWidgets.QDialog, DatabaseService):
	@classmethod
	def sizeInfo(cls):
		return sizeInfo


	@classmethod
	def setSizeInfo(cls, sInfo):
		global sizeInfo
		sizeInfo = sInfo


	def __init__(self, parent = None):
		super(SearchSoldProductDialog, self).__init__(parent)
		self.resize(1024, 600)
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		self.searchWidget = QtWidgets.QWidget(self)
		self.searchWidgetLayout = QtWidgets.QHBoxLayout(self.searchWidget)
		self.searchWidgetLayout.setContentsMargins(8, 0, 8, 0)
		self.searchWidgetLayout.setSpacing(4)

		self.lineEdit = QtWidgets.QLineEdit(self.searchWidget)
		self.lineEdit.setPlaceholderText('Enter a product name to search')

		self.lineEdit.setStyleSheet('padding-left:8px;border-radius:4px;color:white')
		self.calenderLineEdit = QtWidgets.QDateTimeEdit(QtCore.QDate(QtCore.QDate.currentDate()), self.searchWidget)
		self.calenderLineEdit.setCalendarPopup(True)
		self.calenderLineEdit.setStyleSheet('color:black')

		self.limitWidget = QtWidgets.QWidget(self.searchWidget)
		# self.limitWidget.setSizePolicy(sizePolicy)
		self.limitWidgetLayout = QtWidgets.QHBoxLayout(self.limitWidget)
		self.limitWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.limitWidgetLayout.setSpacing(0)
		self.limitLabel = QtWidgets.QLabel(self.limitWidget)
		self.limitLabel.setText('Search Limit:')

		self.limitSpinbox = QtWidgets.QSpinBox(self.searchWidget)
		self.limitSpinbox.setMinimum(1)
		self.limitSpinbox.setMaximum(1000)
		self.limitSpinbox.setValue(30)
		self.limitSpinbox.setStyleSheet('color:black')

		self.limitWidgetLayout.addWidget(self.limitLabel)
		self.limitWidgetLayout.addWidget(self.limitSpinbox)

		self.searchButton = QtWidgets.QPushButton(self.searchWidget)
		self.searchButton.setText('Search')

		self.searchWidgetLayout.addWidget(self.lineEdit)
		self.searchWidgetLayout.addWidget(self.calenderLineEdit)
		self.searchWidgetLayout.addWidget(self.limitWidget)
		self.searchWidgetLayout.addWidget(self.searchButton)

		self.listView = ListView(self)
		self.listView.setItemDelegate(SearchSoldProductDelegate(self.listView))

		self.tableView = SoldOrderListWidget(self)
		self.tableView.infoWidgetIndexInfoLineEdit.hide()
		self.tableView.infoWidgetIndexInfoLabelText.hide()

		self.orderModel = OrderModel()
		self.listView.setModel(self.orderModel)

		self.__search()

		self.verticalLayout.addWidget(self.searchWidget)
		self.verticalLayout.addWidget(self.listView)
		self.verticalLayout.addWidget(self.tableView)

		self.listView.currentIndexChanged.connect(self.__updateSoldProductList)
		self.listView.setCurrentIndex(self.listView.model().index(0))
		self.listView.setStyleSheet('background-color:#404040')

		self.searchButton.clicked.connect(self.__search)

		self.tableView.soldProductLabelView.horizontalHeader().sectionResized.connect(self.__saveHeaderSizes)
		headerSizes = []

		for i in range(self.tableView.soldProductLabelView.horizontalHeader().count()):
			headerSizes.append(self.tableView.soldProductLabelView.horizontalHeader().sectionSize(i))

		SearchSoldProductDialog.sizeInfo().headerSizes = headerSizes


	def __search(self):
		nameText = self.lineEdit.text()
		date = self.calenderLineEdit.date().toPython()
		dtime = datetime.datetime.combine(date, datetime.datetime.max.time())

		limit = self.limitSpinbox.value()
		query = self.databaseService().query(Order)
		if nameText:
			query = query.join(DatabaseSoldProduct).filter(
					DatabaseSoldProduct.product_name.like(f'%{nameText}%'))
		query = query.filter(DatabaseOrder.created_date <= dtime)
		query = query.order_by(desc(DatabaseOrder.created_date)).limit(limit)

		orderList = []
		for databaseOrder in query:
			order = Order.fromDatabase(databaseOrder)
			orderList.append(order)

		self.orderModel.setOrderList(orderList)


	def __updateSoldProductList(self, index):
		order = index.data(QtCore.Qt.UserRole)
		model = SoldProductModel()
		model.setReadOnly(True)
		model.setOrder(order)
		self.tableView.setModel([model])
		self.tableView.setCurrentProductIndex(0)
		self.__updateHeaderSizes()


	def closeEvent(self, event):
		super(SearchSoldProductDialog, self).closeEvent(event)
		SearchSoldProductDialog.sizeInfo().size = self.size()


	def __updateHeaderSizes(self):
		if SearchSoldProductDialog.sizeInfo() is not None and SearchSoldProductDialog.sizeInfo().isValid():
			self.resize(SearchSoldProductDialog.sizeInfo().size)
			headerView = self.tableView.soldProductLabelView.horizontalHeader()
			for i in range(len(SearchSoldProductDialog.sizeInfo().headerSizes)):
				headerView.resizeSection(i, int(SearchSoldProductDialog.sizeInfo().headerSizes[i]))


	def __saveHeaderSizes(self, index, old, new):
		SearchSoldProductDialog.sizeInfo().headerSizes[index] = new

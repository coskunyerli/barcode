import datetime

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
from delegate.searchSoldProductDelegate import SearchSoldProductDelegate
from fontSize import FontSize
from model.db.databaseOrder import DatabaseOrder
from model.db.databaseSoldProduct import DatabaseSoldProduct
from model.order import Order
from model.orderModel import OrderModel
from model.sizeInfo import SizeInfo
from model.soldProductModel import SoldProductModel
from service.databaseService import DatabaseService
from sqlalchemy import desc
from widget.dialogNameWidget import DialogNameWidget
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

		self.setWindowTitle('Search Order')

		self.searchWidget = QtWidgets.QWidget(self)
		self.searchWidgetLayout = QtWidgets.QHBoxLayout(self.searchWidget)
		self.searchWidgetLayout.setContentsMargins(8, 0, 8, 0)
		self.searchWidgetLayout.setSpacing(4)


		self.lineEdit = QtWidgets.QLineEdit(self.searchWidget)
		self.lineEdit.setPlaceholderText('Enter a product name to search')

		self.lineEdit.setStyleSheet('padding-left:8px;border-radius:4px;color:white')
		self.startCheckBox = QtWidgets.QCheckBox(self.searchWidget)
		self.startCheckBox.setText('Disable Start Time')
		self.startCalenderLineEdit = QtWidgets.QDateTimeEdit(QtCore.QDate(QtCore.QDate.currentDate()),
															 self.searchWidget)
		self.startCalenderLineEdit.setCalendarPopup(True)
		self.startCalenderLineEdit.setStyleSheet('color:black')

		self.stopCheckBox = QtWidgets.QCheckBox(self.searchWidget)
		self.stopCheckBox.setText('Disable Stop Time')
		self.stopCalenderLineEdit = QtWidgets.QDateTimeEdit(QtCore.QDate(QtCore.QDate.currentDate()), self.searchWidget)
		self.stopCalenderLineEdit.setCalendarPopup(True)
		self.stopCalenderLineEdit.setStyleSheet('color:black')

		self.limitWidget = QtWidgets.QWidget(self.searchWidget)
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
		self.searchWidgetLayout.addWidget(self.startCheckBox)
		self.searchWidgetLayout.addWidget(self.startCalenderLineEdit)
		self.searchWidgetLayout.addWidget(self.stopCheckBox)
		self.searchWidgetLayout.addWidget(self.stopCalenderLineEdit)
		self.searchWidgetLayout.addWidget(self.limitWidget)
		self.searchWidgetLayout.addWidget(self.searchButton)

		self.listView = ListView(self)
		self.listView.setItemDelegate(SearchSoldProductDelegate(self.listView))

		self.tableView = SoldOrderListWidget(self)
		self.tableView.infoWidgetIndexInfoLineEdit.hide()
		self.tableView.infoWidgetIndexInfoLabelText.hide()

		self.orderModel = OrderModel()
		self.listView.setModel(self.orderModel)
		self.startCheckBox.stateChanged.connect(self.__updateStartCalender)
		self.stopCheckBox.stateChanged.connect(self.__updateStopCalender)

		self.startCheckBox.setChecked(True)

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


	def __updateStartCalender(self, value):
		self.startCalenderLineEdit.setDisabled(value)


	def __updateStopCalender(self, value):
		self.stopCalenderLineEdit.setDisabled(value)


	def __search(self):
		nameText = self.lineEdit.text()
		sdate = self.startCalenderLineEdit.date().toPython()
		startDate = datetime.datetime.combine(sdate, datetime.datetime.min.time())

		eDate = self.stopCalenderLineEdit.date().toPython()
		stopDate = datetime.datetime.combine(eDate, datetime.datetime.max.time())

		limit = self.limitSpinbox.value()
		query = self.databaseService().query(Order)
		if nameText:
			query = query.join(DatabaseSoldProduct).filter(
					DatabaseSoldProduct.product_name.like(f'%{nameText}%'))
		if self.stopCalenderLineEdit.isEnabled():
			query = query.filter(DatabaseOrder.created_date <= stopDate)
		if self.startCalenderLineEdit.isEnabled():
			query = query.filter(startDate <= DatabaseOrder.created_date)
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

import datetime

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
from fontSize import FontSize
from model.db.databaseOrder import DatabaseOrder
from model.db.databaseSoldProduct import DatabaseSoldProduct
from service.databaseService import DatabaseService
from sqlalchemy import func
from widget.dialogNameWidget import DialogNameWidget


class IncomeDialog(QtWidgets.QDialog, DatabaseService):
	def __init__(self, parent = None):
		super(IncomeDialog, self).__init__(parent)
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(8, 8, 8, 8)
		self.dialogNameLabel = DialogNameWidget(self)
		self.dialogNameLabel.setText('Income')
		self.dialogNameLabel.setPointSize(FontSize.dialogNameLabelFontSize())
		self.dialogNameLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.dateLineEdit = QtWidgets.QDateTimeEdit(QtCore.QDate(QtCore.QDate.currentDate()), self)
		self.dateLineEdit.setCalendarPopup(True)
		self.dateLineEdit.setStyleSheet('color:black')

		self.informationWidget = QtWidgets.QWidget(self)
		self.informationGridLayout = QtWidgets.QGridLayout(self.informationWidget)

		self.verticalLayout.addWidget(self.dialogNameLabel)
		self.verticalLayout.addWidget(self.dateLineEdit)
		self.verticalLayout.addWidget(self.informationWidget)

		self.setWindowTitle('Income')
		self.totalIncomeLabel = QtWidgets.QLabel(self)
		self.totalIncomeLabelText = QtWidgets.QLabel(self)
		self.totalIncomeLabelText.setStyleSheet('background-color:#505050;padding:4px;border-radius:4px')

		self.totalProfitLabel = QtWidgets.QLabel(self)
		self.totalProfitLabelText = QtWidgets.QLabel(self)
		self.totalProfitLabelText.setStyleSheet('background-color:#505050;padding:4px;border-radius:4px')

		self.totalProfitLabel.setText('Total Profit')
		self.totalIncomeLabel.setText('Total Income')

		self.informationGridLayout.addWidget(self.totalIncomeLabel, 0, 0)
		self.informationGridLayout.addWidget(self.totalIncomeLabelText, 0, 1)
		self.informationGridLayout.addWidget(self.totalProfitLabel, 1, 0)
		self.informationGridLayout.addWidget(self.totalProfitLabelText, 1, 1)

		self.__update(self.dateLineEdit.date())
		self.dateLineEdit.dateChanged.connect(self.__update)


	def __update(self, date):
		sdate = date.toPython()

		startDate = datetime.datetime.combine(sdate, datetime.datetime.min.time())
		stopDate = datetime.datetime.combine(sdate, datetime.datetime.max.time())

		query = self.databaseService().session().query(
				func.sum(DatabaseSoldProduct.product_sellingPrice).label("totalSellingPrice"),
				func.sum(DatabaseSoldProduct.product_purchasePrice).label("totalPurchasePrice")).filter(
				startDate <= DatabaseOrder.created_date).filter(
				DatabaseOrder.created_date <= stopDate).join(DatabaseOrder)
		if (query.all()):
			totalSellingPrice, totalPurchasePrice = query[0]
			if totalSellingPrice is None:
				totalSellingPrice = 0
			if totalPurchasePrice is None:
				totalPurchasePrice = 0
		else:
			totalSellingPrice = 0
			totalPurchasePrice = 0

		self.totalIncomeLabelText.setText(f'{str(round(totalSellingPrice, 2))}₺')
		self.totalProfitLabelText.setText(f'{str(round(totalSellingPrice - totalPurchasePrice, 2))}₺')

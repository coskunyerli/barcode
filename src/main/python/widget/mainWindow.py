from datetime import date
import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import core
import log

from model.dictList import DictList
from model.product import Product
from model.productModel import ProductModel
from widget.mainWidget import MainWidget
from widget.toast import Toast


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		menubar = self.menuBar()
		menu = QtWidgets.QMenu('File')
		self.importCsvAction = menu.addAction('Import CSV')
		menubar.addMenu(menu)
		self.importCsvAction.triggered.connect(self.importCSVFile)

		self.mainWidget = MainWidget(self)
		self.__date = date.today()
		self.__lastLoadPath = None
		self.settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "Barcode", "barcode")
		self.setCentralWidget(self.mainWidget)
		self.importCSVShortCut = QtWidgets.QShortcut(self)
		self.importCSVShortCut.setKey(QtGui.QKeySequence('Ctrl+O'))
		self.importCSVShortCut.activated.connect(self.importCSVFile)
		self.initSignalsAndSlots()
		self.readSettings()


	def readSettings(self):
		self.resize(self.settings.value("windowSize", QtCore.QSize(1278, 768)))
		headerSizesDict = self.settings.value('headerSizes', {})
		headerSizes = headerSizesDict.get('soldTableView', [])
		headerView = self.mainWidget.soldTableView.horizontalHeader()
		for i in range(len(headerSizes)):
			headerView.resizeSection(i, int(headerSizes[i]))

		headerSizes = headerSizesDict.get('productTableView', [])
		headerView = self.mainWidget.productDialog.productTableView.horizontalHeader()
		for i in range(len(headerSizes)):
			headerView.resizeSection(i, int(headerSizes[i]))

		headerSizes = headerSizesDict.get('soldProductLabelView', [])
		headerView = self.mainWidget.oldProductDialog.soldProductLabelView.horizontalHeader()
		for i in range(len(headerSizes)):
			headerView.resizeSection(i, int(headerSizes[i]))

		self.mainWidget.productDialog.resize(self.settings.value('productDialogSize', QtCore.QSize(1000, 600)))
		self.mainWidget.oldProductDialog.resize(self.settings.value('oldProductDialogSize', QtCore.QSize(800, 300)))

		self.mainWidget.dailySoldProduct.read()

		date_ = int(self.settings.value('date'))
		if date_ is not None:
			self.__date = date.fromordinal(date_)
		else:
			self.__date = date.today()


	# productListInDict = self.settings.value('productModelDict')
	# if productListInDict is not None:
	# 	productList = ProductModel.fromJson(productListInDict)
	# 	self.mainWidget.productModel.setProductList(productList)

	def writeSettings(self):
		headerSizes = {}
		sizes = []
		headerView = self.mainWidget.soldTableView.horizontalHeader()
		for i in range(headerView.count()):
			sizes.append(headerView.sectionSize(i))

		headerSizes['soldTableView'] = sizes

		sizes = []
		headerView = self.mainWidget.productDialog.productTableView.horizontalHeader()
		for i in range(headerView.count()):
			sizes.append(headerView.sectionSize(i))

		headerSizes['productTableView'] = sizes

		sizes = []
		headerView = self.mainWidget.oldProductDialog.soldProductLabelView.horizontalHeader()
		for i in range(headerView.count()):
			sizes.append(headerView.sectionSize(i))

		headerSizes['soldProductLabelView'] = sizes

		self.settings.setValue('headerSizes', headerSizes)
		self.settings.setValue('windowSize', self.size())

		self.settings.setValue('productDialogSize', self.mainWidget.productDialog.size())
		self.settings.setValue('oldProductDialogSize', self.mainWidget.oldProductDialog.size())

		self.mainWidget.dailySoldProduct.save()

		self.settings.setValue('date', self.__date.toordinal())


	# productListInDict = self.mainWidget.productModel.json()
	# self.settings.setValue('productModelDict', productListInDict)

	def closeEvent(self, event):
		self.cleanupBeforeClose()
		super(MainWindow, self).closeEvent(event)


	def cleanupBeforeClose(self):
		self.writeSettings()


	def initSignalsAndSlots(self):
		self.mainWidget.exitButton.clicked.connect(self.close)


	def importCSVFile(self):
		filename, res = QtWidgets.QFileDialog.getOpenFileName(self, "Import CSV File", '',
															  "CSV Files(*.csv)")
		try:
			if res and filename:
				res = self.__importCSVFile(filename)
				if res is True:
					self.__lastLoadPath = filename
					Toast.success('CSV Import', 'Importing CSV file is done successfully', self)
				else:
					Toast.error('CSV Import', 'Invalid file CSV to import')
		except Exception as e:
			log.error(f'There is an error importing csv file. File is {filename}. error is {e}')
			Toast.error('CSV Import', 'Error occurred while importing CSV file')


	def __importCSVFile(self, filename):
		file = QtCore.QFile(filename)
		if not file.open(QtCore.QIODevice.ReadOnly):
			log.error(f'There is invalid file to read {filename}')
			return False
		title = True
		productList = DictList()
		try:
			while not file.atEnd():
				line = str(file.readLine().data(), encoding = 'ISO 8859-9')
				if title:
					title = False
				else:
					productInList = line.split(',')

					product = Product(productInList[1], productInList[3].strip(), productInList[9], productInList[5],
									  productInList[7], productInList[-1])
					if product.id() not in productList:
						productList.setItem(product.id(), product)

			self.mainWidget.productModel.setProductList(productList)
		except Exception as e:
			log.error(f'Error occurred reading CSV file {filename}. Error is => {e}')
			return False

		return True

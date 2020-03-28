import datetime
import json
import os
from datetime import date
import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import log
from enums import ProductType

from model.dictList import DictList
from model.sizeInfo import SizeInfo
from service.databaseService import DatabaseService
from service.filePathService import FilePathService
from service.preferencesService import PreferencesService
from model.product import Product
from widget.buttonGroupWidget import ButtonItemData
from widget.dialog.oldOrderListDialog import OldReceiptDialog
from widget.dialog.productListDialog import ProductListDialog
from widget.dialog.searchSoldProductDialog import SearchSoldProductDialog
from widget.mainWidget import MainWidget
from widget.toast import Toast


class MainWindow(QtWidgets.QMainWindow, PreferencesService, FilePathService, DatabaseService):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		menubar = self.menuBar()
		menu = QtWidgets.QMenu('File')
		self.importCsvAction = menu.addAction('Import CSV')
		self.importCsvAction.setShortcut(QtGui.QKeySequence('Ctrl+O'))
		self.exportCsvAction = menu.addAction('Export CSV')
		self.exportCsvAction.setShortcut(QtGui.QKeySequence('Ctrl+X'))
		menubar.addMenu(menu)
		self.importCsvAction.triggered.connect(self.importCSVFile)
		self.exportCsvAction.triggered.connect(self.exportCSVFile)

		self.mainWidget = MainWidget(self)
		self.__date = date.today()
		self.__lastLoadPath = None
		self.settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "Barcode", "barcode")
		self.setCentralWidget(self.mainWidget)

		self.initSignalsAndSlots()


	def afterReadSettings(self):
		pass


	def readSettings(self):
		productDictList = self.__dataBaseToProductList()
		self.mainWidget.productModel.setProductList(productDictList)
		try:
			# read size of window
			self.resize(self.settings.value("windowSize", QtCore.QSize(1278, 768)))
			# read header size of dialogs
			headerSizesDict = self.settings.value('headerSizes', {})

			# set default header size of product list dialog
			productDialogHeaderSize = headerSizesDict.get('productDialogTableViewHeaderSizes')
			productDialogSizeInfo = SizeInfo(self.settings.value('productDialogSize', QtCore.QSize(1000, 600)),
											 productDialogHeaderSize)
			if productDialogSizeInfo.isValid():
				ProductListDialog.setSizeInfo(productDialogSizeInfo)

			# set default header size of old product list dialog
			oldProductDialogHeaderSize = headerSizesDict.get('oldProductDialogTableViewHeaderSizes')
			oldProductDialogSizeInfo = SizeInfo(self.settings.value('oldProductDialogSize', QtCore.QSize(800, 300)),
												oldProductDialogHeaderSize)
			if oldProductDialogSizeInfo.isValid():
				OldReceiptDialog.setSizeInfo(oldProductDialogSizeInfo)

			searchSoldProductHeaderSize = headerSizesDict.get('searchSoldProductHeaderSizes')
			searchSoldProductSizeInfo = SizeInfo(
					self.settings.value('searchSoldProductSizeInfo', QtCore.QSize(1024, 600)),
					searchSoldProductHeaderSize)
			if searchSoldProductSizeInfo.isValid():
				SearchSoldProductDialog.setSizeInfo(searchSoldProductSizeInfo)

			# set default header size of sold table view in main widget
			headerSizes = headerSizesDict.get('soldTableViewHeaderSizes', [])
			headerView = self.mainWidget.soldTableView.horizontalHeader()
			for i in range(len(headerSizes)):
				headerView.resizeSection(i, int(headerSizes[i]))

			breadCrumbDefaultNumber = self.settings.value('breadCrumbItemNumber', 3)
			self.mainWidget.breadCrumbWidget.setDefaultButtonSize(int(breadCrumbDefaultNumber))
			# read date information
			date_ = self.settings.value('date')
			if date_ is not None:
				self.__date = date.fromordinal(int(date_))
			else:
				self.__date = date.today()

			# read product model from its path
			json_ = self.settings.value('filePaths')

			if json_ is not None and isinstance(json_, dict):
				self.filePath().fromJson(json_)

			shortCutProductList = self.settings.value('shortCutProductList')
			if shortCutProductList is not None:
				shortcutItemDataListDict = json.loads(shortCutProductList)
				for itemDataDict in shortcutItemDataListDict:
					barcode = itemDataDict.get('barcode')
					if barcode is not None:
						product = self.mainWidget.productModel.getProductWithBarcode(barcode)
						itemData = ButtonItemData(itemDataDict.get('text'), product)
						self.mainWidget.buttonGroupWidget.addButton(itemData)

		except Exception as e:
			log.error(f'Setting file is not loaded properly while open the app. Exception is {e}')


	def writeSettings(self):
		headerSizes = {}
		sizes = []
		try:
			headerView = self.mainWidget.soldTableView.horizontalHeader()
			for i in range(headerView.count()):
				sizes.append(headerView.sectionSize(i))

			headerSizes['soldTableViewHeaderSizes'] = sizes

			self.settings.setValue('headerSizes', headerSizes)
			self.settings.setValue('windowSize', self.size())
			productListDialogSizeInfo = ProductListDialog.sizeInfo()
			if productListDialogSizeInfo is not None and productListDialogSizeInfo.isValid():
				self.settings.setValue('productDialogSize', productListDialogSizeInfo.size)
				headerSizes['productDialogTableViewHeaderSizes'] = productListDialogSizeInfo.headerSizes

			oldProductDialogSizeInfo = OldReceiptDialog.sizeInfo()
			if oldProductDialogSizeInfo is not None and oldProductDialogSizeInfo.isValid():
				self.settings.setValue('oldProductDialogSize', oldProductDialogSizeInfo.size)
				headerSizes['oldProductDialogTableViewHeaderSizes'] = oldProductDialogSizeInfo.headerSizes

			searchSoldProductSizeInfo = SearchSoldProductDialog.sizeInfo()
			if searchSoldProductSizeInfo is not None and searchSoldProductSizeInfo.isValid():
				self.settings.setValue('searchSoldProductSizeInfo', searchSoldProductSizeInfo.size)
				headerSizes['searchSoldProductHeaderSizes'] = searchSoldProductSizeInfo.headerSizes

			self.settings.setValue('headerSizes', headerSizes)
			self.settings.setValue('date', self.__date.toordinal())
			# save the product model before close app
			self.settings.setValue('filePaths', self.filePath().json())

			self.settings.setValue('breadCrumbItemNumber', self.mainWidget.breadCrumbWidget.count())

			shortcutItemDataList = self.mainWidget.buttonGroupWidget.itemDataList()
			shortcutItemDataListDict = list(
					map(lambda itemData: {'text': itemData.text, 'barcode': itemData.data.barcode()},
						shortcutItemDataList))

			self.settings.setValue('shortCutProductList', json.dumps(shortcutItemDataListDict))

		except Exception as e:
			log.error(f'Setting of app is not written properly on a disc. Exception is {e} ')


	def closeEvent(self, event):

		# check that there is a not empty model in bread crumb item data, if there is a non empty model, show a question
		breadCrumbItemCount = self.mainWidget.breadCrumbWidget.count()
		exists = False
		for i in range(breadCrumbItemCount):
			itemData = self.mainWidget.breadCrumbWidget.itemData(i)
			if itemData.model().isEmpty() is False:
				exists = True
				break

		# if there is non empty model in bread crumb item data, show a question about are you sure.
		if exists is True:
			action = QtWidgets.QMessageBox.question(self, 'Are you sure?', 'All products will be deleted',
													QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
			if action == QtWidgets.QMessageBox.No:
				event.ignore()
				return

		self.cleanupBeforeClose()
		super(MainWindow, self).closeEvent(event)


	def cleanupBeforeClose(self):
		self.writeSettings()


	def initSignalsAndSlots(self):
		self.mainWidget.printButton.clicked.connect(self.print)

	def print(self):
		pass

	def importCSVFile(self):
		filename, res = QtWidgets.QFileDialog.getOpenFileName(self, "Import CSV File",
															  self.filePath().path('importCsv', ''),
															  "CSV Files(*.csv)")
		try:
			if res and filename:
				res = self.__importCSVFile(filename)
				if res is True:
					self.filePath().setPath('importCsv', os.path.dirname(filename))
					self.__lastLoadPath = filename
					Toast.success('CSV Import',
								  'Importing CSV file is done successfully. Products are added to database')
				else:
					Toast.error('CSV Import', 'Invalid file CSV to import')
		except Exception as e:
			log.error(f'There is an error importing csv file. File is {filename}. error is {e}')
			Toast.error('CSV Import', 'Error occurred while importing CSV file')


	def exportCSVFile(self):
		filename, res = QtWidgets.QFileDialog.getSaveFileName(self, "Export CSV File",
															  self.filePath().path('exportCsv', ''),
															  "CSV Files(*.csv)")
		try:
			if res and filename:
				_, file_extension = os.path.splitext(filename)

				if file_extension != '.csv':
					filename = f'{filename}.csv'

				res = self.__exportCSVFile(filename)
				if res is True:
					self.filePath().setPath('exportCsv', os.path.dirname(filename))
					Toast.success('CSV Export', 'Exporting CSV file is done successfully')
				else:
					Toast.error('CSV Export', 'Invalid file CSV to export')
		except Exception as e:
			log.error(f'There is an error exporting csv file. File is {filename}. error is {e}')
			Toast.error('CSV Export', 'Error occurred while exporting CSV file')


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
				line = line.upper().replace('İ', 'I')
				line = line.replace('\n', '')
				if title:
					title = False
				else:
					productInList = line.split(',')
					if self.__checkRowValid(productInList):

						product = Product(ProductType.convertWeighableBarcode(productInList[1]),
										  productInList[3].strip(), float(productInList[9]),
										  float(productInList[5]),
										  float(productInList[11]),
										  int(productInList[-1]),
										  datetime.datetime.now(), )
						if product.barcode() not in productList:
							productList.setItem(product.barcode(), product)

			# add all products to database
			productListNotInModel = []
			for barcode in productList:
				product = self.mainWidget.productModel.getProductWithBarcode(barcode)
				if product is None:
					productListNotInModel.append(productList[barcode])
			if productListNotInModel:
				for product in productListNotInModel:
					self.databaseService().add(product)

				# commit all changes
				if self.databaseService().commit() is True:
					self.mainWidget.productModel.setProductList(self.__dataBaseToProductList())
			else:
				log.warning('No new item is added to product model')
		except Exception as e:
			log.error(f'Error occurred reading CSV file {filename}. Error is => {e}')
			return False

		return True


	def __checkRowValid(self, row):
		try:
			barcode = row[1].strip()
			if (barcode.isdigit() is False or
					barcode == 0 or
					barcode == '0' or
					len(row[3].strip()) == 0 or
					float(row[9]) < 0 or
					float(row[5]) < 0 or
					float(row[11]) < 0 or
					len(row[7].strip()) == 0 or
					int(row[-1]) < 0):
				return False
			else:
				return True
		except:
			return False


	def __exportCSVFile(self, filename):
		with open(filename, 'w') as file:
			try:
				headers = []
				for headerIndex in range(self.mainWidget.productModel.columnCount()):
					headers.append(self.mainWidget.productModel.headerData(headerIndex, QtCore.Qt.Horizontal))

				file.write(f'{",".join(headers)}\n')
				for i in range(self.mainWidget.productModel.rowCount()):
					data = []
					for j in range(self.mainWidget.productModel.columnCount()):
						index = self.mainWidget.productModel.index(i, j)
						data.append(str(index.data()))
					file.write(f'{",".join(data)}\n')
				return True
			except Exception as e:
				log.error(f'Error occurred reading CSV file {filename}. Error is => {e}')
				return False


	def __dataBaseToProductList(self):
		productDatabaseList = self.databaseService().query(Product).all()
		productDictList = DictList()
		for databaseProduct in productDatabaseList:
			product = Product.fromDatabase(databaseProduct)
			productDictList.setItem(product.barcode(), product)

		return productDictList

import os
from datetime import date
import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import log
from exceptions import InvalidProductModelException

from model.dictList import DictList
from model.sizeInfo import SizeInfo
from service.filePathService import FilePathService
from service.preferencesService import PreferencesService
from model.product import Product
from widget.dialog.oldReceiptDialog import OldReceiptDialog
from widget.dialog.productListDialog import ProductListDialog
from widget.mainWidget import MainWidget
from widget.toast import Toast


class MainWindow(QtWidgets.QMainWindow, PreferencesService, FilePathService):
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

			# set default header size of sold table view in main widget
			headerSizes = headerSizesDict.get('soldTableViewHeaderSizes', [])
			headerView = self.mainWidget.soldTableView.horizontalHeader()
			for i in range(len(headerSizes)):
				headerView.resizeSection(i, int(headerSizes[i]))

			# read daily sold product list from disk
			self.mainWidget.dailySoldProduct.read()

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
		except Exception as e:
			log.error(f'Setting file is not loaded properly while open the app. Exception is {e}')

		try:
			productModelPath = self.mainWidget.productModel.productModelFilePath()
			if productModelPath is not None and os.path.exists(productModelPath):
				self.mainWidget.productModel.load()
		except InvalidProductModelException as e:
			log.error(f'Product is not loaded successfully from file, because of model is invalid. Exception is {e}')
			Toast.error('Product Model Loading Error', 'Product model is not loaded successfully from its file')
		except Exception as e:
			log.error(f'Product model is not loaded from its path successfully. {e}')
			Toast.error('Product Model Loading Error', 'Product model is not loaded successfully from its file')


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

			self.settings.setValue('headerSizes', headerSizes)
			self.settings.setValue('date', self.__date.toordinal())
			# save the product model before close app
			self.settings.setValue('filePaths', self.filePath().json())

			self.mainWidget.dailySoldProduct.save()
		except Exception as e:
			log.error(f'Setting of app is not written properly on a disc. Exception is {e} ')

		try:
			self.mainWidget.productModel.save()
		except InvalidProductModelException as e:
			log.error(f'Product model is not saved successfully before app exit. Exception is {e}')
			QtWidgets.QMessageBox.information(None, 'Product Model Saved Error',
											  'Product model is not saved successfully before closing app')
		except Exception as e:
			log.error(f'Product model is not saved properly before app is closed. {e}')
			QtWidgets.QMessageBox.information(None, 'Product Model Saved Error',
											  'Product model is not saved successfully before closing app')


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
		self.mainWidget.exitButton.clicked.connect(self.close)


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
					Toast.success('CSV Import', 'Importing CSV file is done successfully')
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
				if title:
					title = False
				else:
					productInList = line.split(',')

					product = Product(productInList[1], productInList[3].strip(), float(productInList[9]),
									  float(productInList[5]),
									  float(productInList[11]),
									  productInList[7], int(productInList[-1]))
					if product.id() not in productList:
						productList.setItem(product.id(), product)

			self.mainWidget.productModel.setProductList(productList)
		except Exception as e:
			log.error(f'Error occurred reading CSV file {filename}. Error is => {e}')
			return False

		return True


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

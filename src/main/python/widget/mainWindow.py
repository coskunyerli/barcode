import os
from datetime import date
import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import log

from model.dictList import DictList
from model.preferences import PreferencesObject
from model.product import Product
from widget.mainWidget import MainWidget
from widget.toast import Toast


class MainWindow(QtWidgets.QMainWindow, PreferencesObject):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		menubar = self.menuBar()
		menu = QtWidgets.QMenu('File')
		self.importCsvAction = menu.addAction('Import CSV')
		self.exportCsvAction = menu.addAction('Export CSV')
		menubar.addMenu(menu)
		self.importCsvAction.triggered.connect(self.importCSVFile)
		self.exportCsvAction.triggered.connect(self.exportCSVFile)

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

		date_ = self.settings.value('date')
		if date_ is not None:
			self.__date = date.fromordinal(int(date_))
		else:
			self.__date = date.today()

		# read product model from its path
		try:
			productModelPath = self.mainWidget.productModel.productModelFilePath()
			if productModelPath is not None and os.path.exists(productModelPath):
				self.mainWidget.productModel.load()
		except Exception as e:
			log.error(f'Product model is not loaded from its path successfully. {e}')
			Toast.error('Product Model Loading Error', 'Product model is not loaded successfully from its file')


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

		# save the product model before close app
		try:
			self.mainWidget.productModel.save()
		except Exception as e:
			log.error(f'Product model is not saved properly before app is closed. {e}')
			QtWidgets.QMessageBox.information(None, 'Product Model Saved Error',
											  'Product model is not saved successfully before closing app')


	def closeEvent(self, event):
		self.cleanupBeforeClose()
		super(MainWindow, self).closeEvent(event)


	def cleanupBeforeClose(self):
		self.writeSettings()


	def initSignalsAndSlots(self):
		self.mainWidget.exitButton.clicked.connect(self.close)


	def importCSVFile(self):
		filename, res = QtWidgets.QFileDialog.getOpenFileName(self, "Import CSV File",
															  self.preferences().node('filePath').get('importCSV', ''),
															  "CSV Files(*.csv)")
		try:
			if res and filename:
				res = self.__importCSVFile(filename)
				self.preferences().setNode('filePath')['importCsv'] = filename
				if res is True:
					self.__lastLoadPath = filename
					Toast.success('CSV Import', 'Importing CSV file is done successfully')
				else:
					Toast.error('CSV Import', 'Invalid file CSV to import')
		except Exception as e:
			log.error(f'There is an error importing csv file. File is {filename}. error is {e}')
			Toast.error('CSV Import', 'Error occurred while importing CSV file')


	def exportCSVFile(self):
		filename, res = QtWidgets.QFileDialog.getSaveFileName(self, "Export CSV File", '',
															  "CSV Files(*.csv)")
		try:
			if res and filename:
				_, file_extension = os.path.splitext(filename)

				if file_extension != '.csv':
					filename = f'{filename}.csv'

				res = self.__exportCSVFile(filename)
				if res is True:
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

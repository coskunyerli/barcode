import os
import PySide2.QtCore as QtCore
import log
from enums import ProductType

from model.dictList import DictList
from model.product import Product


class ProductModel(QtCore.QAbstractTableModel):
	modificationChanged = QtCore.Signal(bool)


	def __init__(self, path = None):
		super(ProductModel, self).__init__()
		self.__isModified = False
		self.__path = path
		self.__isSavedEveryUpdate = False
		self.__filename = '.product.lst'
		self.__productList = DictList()
		self.__headerData = ['Barcode', 'Name', 'Price', 'Purchase Price', 'Second Price', 'Kind', 'Value Added Tax']


	def isModified(self):
		return self.__isModified


	def setModified(self, result):
		if self.isModified() != result:
			self.__isModified = result
			self.modificationChanged.emit(self.isModified())


	def isSavedEveryUpdate(self):
		return self.__isSavedEveryUpdate


	def setSavedEveryUpdate(self, res):
		self.__isSavedEveryUpdate = res


	def path(self):
		return self.__path


	def productModelFilePath(self):
		return os.path.join(self.path(), self.__filename)


	def setPath(self, path):
		self.__path = path


	def addProduct(self, product):
		self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
		localBarcode = self.__barcode(product.id())
		localProduct = product.copy()
		localProduct.setID(localBarcode)
		self.__productList.setItem(localBarcode, localProduct)
		self.endInsertRows()


	def removeProductWithBarcode(self, barcodeList):
		if barcodeList:
			for barcode in barcodeList:
				firstIndex = self.__productList.index(barcode)
				self.beginRemoveRows(QtCore.QModelIndex(), firstIndex, firstIndex)
				self.__productList.delete(barcode)
				self.endRemoveRows()


	def columnCount(self, index = QtCore.QModelIndex()):
		return len(self.__headerData)


	def productType(self, barcode):
		return ProductType.productType(barcode)


	def __barcode(self, barcode):
		return ProductType.convertWeighableBarcode(barcode)


	def getProductWithBarcode(self, barcode):
		localBarcode = self.__barcode(barcode)
		return self.__productList[localBarcode]


	def rowCount(self, index = QtCore.QModelIndex()):
		return len(self.__productList)


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		if role == QtCore.Qt.DisplayRole:
			product = self.__productList[index.row()]
			data = [product.id(), product.name(), product.sellingPrice(), product.purchasePrice(),
					product.secondSellingPrice(), product.kind(),
					product.valueAddedTax()]
			return data[index.column()]
		elif role == QtCore.Qt.UserRole:
			return self.__productList[index.row()]


	def getIndexWithBarcode(self, barcode):
		# convert local barcode
		barcode = self.__barcode(barcode)

		if barcode in self.__productList:
			index = self.__productList.index(barcode)
			return self.index(index, 0)
		else:
			return QtCore.QModelIndex()


	def setData(self, index, func, role = QtCore.Qt.EditRole):
		if index.isValid() is False:
			return False
		item = self.data(index, QtCore.Qt.UserRole)
		if func(item) is True:
			self.dataChanged.emit(index, index)
			return True
		return False


	def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
		if orientation == QtCore.Qt.Horizontal:
			if role == QtCore.Qt.DisplayRole:
				return self.__headerData[section]
		elif orientation == QtCore.Qt.Vertical:
			if role == QtCore.Qt.DisplayRole:
				return section + 1


	def setProductList(self, list_):
		self.beginResetModel()
		self.__productList = list_
		self.setModified(True)
		self.endResetModel()




	def json(self):
		json_ = []
		for key in self.__productList:
			product = self.__productList[key]
			json_.append(product.dict())

		return json_


	@classmethod
	def fromJson(cls, json_):
		productList = DictList()
		productInDict = None
		try:
			for productInDict in json_:
				product = Product.fromDict(productInDict)
				productList.setItem(product.id(), product)

			return productList
		except Exception as e:
			log.error(f'Model is not created successfully from dict data. Data is {productInDict}. {e}')
			return None

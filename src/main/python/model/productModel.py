import os
import PySide2.QtCore as QtCore
from enums import ProductType

from model.dictList import DictList


class ProductModel(QtCore.QAbstractTableModel):
	modificationChanged = QtCore.Signal(bool)


	def __init__(self, path = None):
		super(ProductModel, self).__init__()
		self.__isModified = False
		self.__isSavedEveryUpdate = False
		self.__productList = DictList()
		self.__headerData = ['Barcode', 'Name', 'Price', 'Purchase Price', 'Second Price', 'Value Added Tax',
							 'Created Date']


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


	def addProduct(self, product):
		self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
		localBarcode = self.__barcode(product.barcode)
		localProduct = product.copy()
		localProduct.setBarcode(localBarcode)
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
			data = [str(product.barcode()), product.name(), str(product.sellingPrice()), str(product.purchasePrice()),
					str(product.secondSellingPrice()),
					str(product.valueAddedTax()), product.createdDate().strftime("%H:%M:%S - %d/%m/%Y")]
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


	def importProduct(self, productList):
		self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount() + len(productList))
		for product in productList:
			localBarcode = self.__barcode(product.barcode())
			localProduct = product.copy()
			localProduct.setBarcode(localBarcode)
			self.__productList.setItem(localBarcode, localProduct)
		self.endInsertRows()

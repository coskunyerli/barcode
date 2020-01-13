import json
import os

import PySide2.QtCore as QtCore
import log

from model.dictList import DictList
from model.product import Product


class ProductModel(QtCore.QAbstractTableModel):

	def __init__(self, path = None):
		super(ProductModel, self).__init__()
		self.__path = path
		self.__isSavedEveryUpdate = False
		self.__filename = '.product.lst'
		self.__productList = DictList()
		self.__headerData = ['Barcode', 'Name', 'Price', 'Purchase Price', 'Kind', 'Value Added Tax', 'Sale Amount']


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
		self.__productList.setItem(product.id(), product)
		self.endInsertRows()
		if self.isSavedEveryUpdate():
			self.save()


	def removeProduct(self, index):
		# todo buradn silince bütün yerlerden de silmek lazım
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		self.__productList.pop(index.row())
		self.endRemoveRows()
		if self.isSavedEveryUpdate():
			self.save()


	def columnCount(self, index = QtCore.QModelIndex()):
		return len(self.__headerData)


	def getData(self, id):
		return self.__productList[id]


	def rowCount(self, index = QtCore.QModelIndex()):
		return len(self.__productList)


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		if role == QtCore.Qt.DisplayRole:
			product = self.__productList[index.row()]
			data = [product.id(), product.name(), product.sellingPrice(), product.purchasePrice(), product.kind(),
					product.valueAddedTax(), product.saleAmount()]
			return data[index.column()]
		elif role == QtCore.Qt.UserRole:
			return self.__productList[index.row()]


	def getIndex(self, barcode):
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
			if self.isSavedEveryUpdate():
				self.save()
			return True
		return False


	def headerData(self, section, orientation, role):
		if orientation == QtCore.Qt.Horizontal:
			if role == QtCore.Qt.DisplayRole:
				return self.__headerData[section]
		elif orientation == QtCore.Qt.Vertical:
			if role == QtCore.Qt.DisplayRole:
				return section + 1


	def setProductList(self, list):
		self.beginResetModel()
		self.__productList = list
		self.endResetModel()


	def json(self):
		json_ = []
		for key in self.__productList:
			product = self.__productList[key]
			json_.append(product.dict())

		return json_


	def save(self):
		if self.path() is not None:
			try:
				with open(os.path.join(self.path(), self.__filename), 'w') as file:
					file.write(json.dumps(self.json()))
			except Exception as e:
				raise Exception(f'Product model is not saved into file. path is {self.path()}. {e}')
		else:
			raise Exception('There is not path to save it')


	def load(self):
		if self.path() is None:
			raise Exception('There is no path to load')
		else:
			try:
				with open(os.path.join(self.path(), self.__filename)) as file:
					modelInDict = json.loads(file.read())
					list_ = ProductModel.fromJson(modelInDict)
					self.setProductList(list_)
			except Exception as e:
				raise Exception(f'Product model is not loaded from file. path is {self.path()}. {e}')


	@classmethod
	def fromJson(cls, json_):
		productList = DictList()
		try:
			for productInDict in json_:
				product = Product.fromDict(productInDict)
				productList.setItem(product.id(), product)

			return productList
		except Exception as e:
			log.error(f'Model is not created successfully from dict data. Data is {json_}. {e}')
			return None

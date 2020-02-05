import json
import os

import PySide2.QtCore as QtCore
import log
from enums import ProductType

from model.dictList import DictList
from model.product import Product


class ProductModel(QtCore.QAbstractTableModel):

	def __init__(self, path=None):
		super(ProductModel, self).__init__()
		self.__path = path
		self.__isSavedEveryUpdate = False
		self.__filename = '.product.lst'
		self.__productList = DictList()
		self.__headerData = ['Barcode', 'Name', 'Price', 'Purchase Price', 'Second Price', 'Kind', 'Value Added Tax']


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
		if self.isSavedEveryUpdate():
			self.save()


	def removeProduct(self, index):
		# todo buradn silince bütün yerlerden de silmek lazım
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		self.__productList.pop(index.row())
		self.endRemoveRows()
		if self.isSavedEveryUpdate():
			self.save()


	def columnCount(self, index=QtCore.QModelIndex()):
		return len(self.__headerData)


	def productType(self, id):
		if id[0:2] == '27':
			return ProductType.WEIGHABLE
		else:
			return ProductType.REGULAR


	def __barcode(self, barcode):
		# convert barcode to local value
		if self.productType(barcode) == ProductType.WEIGHABLE:
			return ProductType.convertWeighableBarcode(barcode)
		else:
			return barcode


	def getProductWithBarcode(self, barcode):
		localBarcode = self.__barcode(barcode)

		return self.__productList[localBarcode]


	def rowCount(self, index=QtCore.QModelIndex()):
		return len(self.__productList)


	def data(self, index, role=QtCore.Qt.DisplayRole):
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


	def setData(self, index, func, role=QtCore.Qt.EditRole):
		if index.isValid() is False:
			return False
		item = self.data(index, QtCore.Qt.UserRole)
		if func(item) is True:
			self.dataChanged.emit(index, index)
			if self.isSavedEveryUpdate():
				self.save()
			return True
		return False


	def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
		if orientation == QtCore.Qt.Horizontal:
			if role == QtCore.Qt.DisplayRole:
				return self.__headerData[section]
		elif orientation == QtCore.Qt.Vertical:
			if role == QtCore.Qt.DisplayRole:
				return section + 1


	def setProductList(self, list):
		self.beginResetModel()
		self.__productList = self.__preProcessBeforeSetList(list)
		self.endResetModel()


	def __preProcessBeforeSetList(self, productList):
		localProductList = []
		for product in productList:
			localProduct = product.copy()
			localProduct.setID(self.__barcode(product.id()))
			localProductList.append(localProduct)
		return localProductList


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
			with open(os.path.join(self.path(), self.__filename)) as file:
				modelInDict = json.loads(file.read())
				list_ = ProductModel.fromJson(modelInDict)
				if list_ is not None:
					self.setProductList(list_)
				else:
					raise Exception(f'Product model is not loaded from file. path is {self.path()}.')


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

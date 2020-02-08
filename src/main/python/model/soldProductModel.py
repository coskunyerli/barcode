import datetime
import PySide2.QtCore as QtCore

import static
from model.dictList import DictList
from model.soldProduct import SoldProduct


class SoldProductModel(QtCore.QAbstractTableModel):
	totalPriceChanged = QtCore.Signal(float)


	def __init__(self, productModel = None):
		super(SoldProductModel, self).__init__()
		self.__productList = []
		self.__headerData = ['Barcode', 'Name', 'Amount', 'Price', 'Total Price']
		self.__date = datetime.datetime.now()
		self.__readOnly = False
		self.__productModel = productModel
		if self.__productModel is not None:
			self.__productModel.dataChanged.connect(self.__updateProductItems)


	def __updateProductItems(self, left, right):
		if self.__productModel is not None:
			changedProduct = left.data(QtCore.Qt.UserRole)
			soldProduct = static.first_(lambda sProduct: sProduct.id() == changedProduct.id(),
										self.__productList)
			if soldProduct is not None:
				soldProduct.setProduct(changedProduct.copy())
			self.totalPriceChanged.emit(self.totalPrice())
			self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())


	def setReadOnly(self, res):
		self.__readOnly = res


	def date(self):
		return self.__date


	def setProducList(self, productList):
		self.beginResetModel()
		self.__productList = productList
		self.endResetModel()


	def addProduct(self, product, distinct = False):
		if distinct is False:
			currentProduct = self.product(product.id())
			if currentProduct is not None:
				currentProduct.setAmount(currentProduct.amount() + product.amount())
				index = self.__productList.index(currentProduct)
				self.dataChanged.emit(index, index)
				self.totalPriceChanged.emit(self.totalPrice())
				return

		self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
		self.__productList.append(product)
		self.endInsertRows()
		self.totalPriceChanged.emit(self.totalPrice())


	def flags(self, index):
		if index.column() == 2 and self.__readOnly is False:
			return super(SoldProductModel, self).flags(index) | QtCore.Qt.ItemIsEditable
		else:
			return super(SoldProductModel, self).flags(index)


	def setData(self, index, data, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			if index.column() == 2 and data.isdigit():
				amount = int(data)
				if amount == 0:
					return False
				soldProduct = self.__productList[index.row()]
				soldProduct.setAmount(int(data))
				self.totalPriceChanged.emit(self.totalPrice())
				self.dataChanged.emit(index, index)
				return True
		return False


	def removeProduct(self, id):
		if id in self.__productList:
			index = self.__productList.keys().index(id)
			self.beginRemoveRows(QtCore.QModelIndex(), index, index)
			if id in self.__productList:
				del self.__productList[id]
			self.endRemoveRows()
		self.totalPriceChanged.emit(self.totalPrice())


	def pop(self, index):
		self.beginRemoveRows(QtCore.QModelIndex(), index, index)
		self.__productList.pop(index)
		self.endRemoveRows()
		self.totalPriceChanged.emit(self.totalPrice())


	def columnCount(self, index = QtCore.QModelIndex()):
		return len(self.__headerData)


	def rowCount(self, index = QtCore.QModelIndex()):
		return len(self.__productList)


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		if role == QtCore.Qt.DisplayRole:
			soldProduct = self.__productList[index.row()]
			data = [soldProduct.id(), soldProduct.name(), f'{soldProduct.amount()} {soldProduct.unit()}',
					f'{soldProduct.price()} ₺',
					f'{soldProduct.totalPrice()} ₺']
			return data[index.column()]
		elif role == QtCore.Qt.UserRole:
			return self.__productList[index.row()]
		elif role == QtCore.Qt.TextAlignmentRole:
			if index.column() == 2 or index.column() == 3 or index.column() == 4:
				return QtCore.Qt.AlignCenter
			else:
				return QtCore.Qt.AlignVCenter


	def headerData(self, section, orientation, role):
		if orientation == QtCore.Qt.Horizontal:
			if role == QtCore.Qt.DisplayRole:
				return self.__headerData[section]
		elif orientation == QtCore.Qt.Vertical:
			if role == QtCore.Qt.DisplayRole:
				return section + 1


	def clear(self):
		self.beginResetModel()
		self.__productList = []
		self.totalPriceChanged.emit(0)
		self.endResetModel()


	def totalPrice(self):
		totalPrice = 0.0
		for soldProduct in self.__productList:
			totalPrice += soldProduct.totalPrice()
		return totalPrice


	def product(self, id):
		product = static.first_(lambda p: p.id() == id, self.__productList)
		return product


	def productList(self):
		return self.__productList.copy()


	def dict(self):
		return {'date': self.__date.timestamp(), 'list': list(map(lambda item: item.dict(), self.__productList)),
				'totalPrice': self.totalPrice()}


	def copy(self):
		model = SoldProductModel()
		model.__productList = self.__productList
		model.__date = self.__date
		return model


	@classmethod
	def fromDict(cls, dict):
		model = SoldProductModel()

		productListInDict = dict.get('list', [])
		dateInTimeStamp = dict.get('date', datetime.datetime.now().timestamp())

		model.__productList = list(map(lambda itemInDict: SoldProduct.fromDict(itemInDict), productListInDict))
		model.__date = datetime.datetime.fromtimestamp(dateInTimeStamp)
		return model

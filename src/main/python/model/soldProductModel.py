import datetime
import PySide2.QtCore as QtCore

import static
from model.order import Order


class SoldProductModel(QtCore.QAbstractTableModel):
	totalPriceChanged = QtCore.Signal(float)


	def __init__(self, productModel = None):
		super(SoldProductModel, self).__init__()
		self.__order = None
		self.__headerData = ['Barcode', 'Name', 'Amount', 'Price', 'Total Price']
		self.__readOnly = False
		self.__productModel = productModel
		if self.__productModel is not None:
			self.__productModel.dataChanged.connect(self.__updateProductItems)
			self.__productModel.rowsAboutToBeRemoved.connect(self.__updateProductItemList)


	@property
	def __productListInOrder(self):
		return self.order().productList()


	def __updateProductItemList(self, parent, first, last):
		if self.__productModel is not None:
			removedProductIndex = self.__productModel.index(first, 0, parent)
			removedProduct = removedProductIndex.data(QtCore.Qt.UserRole)
			soldProduct = static.first_(lambda sProduct: sProduct.barcode() == removedProduct.barcode(),
										self.__productListInOrder)

			if soldProduct is not None:
				index = self.__productListInOrder.index(soldProduct)
				self.pop(index)


	def __updateProductItems(self, left, right):
		if self.__productModel is not None:
			changedProduct = left.data(QtCore.Qt.UserRole)
			soldProduct = static.first_(lambda sProduct: sProduct.barcode() == changedProduct.barcode(),
										self.__productListInOrder)
			if soldProduct is not None:
				soldProduct.setProduct(changedProduct.copy())
			self.totalPriceChanged.emit(self.totalPrice())
			self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())


	def setReadOnly(self, res):
		self.__readOnly = res


	def setOrder(self, order):
		self.beginResetModel()
		self.__order = order
		self.endResetModel()


	def order(self):
		return self.__order


	def date(self):
		return self.order().createdDate()


	def setProducList(self, productList):
		self.beginResetModel()
		self.__productList = productList
		self.endResetModel()


	def addProduct(self, soldProduct, distinct = False):
		if distinct is False:
			currentProduct = self.product(soldProduct.barcode())
			if currentProduct is not None:
				currentProduct.setAmount(currentProduct.amount() + soldProduct.amount())
				index = self.__productListInOrder.index(currentProduct)
				self.dataChanged.emit(index, index)
				self.totalPriceChanged.emit(self.totalPrice())
				return

		self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
		self.__productListInOrder.append(soldProduct)
		soldProduct.setOrder(self.order())
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
				soldProduct = self.__productListInOrder[index.row()]
				soldProduct.setAmount(int(data))
				self.totalPriceChanged.emit(self.totalPrice())
				self.dataChanged.emit(index, index)
				return True
		return False


	def removeProduct(self, id):
		if id in self.__productListInOrder:
			index = self.__productListInOrder.keys().index(id)
			self.beginRemoveRows(QtCore.QModelIndex(), index, index)
			if id in self.__productListInOrder:
				del self.__productListInOrder[id]
			self.endRemoveRows()
		self.totalPriceChanged.emit(self.totalPrice())


	def pop(self, index):
		self.beginRemoveRows(QtCore.QModelIndex(), index, index)
		self.__productListInOrder.pop(index)
		self.endRemoveRows()
		self.totalPriceChanged.emit(self.totalPrice())


	def columnCount(self, index = QtCore.QModelIndex()):
		return len(self.__headerData)


	def rowCount(self, index = QtCore.QModelIndex()):
		return len(self.__productListInOrder)


	def isEmpty(self):
		return self.rowCount() <= 0


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		if role == QtCore.Qt.DisplayRole:
			soldProduct = self.__productListInOrder[index.row()]
			data = [soldProduct.barcode(), soldProduct.name(), f'{soldProduct.amount()} {soldProduct.unit()}',
					f'{soldProduct.price()} ₺',
					f'{soldProduct.totalPrice()} ₺']
			return data[index.column()]
		elif role == QtCore.Qt.UserRole:
			return self.__productListInOrder[index.row()]
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
		self.order().clearUncommitProductList()
		self.totalPriceChanged.emit(0)
		self.endResetModel()


	def totalPrice(self):
		totalPrice = 0.0
		for soldProduct in self.__productListInOrder:
			totalPrice += soldProduct.totalPrice()
		return totalPrice


	def product(self, barcode):
		product = static.first_(lambda p: p.barcode() == barcode, self.__productListInOrder)
		return product


	def productList(self):
		return self.__productListInOrder.copy()

import PySide2.QtCore as QtCore


class OrderModel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		super(OrderModel, self).__init__(parent)
		self.__orderList = []


	def setOrderList(self, orderList):
		self.beginResetModel()
		self.__orderList = orderList
		self.endResetModel()


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		if role == QtCore.Qt.DisplayRole:
			order = self.__orderList[index.row()]
			return order.id()
		elif role == QtCore.Qt.UserRole:
			order = self.__orderList[index.row()]
			return order


	def rowCount(self, parent = QtCore.QModelIndex()):

		return len(self.__orderList)

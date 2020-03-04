from model.db.databaseConnectInterface import DatabaseConnector
from model.db.databaseOrder import DatabaseOrder
from model.soldProduct import SoldProduct

class Order(DatabaseConnector):
	def __init__(self, createdDate):
		self.__id = None
		self.__soldProductList = []
		self.__createdDate = createdDate
		self.__unCommitSoldProductList = []
		self.__databaseObject = None


	def toDatabase(self):
		if self.__databaseObject is None:
			orderDatabaseObject = DatabaseOrder(created_date = self.createdDate())
			self.__databaseObject = orderDatabaseObject
		return self.__databaseObject


	@classmethod
	def fromDatabase(cls, databaseObject):
		order = Order(databaseObject.created_date)
		order.__id = databaseObject.id
		order.__databaseObject = databaseObject
		return order


	@classmethod
	def getClass(cls):
		return DatabaseOrder


	def createdDate(self):
		return self.__createdDate


	def id(self):
		return self.__id


	@property
	def committedProductList(self):
		soldProductList = list(map(lambda soldProductDatabase: SoldProduct.fromDatabase(soldProductDatabase),
								   self.__databaseObject.soldProducts))
		return soldProductList


	def uncommittedProductList(self):
		return self.__unCommitSoldProductList


	def productList(self):
		if self.__databaseObject is not None:
			return self.uncommittedProductList() + self.committedProductList
		else:
			return self.uncommittedProductList()


	def addProduct(self, soldProduct):
		self.__unCommitSoldProductList.append(soldProduct)


	def clearUncommitProductList(self):
		self.__unCommitSoldProductList.clear()


	def __str__(self):
		return f'Order({self.id()}, {self.createdDate()})'

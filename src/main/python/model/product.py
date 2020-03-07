from model.db.databaseConnectInterface import DatabaseConnector
from model.db.databaseProduct import DatabaseProduct


class Product(DatabaseConnector):
	def __init__(self, barcode, name, purchasePrice, sellingPrice, secondSellingPrice, vat, createdDate):
		self.__barcode = barcode
		self.__name = name
		self.__purchasePrice = purchasePrice
		self.__sellingPrice = sellingPrice
		self.__secondSellingPrice = secondSellingPrice
		self.__vat = vat
		self.__createdDate = createdDate

		self.__databaseObject = None


	# self.__stockLevel = stockLevel
	# self.__stockType = stockType

	def toDatabase(self):
		if self.__databaseObject is None:
			databaseProduct = DatabaseProduct(barcode = int(self.barcode()), name = self.name(),
											  purchasePrice = self.purchasePrice(),
											  sellingPrice = self.sellingPrice(),
											  secondSellingPrice = self.secondSellingPrice(),
											  vat = self.valueAddedTax(),
											  createdDate = self.createdDate())
			self.__databaseObject = databaseProduct
		return self.__databaseObject


	@classmethod
	def fromDatabase(self, databaseObject):
		product = Product(str(databaseObject.barcode), databaseObject.name, databaseObject.purchasePrice,
						  databaseObject.sellingPrice, databaseObject.secondSellingPrice, databaseObject.vat,
						  databaseObject.createdDate)
		product.__databaseObject = databaseObject
		return product


	@classmethod
	def getClass(cls):
		return DatabaseProduct


	def copy(self):
		return Product(self.barcode(), self.name(), self.purchasePrice(), self.sellingPrice(),
					   self.secondSellingPrice(), self.valueAddedTax(), self.createdDate())


	def __repr__(self):
		return self.__str__()


	def __str__(self):
		return 'Product(%s,%s,%s,%s,%s,%s)' % (
			self.barcode(), self.name(), self.purchasePrice(), self.sellingPrice(), self.valueAddedTax(),
			self.createdDate())


	def createdDate(self):
		return self.__createdDate


	def setCreatedDate(self, kind):
		if self.__createdDate != kind:
			self.__createdDate = kind
			return True
		else:
			return False


	def sellingPrice(self):
		return self.__sellingPrice


	def secondSellingPrice(self):
		return self.__secondSellingPrice


	def purchasePrice(self):
		return self.__purchasePrice


	def setSellingPrice(self, price):
		if self.__sellingPrice != price:
			self.__sellingPrice = price
			return True
		else:
			return False


	def setSecondSellingPrice(self, price):
		self.__secondSellingPrice = price


	def setPurchasePrice(self, price):
		if self.__purchasePrice != price:
			self.__purchasePrice = price
			return True
		else:
			return False


	def setName(self, name):
		if self.__name != name:
			self.__name = name
			return True
		else:
			return False


	def setBarcode(self, id):
		if self.__barcode != id:
			self.__barcode = id
			return True
		else:
			return False


	def barcode(self):
		return self.__barcode


	def name(self):
		return self.__name


	def valueAddedTax(self):
		return self.__vat


	def setValueAddedTax(self, tax):
		if self.__vat != tax:
			self.__vat = tax
			return True
		else:
			return False


	def profit(self):
		return (self.sellingPrice() - self.purchasePrice())


	def profitRate(self):
		return self.profit() / self.purchasePrice() * 100


class CustomProduct(Product):
	def __init__(self, price):
		super(CustomProduct, self).__init__('0', 'Unknown Product', price, price, price, 'Any', 18)

import datetime

from model.db.databaseConnectInterface import DatabaseConnector
from model.db.databaseSoldProduct import DatabaseSoldProduct
from model.product import Product


class SoldProduct(DatabaseConnector):
	def __init__(self, product, amount):
		self.__id = None
		self.__product = product
		self.__amount = amount
		self.__date = datetime.datetime.now()
		self.__unit = 'pcs'

		self.__databaseObject = None

		self.__order = None


	def toDatabase(self):
		if self.__databaseObject is None:
			params = {'amount': self.amount(), 'unit': self.unit(), 'product_barcode': self.barcode(),
					  'product_name': self.name(), 'product_purchasePrice': self.__product.purchasePrice(),
					  'product_sellingPrice': self.__product.sellingPrice(),
					  'product_secondSellingPrice': self.__product.secondSellingPrice(),
					  'product_createdDate': self.__product.createdDate(),
					  'product_vat': self.__product.valueAddedTax()}
			if self.id() is not None:
				params['id'] = self.id()
			if self.order() is not None:
				params['order'] = self.order().toDatabase()
			databaseObject = DatabaseSoldProduct(**params)
			self.__databaseObject = databaseObject
		return self.__databaseObject


	@classmethod
	def fromDatabase(cls, db):
		product = Product(db.product_barcode, db.product_name, db.product_purchasePrice, db.product_sellingPrice,
						  db.product_secondSellingPrice, db.product_vat, db.product_createdDate)
		soldProduct = SoldProduct(db.id, db.amount)
		soldProduct.setUnit(db.unit)
		soldProduct.__product = product
		soldProduct.__databaseObject = db
		return soldProduct


	@classmethod
	def getClass(cls):
		return DatabaseSoldProduct


	def setOrder(self, order):
		self.__order = order


	def order(self):
		return self.__order


	def unit(self):
		return self.__unit


	def setUnit(self, unit):
		self.__unit = unit


	def setProduct(self, product):
		self.__product = product


	def id(self):
		return self.__id


	def barcode(self):
		return self.__product.barcode()


	def name(self):
		return self.__product.name()


	def sellingPrice(self):
		return self.__product.sellingPrice()


	def amount(self):
		return self.__amount


	def setAmount(self, amount):
		self.__amount = amount


	def totalPrice(self):
		return float(self.sellingPrice()) * self.amount()


	def price(self):
		return self.__product.sellingPrice()


	def __eq__(self, other):
		if self.id() == other.id():
			return True
		else:
			return False


	def __str__(self):
		return f'SoldProduct({self.id(), self.__product, self.amount(), self.unit(), self.order()})'


class WeighableSoldProduct(SoldProduct):

	def __init__(self, product, amount):
		super(WeighableSoldProduct, self).__init__(product, amount)
		self.setUnit('gr')


	def totalPrice(self):
		totalPrice = super(WeighableSoldProduct, self).totalPrice()
		return round(totalPrice / 1000.0, 2)


	@classmethod
	def amountFromBarcode(cls, barcode):
		amountInString = barcode[-5:-1]
		if amountInString.isdigit():
			amount = int(amountInString)
		else:
			amount = 1
		return amount


if __name__ == '__main__':
	a = '2700067005670'
	print(WeighableSoldProduct.amount(a))

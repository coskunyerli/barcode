import datetime

from model.product import Product


class SoldProduct(object):
	def __init__(self, product, amount):
		self.__product = product
		self.__amount = amount
		self.__date = datetime.datetime.now()
		self.__unit = 'pcs'


	def unit(self):
		return self.__unit


	def setUnit(self, unit):
		self.__unit = unit


	def setProduct(self, product):
		self.__product = product


	def id(self):
		return self.__product.id()


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


	def dict(self):
		return {'product': self.__product.dict(), 'amount': self.amount(), 'date': self.__date.timestamp()}


	@classmethod
	def fromDict(self, dict):
		product = Product.fromDict(dict['product'])
		soldProduct = SoldProduct(product, dict['amount'])
		soldProduct.__date = datetime.datetime.fromtimestamp(dict['date'])
		return soldProduct


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

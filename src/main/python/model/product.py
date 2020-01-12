class Product(object):
	def __init__(self, id, name, purchasePrice, sellingPrice, kind, vat):
		self.__id = id
		self.__name = name
		self.__purchasePrice = purchasePrice
		self.__sellingPrice = sellingPrice
		self.__kind = kind
		self.__vat = vat
		self.__saleAmount = 0


	def dict(self):
		return {'id': self.id(), 'name': self.name(), 'purchasePrice': self.purchasePrice(),
				'sellingPrice': self.sellingPrice(), 'kind': self.kind(), 'vat': self.valueAddedTax()}


	@classmethod
	def fromDict(cls, dict):
		try:
			product = Product(**dict)
			return product
		except Exception as e:
			raise Exception(f'Product is not created successfully {dict} is not valid. {e}')


	def __repr__(self):
		return self.__str__()


	def __str__(self):
		return 'Product(%s,%s,%s,%s,%s,%s %s)' % (
			self.id(), self.name(), self.purchasePrice(), self.sellingPrice(), self.kind(), self.valueAddedTax(),
			self.saleAmount())


	# self.__stockLevel = stockLevel
	# self.__stockType = stockType

	def kind(self):
		return self.__kind


	def setKind(self, kind):
		if self.__kind != kind:
			self.__kind = kind
			return True
		else:
			return False


	def sellingPrice(self):
		return self.__sellingPrice


	def purchasePrice(self):
		return self.__purchasePrice


	def setSellingPrice(self, price):
		if self.__sellingPrice != price:
			self.__sellingPrice = price
			return True
		else:
			return False


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


	def setID(self, id):
		if self.__id != id:
			self.__id = id
			return True
		else:
			return False


	def setSaleAmount(self, value):
		if self.__saleAmount != value:
			self.__saleAmount = value
			return True
		else:
			return False


	def saleAmount(self):
		return self.__saleAmount


	def id(self):
		return self.__id


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
		super(CustomProduct, self).__init__('0', 'Unknown Product', price, price, None, 18)

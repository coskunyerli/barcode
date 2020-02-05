class Product(object):
	def __init__(self, id, name, purchasePrice, sellingPrice, secondSellingPrice, kind, vat):
		self.__id = id
		self.__name = name
		self.__purchasePrice = purchasePrice
		self.__sellingPrice = sellingPrice
		self.__secondSellingPrice = secondSellingPrice
		self.__kind = kind
		self.__vat = vat

	def dict(self):
		return {'id': self.id(), 'name': self.name(), 'purchasePrice': self.purchasePrice(),
				'sellingPrice': self.sellingPrice(), 'secondSellingPrice': self.secondSellingPrice(),
				'kind': self.kind(), 'vat': self.valueAddedTax()}


	@classmethod
	def fromDict(cls, dict):

		id_ = dict.get('id')
		name = dict.get('name')
		purchasePrice = dict.get('purchasePrice')
		sellingPrice = dict.get('purchasePrice')
		secondSellingPrice = dict.get('secondSellingPrice')
		kind = dict.get('kind')
		vat = dict.get('vat')

		assert isinstance(id_, str), f'Product ID should be string. ID is {id_}. Type is {type(id_)}'

		assert name is not None, f'Product name should not be null. Product name is {name}. Type is {type(name)}'

		assert isinstance(purchasePrice, int) or isinstance(purchasePrice, float), f'Product purchase price should be ' \
																				   f'integer or float. Price is {purchasePrice}. Type is {type(purchasePrice)}'

		assert isinstance(sellingPrice, int) or isinstance(sellingPrice, float), f'Product Selling price should be ' \
																				 f'integer or float. Price is {sellingPrice}. Type is {type(sellingPrice)}'

		assert isinstance(secondSellingPrice, int) or isinstance(secondSellingPrice, float), f'Product second selling ' \
																							 f'price price should be integer or float. Price is {secondSellingPrice}. Type is {type(secondSellingPrice)}'

		assert isinstance(vat, int), f'Value-added-text of product should be integer. Vat is {vat}. Type is {type(vat)}'
		assert isinstance(kind, str), f'Product kind should be string. Kind is {kind}. Type is {type(type)}'
		try:
			product = Product(**dict)
			return product
		except Exception as e:
			raise Exception(f'Product is not created successfully {dict} is not valid. {e}')


	def copy(self):
		return Product.fromDict(self.dict())


	def __repr__(self):
		return self.__str__()


	def __str__(self):
		return 'Product(%s,%s,%s,%s,%s,%s)' % (
			self.id(), self.name(), self.purchasePrice(), self.sellingPrice(), self.kind(), self.valueAddedTax())


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


	def setID(self, id):
		if self.__id != id:
			self.__id = id
			return True
		else:
			return False


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
		super(CustomProduct, self).__init__('0', 'Unknown Product', price, price, price, 'Any', 18)

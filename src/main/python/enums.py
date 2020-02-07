class BarcodeType:
	CUSTOM = '0'
	INVALID = ''


class ProductType:
	REGULAR = 0
	WEIGHABLE = 1


	@classmethod
	def convertWeighableBarcode(cls, barcode):
		if cls.productType(barcode) == ProductType.WEIGHABLE:
			zero = ['0'] * len(barcode[7:])
			return f'{"".join(barcode[0:7])}{"".join(zero)}'
		else:
			return barcode


	@classmethod
	def productType(cls, barcode):
		if len(barcode) > 12 and barcode[0:2] == '27':
			return cls.WEIGHABLE
		else:
			return cls.REGULAR

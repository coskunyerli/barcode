class BarcodeType:
	CUSTOM = '0'
	INVALID = ''


class ProductType:
	REGULAR = 0
	WEIGHABLE = 1


	@classmethod
	def convertWeighableBarcode(cls, barcode):
		zero = ['0'] * len(barcode[2:5])
		zero2 = ['0'] * len(barcode[7:])
		return f'{"".join(barcode[0:2])}{"".join(zero)}{"".join(barcode[5:7])}{"".join(zero2)}'


	@classmethod
	def productType(cls, barcode):
		if len(barcode) > 5 and barcode[0:2] == '27':
			return cls.WEIGHABLE
		else:
			return cls.REGULAR

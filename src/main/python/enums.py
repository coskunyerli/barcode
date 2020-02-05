class BarcodeType:
	CUSTOM = '0'
	INVALID = ''


class ProductType:
	REGULAR = 0
	WEIGHABLE = 1


	@classmethod
	def convertWeighableBarcode(cls, barcode):
		zero = [0] * len(barcode[2:])
		return f'{"".join(barcode[0:2])}{"".join(zero)}'

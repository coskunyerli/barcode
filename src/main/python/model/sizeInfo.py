import PySide2.QtCore as QtCore


class SizeInfo(object):
	def __init__(self, size, headerSizes):
		if isinstance(size, QtCore.QSize) is False:
			size = None
		if isinstance(headerSizes, list) is False:
			headerSizes = None
		else:
			sizes = list(filter(lambda item: isinstance(item, int) is False, headerSizes))
			if len(sizes) > 0:
				headerSizes = None

		self.size = size
		self.headerSizes = headerSizes


	def isValid(self):
		return self.size is not None and self.headerSizes is not None

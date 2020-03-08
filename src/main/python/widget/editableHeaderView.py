import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore


class HeaderLineEdit(QtWidgets.QLineEdit):
	editingFinishedChanged = QtCore.Signal()


	def __init__(self, parent = None):
		super(HeaderLineEdit, self).__init__(parent)
		self.setStyleSheet('color:black;background-color:white')
		self.__oldText = self.text()
		self.editingFinished.connect(self.__editingFinishedChanged)


	def __editingFinishedChanged(self):
		if self.__oldText != self.text():
			self.__oldText = self.text()
			self.editingFinishedChanged.emit()


class HeaderWidget(QtWidgets.QFrame):
	editingFinishedChanged = QtCore.Signal()
	compareChanged = QtCore.Signal(object)


	def __init__(self, parent = None):
		super(HeaderWidget, self).__init__(parent)
		self.setStyleSheet('background-color:#303030')
		self.horizontalLayout = QtWidgets.QHBoxLayout(self)
		self.lineEdit = HeaderLineEdit(self)
		self.combobox = QtWidgets.QComboBox(self)
		stringModel = QtCore.QStringListModel(['=', '<', '>', '<=', '>='])
		self.combobox.setModel(stringModel)
		self.methods = {'=': lambda obj1, obj2: obj1 == obj2, '<': lambda obj1, obj2: obj1 < obj2,
						'>': lambda obj1, obj2: obj1 > obj2, '<=': lambda obj1, obj2: obj1 <= obj2,
						'>=': lambda obj1, obj2: obj1 >= obj2}
		self.combobox.setStyleSheet('color:white')
		self.combobox.setFixedWidth(60)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setSpacing(4)

		self.horizontalLayout.addWidget(self.lineEdit)
		self.horizontalLayout.addWidget(self.combobox)

		self.lineEdit.editingFinishedChanged.connect(self.editingFinishedChanged.emit)
		self.combobox.currentTextChanged.connect(self.__updateCompareMethod)


	def __updateCompareMethod(self, text):
		if self.methods.get(text) is not None:
			self.compareChanged.emit(self.methods[text])


	def compare(self):
		return self.methods[self.combobox.currentText()]


	def text(self):
		return self.lineEdit.text()


	def setPlaceholderText(self, text):
		self.lineEdit.setPlaceholderText(text)


class HeaderData(object):
	def __init__(self, func, text):
		self.func = func
		self.text = text


class EditableHeaderView(QtWidgets.QFrame):
	sectionChanged = QtCore.Signal(int, HeaderData)


	def __init__(self, parent = None):
		super(EditableHeaderView, self).__init__(parent)
		self.setStyleSheet('background-color:#303030')
		self.horizontalLayout = QtWidgets.QHBoxLayout(self)
		self.__model = None
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

		self.barcodeWidget = HeaderWidget(self)
		self.barcodeWidget.setPlaceholderText('Barcode')
		self.barcodeWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(0, HeaderData(self.barcodeWidget.compare(),
															   self.barcodeWidget.text())))
		methods = {'=': lambda obj1, obj2: obj1 == obj2, 'in': lambda obj1, obj2: obj1 in obj2}
		self.barcodeWidget.methods = methods
		self.barcodeWidget.combobox.clear()
		self.barcodeWidget.combobox.addItems(['=', 'in'])
		self.barcodeWidget.combobox.setCurrentText('=')

		self.barcodeWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(0, HeaderData(self.barcodeWidget.compare(),
															   self.barcodeWidget.text())))

		self.nameWidget = HeaderWidget(self)
		self.nameWidget.setPlaceholderText('Name')
		self.nameWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(1, HeaderData(self.nameWidget.compare(),
															   self.nameWidget.text())))

		self.nameWidget.combobox.clear()
		self.nameWidget.combobox.addItems(['=', 'in'])
		self.nameWidget.combobox.setCurrentText('=')
		self.nameWidget.methods = methods
		self.nameWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(1, HeaderData(self.nameWidget.compare(),
															   self.nameWidget.text())))

		self.priceWidget = HeaderWidget(self)
		self.priceWidget.setPlaceholderText('Price')
		self.priceWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(2, HeaderData(self.priceWidget.compare(),
															   self.priceWidget.text())))
		self.priceWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(2, HeaderData(self.priceWidget.compare(),
															   self.priceWidget.text())))

		self.purchasePriceWidget = HeaderWidget(self)
		self.purchasePriceWidget.setPlaceholderText('Purchase Price')
		self.purchasePriceWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(3, HeaderData(self.purchasePriceWidget.compare(),
															   self.purchasePriceWidget.text())))
		self.purchasePriceWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(3, HeaderData(self.purchasePriceWidget.compare(),
															   self.purchasePriceWidget.text())))

		self.secondSellingPriceWidget = HeaderWidget(self)
		self.secondSellingPriceWidget.setPlaceholderText('Second Selling Price')
		self.secondSellingPriceWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(4, HeaderData(self.secondSellingPriceWidget.compare(),
															   self.secondSellingPriceWidget.text())))
		self.secondSellingPriceWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(4, HeaderData(self.secondSellingPriceWidget.compare(),
															   self.secondSellingPriceWidget.text())))

		self.vatWidget = HeaderWidget(self)
		self.vatWidget.setPlaceholderText('Value Added Tax')
		self.vatWidget.editingFinishedChanged.connect(
				lambda: self.sectionChanged.emit(5, HeaderData(self.vatWidget.compare(),
															   self.vatWidget.text())))
		self.vatWidget.compareChanged.connect(
				lambda: self.sectionChanged.emit(5, HeaderData(self.vatWidget.compare(),
															   self.vatWidget.text())))

		# self.calenderWidget = QtWidgets.QWidget(self)
		# self.calenderWidgetLayout = QtWidgets.QHBoxLayout(self.calenderWidget)
		# self.calenderWidgetLayout.setContentsMargins(0, 0, 0, 0)
		#
		# self.calenderLabel = QtWidgets.QLabel(self.calenderWidget)
		# self.calenderLabel.setText('Created Date')
		#
		# self.calenderLineEdit = QtWidgets.QDateTimeEdit(QtCore.QDate(QtCore.QDate.currentDate()), self.calenderWidget)
		# self.calenderLineEdit.setCalendarPopup(True)
		# self.calenderLineEdit.setStyleSheet('color:black')
		#
		# self.calenderWidgetLayout.addWidget(self.calenderLabel)
		# self.calenderWidgetLayout.addWidget(self.calenderLineEdit)

		self.horizontalLayout.addWidget(self.barcodeWidget)
		self.horizontalLayout.addWidget(self.nameWidget)
		self.horizontalLayout.addWidget(self.priceWidget)
		self.horizontalLayout.addWidget(self.purchasePriceWidget)
		self.horizontalLayout.addWidget(self.secondSellingPriceWidget)
		self.horizontalLayout.addWidget(self.vatWidget)
		# self.horizontalLayout.addWidget(self.calenderWidget)
		# self.calenderLineEdit.dateTimeChanged.connect(self.test)


	def test(self, dateTime):
		print(dateTime)

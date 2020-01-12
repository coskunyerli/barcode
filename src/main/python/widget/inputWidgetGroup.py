import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore

from enums import BarcodeType
from widget.lineEdit import LineEdit


class InputWidgetGroup(QtWidgets.QWidget):
	barcodeChanged = QtCore.Signal(str)


	def __init__(self, parent = None):
		super(InputWidgetGroup, self).__init__(parent)
		self.inputWidgetLayout = QtWidgets.QHBoxLayout(self)
		self.inputWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.inputWidgetLayout.setSpacing(0)

		self.inputs = [self.createInput('Barcode'),
					   self.createInput('Amount'), self.createInput('Price')]

		self.inputs[1].setValidator(QtGui.QIntValidator(self.inputs[0]))
		self.inputs[2].setValidator(QtGui.QDoubleValidator(self.inputs[0]))
		self.clearInputs()
		self.setFocusPolicy(QtCore.Qt.NoFocus)


	def createInput(self, text):
		input_ = LineEdit(self)
		input_.setPlaceholderText(text)
		input_.setObjectName('inputWidget')
		self.inputWidgetLayout.addWidget(input_)
		return input_


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.addProduct()
		else:
			super(InputWidgetGroup, self).keyPressEvent(event)


	def enableAmountWidget(self):
		self.inputs[1].setEnabled(True)
		self.inputs[1].setFocus()


	def barcodeLineEdit(self):
		return self.inputs[0]


	def currentBarcode(self):
		return self.inputs[0].text()


	def price(self):
		if self.inputs[2].text() == '':
			return 0.0
		else:
			return float(self.inputs[2].text().replace(',', '.'))


	def amount(self):
		if self.inputs[1].text() == '':
			return 1
		else:
			return int(self.inputs[1].text())


	def clearInputs(self):
		for input_ in self.inputs:
			input_.clear()

		self.inputs[1].setEnabled(False)
		self.inputs[2].setEnabled(False)


	def addProduct(self):
		if self.currentBarcode() == BarcodeType.CUSTOM:
			if self.inputs[2].text() == '':
				self.inputs[2].setEnabled(True)
				self.inputs[2].setFocus()
			else:
				self.barcodeChanged.emit(self.currentBarcode())
				self.clearInputs()
		elif self.currentBarcode() != BarcodeType.INVALID:
			self.barcodeChanged.emit(self.currentBarcode())
			self.clearInputs()

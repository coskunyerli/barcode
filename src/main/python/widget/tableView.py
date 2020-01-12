import os

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui

import static
from enums import BarcodeType
from widget.lineEdit import LineEdit


class TableView(QtWidgets.QTableView):
	barcodeChanged = QtCore.Signal(str)


	def __init__(self, parent = None):
		super(TableView, self).__init__(parent)
		self.setFocusPolicy(QtCore.Qt.StrongFocus)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Asterisk:
			self.enableAmountWidget()
		elif event.key() == QtCore.Qt.Key_Backspace:
			index = self.__tableView.currentIndex()
			if index.isValid():
				self.__tableView.model().pop(index.row())
		else:
			super(TableView, self).keyPressEvent(event)

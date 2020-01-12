import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui


class LineEdit(QtWidgets.QLineEdit):
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Asterisk:
			event.ignore()
		else:
			super(LineEdit, self).keyPressEvent(event)

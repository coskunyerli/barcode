import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore


class PushButton(QtWidgets.QLabel):
	clicked = QtCore.Signal()


	def __init__(self, parent = None):
		super(PushButton, self).__init__(parent)
		self.setAlignment(QtCore.Qt.AlignCenter)


	def mouseReleaseEvent(self, event):
		if event.button() & QtCore.Qt.LeftButton:
			self.clicked.emit()
		super(PushButton, self).mouseReleaseEvent(event)

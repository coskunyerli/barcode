import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore


class FooterWidget(QtWidgets.QFrame):
	def __init__(self, parent = None):
		super(FooterWidget, self).__init__(parent)
		self.setFixedHeight(20)

import PySide2.QtWidgets as QtWidgets


class DialogNameWidget(QtWidgets.QWidget):

	def __init__(self, parent = None):
		super(DialogNameWidget, self).__init__(parent)

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		self.__label = QtWidgets.QLabel(self)
		self.verticalLayout.addWidget(self.__label)
		self.__label.setStyleSheet(self.__styleSheet(24))


	def setText(self, text):
		self.__label.setText(text)


	def setAlignment(self, alignment):
		self.__label.setAlignment(alignment)


	def setPointSize(self, pointSize):
		self.__label.setStyleSheet(self.__styleSheet(pointSize))


	def __styleSheet(self, font):
		return f"""
			padding: 2px;
			border: 1px solid #606060;
    	 	border-radius: 8px;
    	 	color:white;
    	 	font-size: {font}pt;
			"""

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore


class ButtonGroupWidget(QtWidgets.QWidget):
	currentIndexChanged = QtCore.Signal(int)


	def __init__(self, size = 0, parent = None):
		super(ButtonGroupWidget, self).__init__(parent)
		self.mainLayout = QtWidgets.QHBoxLayout(self)
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.setSpacing(0)
		self.newButton = QtWidgets.QPushButton(self)
		self.newButton.setText('+')
		self.mainLayout.addWidget(self.newButton)
		self.buttonList = []
		self.__currentIndex = -1
		self.__defaultButtonSize = size
		self.newButton.clicked.connect(self.__addButton)
		self.customContextMenuRequested.connect(self.__showPopup)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		for _ in range(self.__defaultButtonSize):
			self.addButton('Label')


	def setDefaultButtonSize(self, size):
		self.__defaultButtonSize = size
		if len(self.buttonList) < self.__defaultButtonSize:
			for _ in len(self.buttonList) - self.__defaultButtonSize:
				self.addButton('Label')


	def setCurrentIndex(self, index):
		if self.currentButton() is not None:
			self.currentButton().setChecked(False)
		self.__currentIndex = index
		if self.currentButton() is not None:
			self.currentButton().setChecked(True)


	def currentIndex(self):
		return self.__currentIndex


	def currentButton(self):
		if self.currentIndex() != None and self.currentIndex() != -1:
			return self.buttonList[self.currentIndex()]
		else:
			return None


	def addButton(self, text):
		button = QtWidgets.QPushButton(self)
		button.setText(text)
		button.setProperty('button', True)
		self.buttonList.append(button)
		self.mainLayout.insertWidget(self.mainLayout.count() - 1, button)


	def __addButton(self):
		self.addButton('Label')


	def __showPopup(self, pos):
		globalPos = self.mapToGlobal(pos)

		button = self.childAt(pos)
		if button is not None and button.property('button') and len(self.buttonList) > 1:
			menu = QtWidgets.QMenu(self)
			removeAction = menu.addAction('Remove')
			action = menu.exec_(globalPos)
			if action == removeAction:
				self.mainLayout.removeWidget(button)
				button.setParent(None)
				button.hide()
				currentButton = self.currentButton()
				self.buttonList.remove(button)
				if currentButton == button:
					self.setCurrentIndex(0)


	def mouseReleaseEvent(self, event):
		if event.button() & QtCore.Qt.LeftButton:
			button = self.childAt(event.pos())
			if button.property('button'):
				button.setChecked(True)
		else:
			super(ButtonGroupWidget, self).mouseReleaseEvent(event)

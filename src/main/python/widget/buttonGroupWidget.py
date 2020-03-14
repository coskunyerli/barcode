import os
import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
import core


class ButtonItem(QtWidgets.QPushButton):
	def __init__(self, parent = None):
		super(ButtonItem, self).__init__(parent)
		self.__data = None


	def setData(self, data):
		self.__data = data


	def data(self):
		return self.__data


class ButtonItemData(object):
	def __init__(self, text, data):
		self.text = text
		self.data = data


	def __str__(self):
		return f'ButtonItemData({self.text}, {self.data})'


	def __eq__(self, other):
		return self.text == other.text and self.data == other.data


class ButtonGroupWidget(QtWidgets.QWidget):
	clicked = QtCore.Signal(int, int, ButtonItemData)
	createClicked = QtCore.Signal()


	def __init__(self, parent = None):
		super(ButtonGroupWidget, self).__init__(parent)
		self.size = QtCore.QSize(80, 80)
		self.buttonItemDataList = []
		self.scrollbarArea = QtWidgets.QScrollArea(self)
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.addWidget(self.scrollbarArea)
		self.verticalSpacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
														QtWidgets.QSizePolicy.Expanding)
		self.horizontalSpacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
														  QtWidgets.QSizePolicy.Minimum)

		self.mainWidget = QtWidgets.QWidget(self.scrollbarArea)
		self.scrollbarArea.setWidget(self.mainWidget)
		self.scrollbarArea.setWidgetResizable(True)
		self.gridLayout = QtWidgets.QGridLayout(self.mainWidget)
		self.__columnCount = None
		self.setColumnCount(4)

		self.newButton = self.createButton(ButtonItemData('', None))

		self.newButton.clicked.connect(self.createClicked.emit)
		self.newButton.setObjectName('newButton')
		self.gridLayout.addWidget(self.newButton, 0, 0)
		self.gridLayout.addItem(self.horizontalSpacerItem)
		self.gridLayout.addItem(self.verticalSpacerItem)

		icon = QtGui.QIcon(QtGui.QPixmap(core.fbs.get_resource(os.path.join('icons', 'baseline_add_white_48dp.png'))))
		self.newButton.setIcon(icon)
		self.newButton.setIconSize(QtCore.QSize(24, 24))

		self.mainWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.mainWidget.customContextMenuRequested.connect(self.__showPopup)


	def __showPopup(self, pos):
		contextMenu = QtWidgets.QMenu()
		removeAction = contextMenu.addAction('Remove')
		globalPos = self.mainWidget.mapToGlobal(pos)
		widget = self.childAtLayout(pos)
		if widget is not None:
			action = contextMenu.exec_(globalPos)
			if action == removeAction:
				row, column = self.index(widget)
				self.removeButton(row, column)


	def childAtLayout(self, point):
		for button in self.buttonItemDataList:
			if button.geometry().contains(point):
				return button
		return None


	def setColumnCount(self, columnCount):
		if self.__columnCount != columnCount and columnCount > 0:
			self.__columnCount = columnCount
			margins = self.gridLayout.contentsMargins()
			self.setFixedWidth(self.size.width() * self.__columnCount + margins.left() + margins.right())

		self.resetView()


	def createButton(self, data):
		for b in self.buttonItemDataList:
			if b.data() == data:
				return None
		button = ButtonItem(self.mainWidget)
		button.clicked.connect(lambda checked = False, button = button: self.buttonClicked(button))
		button.setData(data)
		label = QtWidgets.QLabel(button)
		label.setText(data.text)
		label.setWordWrap(True)
		label.setAlignment(QtCore.Qt.AlignCenter)
		layout = QtWidgets.QVBoxLayout(button)
		layout.setContentsMargins(4, 0, 4, 0)
		layout.addWidget(label)
		button.setObjectName('buttonItem')
		button.setFixedSize(self.size)
		return button


	def addButton(self, data):
		button = self.createButton(data)
		if button is not None:
			self.__addButton(button)
			self.buttonItemDataList.append(button)


	def __addButton(self, button):
		self.beginReArrange()
		count = self.gridLayout.count()
		row = int(count / self.__columnCount)
		column = count % self.__columnCount
		self.gridLayout.addWidget(button, row, column)
		self.endReArrange()


	def beginReArrange(self):
		self.gridLayout.removeItem(self.verticalSpacerItem)
		self.gridLayout.removeItem(self.horizontalSpacerItem)
		self.gridLayout.removeWidget(self.newButton)


	def endReArrange(self):
		count = self.gridLayout.count()
		row = int(count / self.__columnCount)
		column = count % self.__columnCount
		self.gridLayout.addWidget(self.newButton, row, column)
		self.gridLayout.addItem(self.verticalSpacerItem, self.gridLayout.rowCount(), 0)
		self.gridLayout.addItem(self.horizontalSpacerItem, 0, self.__columnCount)


	def removeButton(self, row, column):
		index = row * self.__columnCount + column
		button = self.buttonItemDataList[index]
		self.gridLayout.removeWidget(button)
		button.setParent(None)
		button.close()
		self.buttonItemDataList.remove(button)
		button.blockSignals(True)
		del button
		self.resetView()


	def resetView(self):
		self.clearView()
		for button in self.buttonItemDataList:
			self.__addButton(button)


	def clearView(self):
		for button in self.buttonItemDataList:
			self.gridLayout.removeWidget(button)


	def buttonClicked(self, button):
		row, column = self.index(button)
		if row is not None and column is not None:
			self.clicked.emit(row, column, button.data())


	def index(self, widget):
		try:
			index = self.buttonItemDataList.index(widget)
			row = int(index / self.__columnCount)
			column = index % self.__columnCount
			return row, column
		except:
			return None, None


	def itemDataList(self):
		return list(map(lambda button: button.data(), self.buttonItemDataList))
# def keyPressEvent(self, event):
# 	if event.modifiers() & QtCore.Qt.ShiftModifier:
# 		print(int(event.key()))
# 	else:
# 		super(ButtonGroupWidget, self).keyPressEvent(event)

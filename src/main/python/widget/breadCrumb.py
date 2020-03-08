import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
import static

class BreadCrumbData(object):

	def __init__(self):
		self._isActive = False
		self.__parent = None


	def _setParent(self, parent):
		self.__parent = parent


	def setActive(self, res):
		self._isActive = res
		self.__parent._update()


	def isActive(self):
		return self._isActive


class ModelBreadCrumbData(BreadCrumbData):
	def __init__(self):
		super(ModelBreadCrumbData, self).__init__()
		self.__model = None


	def setModel(self, model):
		self.__model = model
		self.__model.totalPriceChanged.connect(self.__updateActivity)


	def __updateActivity(self, _):
		res = self.__model.rowCount() != 0
		self.setActive(res)


	def model(self):
		return self.__model


	def __str__(self):
		return 'ModelBreadCrumbData(%s)' % self.model()


class BreadCrumb(QtWidgets.QFrame):
	clicked = QtCore.Signal(int)
	currentIndexChanged = QtCore.Signal(int)
	itemAdded = QtCore.Signal(object)


	def setItemCLass(self, klass):
		self._itemDataClass = klass


	def __init__(self, parent = None):
		super(BreadCrumb, self).__init__(parent)
		self._itemDataClass = BreadCrumbData
		self.mainLayout = QtWidgets.QHBoxLayout(self)
		self.mainLayout.setSpacing(1)
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.buttonList = []
		self.__spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.__currentIndex = None
		self.mainLayout.addItem(self.__spacer)
		self._lastItem = None
		self.__defaultButtonSize = 0
		self.__defaultName = 'Label'
		self.__addButton = BreadCrumbItem('+', self)
		self.__addButton.setFixedWidth(20)
		self.__addButton.setAlignment(QtCore.Qt.AlignCenter)
		self.buttonList.append(self.__addButton)
		self.mainLayout.addWidget(self.__addButton)
		self.customContextMenuRequested.connect(self.__showPopup)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		# create default size bread crumb items
		for _ in range(self.__defaultButtonSize):
			self.addButton(self.__defaultName)


	def itemData(self, index):
		return self.buttonList[index].itemData()


	def currentItemData(self):
		if self.currentIndex() is None or self.currentIndex() == -1:
			return None
		return self.buttonList[self.currentIndex()].itemData()


	def setDefaultName(self, name):
		self.__defaultName = name
		for i in range(len(self.buttonList) - 1):
			button = self.buttonList[i]
			button.setText('%s %s' % (self.__defaultName, i + 1))


	def __showPopup(self, pos):
		globalPos = self.mapToGlobal(pos)

		buttonIndex = self.itemAt(pos)
		if buttonIndex is not None:
			button = self.buttonList[buttonIndex]
			if button.property('button') and len(self.buttonList) - 1 > 1:
				menu = QtWidgets.QMenu()
				removeAction = menu.addAction('Remove')
				action = menu.exec_(globalPos)
				if action == removeAction:
					self.mainLayout.removeWidget(button)
					button.setParent(None)
					button.hide()
					button.deleteLater()
					currentButton = self.__currentButton()
					self.buttonList.remove(button)
					if currentButton == button:
						self.setCurrentIndex(0)
					else:
						index = self.buttonList.index(currentButton)
						self.setCurrentIndex(index)
				del menu


	def setDefaultButtonSize(self, size):
		self.__defaultButtonSize = size
		if self.count() < self.__defaultButtonSize:
			for _ in range(self.__defaultButtonSize - len(self.buttonList) + 1):
				self.addButton(self.__defaultName)


	def mouseReleaseEvent(self, event):
		if event.button() & QtCore.Qt.LeftButton:
			breadCrumbItemIndex = self.itemAt(event.pos())
			if breadCrumbItemIndex is not None:
				if breadCrumbItemIndex == len(self.buttonList) - 1:
					self.addButton(self.__defaultName)
				else:
					self.clicked.emit(breadCrumbItemIndex)
					self.setCurrentIndex(breadCrumbItemIndex)
		else:
			super(BreadCrumb, self).mouseReleaseEvent(event)


	def setCurrentIndex(self, index):
		index = min(self.count() - 1, max(0, index))
		button = self.buttonList[index]
		if self.__currentButton() is not None:
			self.__currentButton().setCurrent(False)
		button.setCurrent(True)
		self.__currentIndex = index
		self.currentIndexChanged.emit(index)


	def currentIndex(self):
		return self.__currentIndex


	def __currentButton(self):
		if self.currentIndex() is not None and -1 < self.currentIndex() < len(self.buttonList) - 1:
			return self.buttonList[self.currentIndex()]
		else:
			return None


	def itemAt(self, pos):

		def cmp(item):
			geometry = item.geometry()
			if geometry.contains(pos):
				return 0
			return static.cmp(geometry.left(), pos.x())


		return static.binarySearch(self.buttonList, cmp = lambda item: cmp(item))


	def addButton(self, text):
		item = BreadCrumbItem('%s %s' % (text, len(self.buttonList)), self)
		item.setProperty('button', True)
		item.setFixedSize(QtCore.QSize(80, 80))
		item.setAlignment(QtCore.Qt.AlignCenter)
		self.buttonList.insert(len(self.buttonList) - 1, item)
		self.mainLayout.insertWidget(self.mainLayout.count() - 2, item)
		self.itemAdded.emit(item.itemData())


	def _clearItems(self):
		for item in self.buttonList:
			self.mainLayout.removeWidget(item)
			item.setParent(None)
			del item
		self.mainLayout.removeItem(self.__spacer)
		self.buttonList = []


	def count(self):
		return len(self.buttonList) - 1


class BreadCrumbItem(QtWidgets.QFrame):

	def __init__(self, text, parent = None):
		super(BreadCrumbItem, self).__init__(parent)
		self.__itemData = parent._itemDataClass()
		self.__itemData._setParent(self)
		self._layout = QtWidgets.QVBoxLayout(self)
		self.label = QtWidgets.QLabel(self)
		self.label.setMaximumWidth(200)
		self.label.setText(text)
		self.redLight = QtWidgets.QFrame(self)
		self.redLight.setFixedHeight(2)

		self.light = QtWidgets.QFrame(self)
		self.light.setFixedHeight(2)
		self._layout.setContentsMargins(0, 0, 0, 2)
		self._layout.setSpacing(0)
		self._layout.addWidget(self.light)
		self._layout.addWidget(self.label)
		self._layout.addWidget(self.redLight)
		self.setStyleSheet("background-color:%s" % '#404040')
		self.__isCurrent = False


	def itemData(self):
		return self.__itemData


	def setText(self, text):
		text = self.label.fontMetrics().elidedText(text, QtCore.Qt.ElideRight, self.label.maximumWidth())
		self.label.setText(text)


	def text(self):
		return self.label.text()


	def setCurrent(self, res):
		self.__isCurrent = res
		if self.__isCurrent is True:
			self.setStyleSheet('background-color:#373737')
		else:
			self.setStyleSheet('background-color:#404040')


	def setAlignment(self, align):
		self.label.setAlignment(align)


	def _update(self):
		if self.itemData().isActive():
			self.light.setStyleSheet('background-color:#DC7D14')
		else:
			self.light.setStyleSheet('background-color:transparent')

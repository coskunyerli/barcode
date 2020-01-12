import os

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui


class Toast(QtWidgets.QFrame):
	toastArray = []
	settings = {'fadeInTime': 1000, 'fadeOutTime': 200, 'titleStyle': "color:white",
				'messageStyle': "color:white", 'showAnimationType': 6, 'hideAnimationType': 0,
				'style': '', 'addTop': True, 'iconPath': '.'}


	def __init__(self, title, message, parent = None):
		super(Toast, self).__init__(parent)
		self.setupUi()
		self.initWidgets()
		self.timer = QtCore.QTimer(parent)
		self.titleLabel.setText(title)
		self.messageLabel.setText(message)
		self.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.setFrameShadow(QtWidgets.QFrame.Plain)
		eff = QtWidgets.QGraphicsOpacityEffect(self)
		eff.setOpacity(0)
		self.setGraphicsEffect(eff)
		self.showAnim = QtCore.QPropertyAnimation(eff, b'opacity', eff)
		self.showAnim.setDuration(Toast.settings.get('fadeInTime'))
		self.showAnim.setStartValue(0)
		self.showAnim.setEndValue(1)
		self.showAnim.setEasingCurve(
			QtCore.QEasingCurve(QtCore.QEasingCurve.Type(Toast.settings.get('showAnimationType'))))
		self.hideAnim = QtCore.QPropertyAnimation(eff, b'opacity', eff)
		self.hideAnim.setDuration(Toast.settings.get('fadeOutTime'))
		self.hideAnim.setStartValue(1)
		self.hideAnim.setEndValue(0)
		self.hideAnim.setEasingCurve(
			QtCore.QEasingCurve(QtCore.QEasingCurve.Type(Toast.settings.get('hideAnimationType'))))
		self.initSignalsAndSlot()


	def setupUi(self):
		self.setObjectName("Toast")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
		self.iconLabel = QtWidgets.QLabel(self)
		self.iconLabel.setObjectName("iconLabel")
		self.horizontalLayout.addWidget(self.iconLabel)
		self.widget = QtWidgets.QWidget(self)
		self.widget.setMinimumWidth(300)
		self.widget.setMaximumWidth(300)
		self.widget.setObjectName("widget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
		self.verticalLayout.setContentsMargins(0, 0, 9, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.titleLabel = QtWidgets.QLabel(self.widget)

		self.titleLabel.setObjectName("titleLabel")
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setWeight(75)
		font.setBold(True)
		self.titleLabel.setFont(font)
		self.verticalLayout.addWidget(self.titleLabel)
		self.messageLabel = QtWidgets.QLabel(self.widget)
		self.messageLabel.setStyleSheet("color:white")
		self.messageLabel.setObjectName("messageLabel")
		self.verticalLayout.addWidget(self.messageLabel)
		self.horizontalLayout.addWidget(self.widget)
		self.horizontalLayout.setSpacing(15)
		self.verticalLayout.setSpacing(2)

		self.messageLabel.setWordWrap(True)
		self.titleLabel.setWordWrap(True)

		QtCore.QMetaObject.connectSlotsByName(self)


	def initWidgets(self):
		self.closeButton = QtWidgets.QPushButton(self)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(Toast.settings['iconPath'], "delete.png")),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		self.closeButton.setIcon(icon)
		self.closeButton.setIconSize(QtCore.QSize(12, 12))
		self.closeButton.move(self.sizeHint().width() - 4, 4)
		self.closeButton.setMaximumSize(QtCore.QSize(12, 12))
		self.titleLabel.setStyleSheet(Toast.settings.get('titleStyle'))
		self.messageLabel.setStyleSheet(Toast.settings.get('messageStyle'))
		self.setStyleSheet(Toast.settings.get('style'))


	def setBackgroundColor(self, color):
		text = "background-color:%s;border-radius:8px;" % color.name()
		self.setStyleSheet(text)


	def initSignalsAndSlot(self):
		self.timer.timeout.connect(lambda: self.hideAnim.start(QtCore.QPropertyAnimation.DeleteWhenStopped))
		self.hideAnim.finished.connect(self.close)
		self.closeButton.clicked.connect(self._clickClosed)


	def setIcon(self, icon):
		self.iconLabel.setPixmap(icon.pixmap(QtCore.QSize(24, 24)))


	def show(self):
		self.timer.start(self.animationTime())
		if Toast.settings.get('addTop'):
			Toast.toastArray.insert(0, self)
		else:
			Toast.toastArray.append(self)
		Toast._updateToastsGeometry()
		super(Toast, self).show()
		self.showAnim.start(QtCore.QPropertyAnimation.DeleteWhenStopped)


	def animationTime(self):
		return 6 * len(self.titleLabel.text()) * len(self.messageLabel.text())


	def close(self):
		self.timer.stop()
		try:
			Toast.toastArray.remove(self)
		except ValueError as e:
			pass
		super(Toast, self).close()


	def _clickClosed(self):
		self.close()
		Toast._updateToastsGeometry()


	@classmethod
	def success(cls, title, message, parent = None):
		toast = Toast(title, message, parent)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(Toast.settings['iconPath'], "checkmark.png")),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		toast.setBackgroundColor(QtGui.QColor('#4CA055'))
		toast.setIcon(icon)
		toast.show()


	@classmethod
	def info(cls, title, message, parent = None):
		toast = Toast(title, message, parent)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(Toast.settings['iconPath'], "info.png")),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		toast.setIcon(icon)
		toast.setBackgroundColor(QtGui.QColor('#4596B2'))
		toast.show()


	@classmethod
	def warning(cls, title, message, parent = None):
		toast = Toast(title, message, parent)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(Toast.settings['iconPath'], "attention.png")),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		toast.setIcon(icon)
		toast.setBackgroundColor(QtGui.QColor('#FD9326'))
		toast.show()


	@classmethod
	def error(cls, title, message, parent = None):
		toast = Toast(title, message, parent)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(Toast.settings['iconPath'], "delete.png")),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		toast.setIcon(icon)
		toast.setBackgroundColor(QtGui.QColor('#C1392F'))
		toast.show()


	@classmethod
	def _updateToastsGeometry(cls):
		indexHeight = 10
		for i in range(len(cls.toastArray)):
			toast = cls.toastArray[i]
			toast.move(toast.parent().width() - toast.sizeHint().width() - 10, indexHeight)
			indexHeight += toast.sizeHint().height() + 5

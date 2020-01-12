import PySide2.QtCore as QtCore


class EventFilterForTableView(QtCore.QObject):

	def eventFilter(self, object, event):
		if event.type() == QtCore.QEvent.KeyPress:
			if event.text().isdigit():
				event.ignore()
				return True
		return QtCore.QObject.eventFilter(self, object, event)

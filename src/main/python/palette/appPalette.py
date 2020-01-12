import PySide2.QtCore as QtCore, PySide2.QtGui as QtGui, PySide2.QtWidgets as QtWidgets

def getAppPalette():
	palette = QtGui.QPalette()
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

	brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)

	brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)

	brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)

	brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)

	brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)

	brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

	brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)

	brush = QtGui.QBrush(QtGui.QColor(247, 147, 30))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)

	# inactive
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)

	brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)

	brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)

	brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)

	brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)

	brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)

	brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

	brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)

	brush = QtGui.QBrush(QtGui.QColor(247, 147, 30))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)

	# disabled
	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

	brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

	brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)

	brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)

	brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)

	brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)

	brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

	brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)

	brush = QtGui.QBrush(QtGui.QColor(174, 174, 174))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)

	brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)

	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)

	return palette
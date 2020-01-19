import datetime

import log
from fbs import BarcodeApplicationContext
import os
import sys
import core
import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore
from palette import appPalette
from widget.mainWindow import MainWindow

from widget.toast import Toast

if __name__ == '__main__':
	fbs = BarcodeApplicationContext()  # 1. Instantiate ApplicationContext
	core.fbs = fbs

	logName = datetime.datetime.now().strftime("%m-%d-%Y.log")
	try:
		logPath = os.path.join(fbs.get_resource(), 'log')
		# check path exists or not. I not exists create it

		if os.path.exists(logPath) is False:
			os.mkdir(logPath)
			print('Log folder is created')

		log.basicConfig(filename = os.path.join(logPath, logName),
						format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = log.INFO)

		try:
			basePath = fbs.get_resource()
			productPath = os.path.join(basePath, 'product')
			if os.path.exists(productPath) is False:
				os.mkdir(productPath)
				log.info('Product folder is created')

		except Exception as e:
			print(f'product folder is not created successfully. Exception is {e}')

		brush = QtGui.QBrush(QtGui.QColor('#383838'))
		brush.setStyle(QtCore.Qt.SolidPattern)

		palette = appPalette.getAppPalette()
		brush = QtGui.QBrush(QtGui.QColor('#383838'))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		fbs.app.setPalette(palette)

		mainWindow = MainWindow()
		mainWindow.show()
		Toast.settings['iconPath'] = fbs.get_resource('icons')
		barcodeQssFile = fbs.get_resource(os.path.join('qss', 'barcode.qss'))

		try:
			qssFile = open(barcodeQssFile)
			mainWindow.setStyleSheet(qssFile.read())
		except Exception as e:
			print(
					'Failed qss file barcode.qss for MainWindow path is %s, Error is %s ' % (
						os.path.abspath(barcodeQssFile), str(e)))
			QtWidgets.QMessageBox.warning(mainWindow, 'Qss Error',
										  'Path is %s. Error is %s' % (os.path.abspath(barcodeQssFile), str(e)))
	except Exception as e:
		log.critical(f'Unexpected error is occurred, Error is => {e}')
		QtWidgets.QMessageBox().critical(None, 'Error', 'Unexpected error is occurred')
		sys.exit(1)

	try:
		result = fbs.app.exec_()
		sys.exit(result)
	except Exception as e:
		log.critical(f'Running error Error is => {e}')
		QtWidgets.QMessageBox().warning(None, 'Running error ', '')

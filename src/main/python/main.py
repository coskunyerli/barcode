import datetime

import log
from fbs import BarcodeApplicationContext
import os
import sys
import core
import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore
from palette import appPalette
from service import databaseService
from service.databaseService import DatabaseServiceModel
from widget.mainWindow import MainWindow

from widget.toast import Toast

if __name__ == '__main__':
	databaseService._databaseServiceModel = DatabaseServiceModel()

	fbs = BarcodeApplicationContext()  # 1. Instantiate ApplicationContext
	core.fbs = fbs

	logName = datetime.datetime.now().strftime("%m-%d-%Y.log")
	try:
		logPath = os.path.join(fbs.get_resource(), 'log')
		# check path exists or not. I not exists create it

		if os.path.exists(logPath) is False:
			os.mkdir(logPath)
			print('Log folder is created')

		# log.basicConfig(filename = os.path.join(logPath, logName),
		# 				format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = log.INFO)
		log.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = log.INFO)
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

		Toast.setWidget(mainWindow)
		Toast.settings['iconsPath'] = fbs.get_resource('icons')

		mainWindow.readSettings()
		mainWindow.afterReadSettings()

		mainWindow.show()
		barcodeQss = fbs.qss('barcode.qss')
		if barcodeQss is not None:
			mainWindow.setStyleSheet(barcodeQss)
		else:
			log.warning(f'barcode.qss is not loaded successfully')

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

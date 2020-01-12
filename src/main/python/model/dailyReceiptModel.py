import json
import os
from datetime import date

from model.soldProductModel import SoldProductModel


class DailyReceiptModel(object):
	def __init__(self):
		self.__soldModelList = []
		self.__fileName = date.today()


	def read(self):
		self.__soldModelList = []
		filename = '%s.json' % self.__fileName
		if os.path.exists(filename):
			try:
				file_ = open(filename)
			except:
				print('Error occurred while read file')
			fileList = file_.read()
			dictArray = json.loads(fileList)
			for modelDict in dictArray:
				model = SoldProductModel.fromDict(modelDict)
				model.setReadOnly(True)
				self.__soldModelList.append(model)
			file_.close()


	def setList(self, list):
		self.__soldModelList = list


	def addProduct(self, model):
		self.__soldModelList.append(model)


	def save(self):
		try:
			file_ = open('%s.json' % self.__fileName, 'w')
		except:
			print('Error occurred while open file')
		file_.write(json.dumps(list(map(lambda model: model.dict(), self.__soldModelList))))
		file_.close()


	def __getitem__(self, item):
		return self.__soldModelList[item]


	def __len__(self):
		return len(self.__soldModelList)


	def income(self):
		sum = 0
		for model in self.__soldModelList:
			sum += model.totalPrice()
		return sum

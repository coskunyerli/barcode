import datetime

from model.db.base import Base
from sqlalchemy import Integer, Column, String, Float, DateTime, func
from sqlalchemy.orm import relationship


class DatabaseProduct(Base):
	__tablename__ = 'product'
	barcode = Column(Integer(), primary_key = True)
	name = Column(String())
	purchasePrice = Column(Float())
	sellingPrice = Column(Float())
	secondSellingPrice = Column(Float())
	createdDate = Column(DateTime(timezone = True), server_default = func.now())
	vat = Column(Integer())


	def __repr__(self):
		return f'DatabaseProduct({self.barcode}, {self.name}, {self.purchasePrice}, {self.sellingPrice}, {self.secondSellingPrice})'

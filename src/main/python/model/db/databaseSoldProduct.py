from model.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship


class DatabaseSoldProduct(Base):
	__tablename__ = 'soldProduct'
	id = Column(Integer(), primary_key = True)
	amount = Column(Integer())
	unit = Column(String())

	product_barcode = Column(Integer())
	product_name = Column(String())
	product_purchasePrice = Column(Float())
	product_sellingPrice = Column(Float())
	product_secondSellingPrice = Column(Float())
	product_createdDate = Column(DateTime(timezone = True), server_default = func.now())
	product_vat = Column(Integer())

	order_id = Column(Integer(), ForeignKey('order.id'))
	order = relationship('DatabaseOrder')


	def __repr__(self):
		return f'DatabaseSoldProduct({self.id}, {self.amount}, {self.product_barcode}, {self.product_name}, {self.unit}, {self.order})'

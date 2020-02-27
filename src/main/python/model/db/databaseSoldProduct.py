from model.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DatabaseSoldProduct(Base):
	__tablename__ = 'soldProduct'
	id = Column(Integer(), primary_key = True)
	amount = Column(Integer())
	unit = Column(String())
	product_id = Column(Integer(), ForeignKey('product.id'))
	product = relationship('DatabaseProduct')

	order_id = Column(Integer(), ForeignKey('order.id'))
	order = relationship('DatabaseOrder')


	def __repr__(self):
		return f'DatabaseSoldProduct({self.id}, {self.amoun}, {self.product}, {self.unit}, {self.order})'

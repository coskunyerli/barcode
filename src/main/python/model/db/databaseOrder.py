from model.db.base import Base
from sqlalchemy import Integer, Column, DateTime
from sqlalchemy.orm import relationship


class DatabaseOrder(Base):
	__tablename__ = 'order'
	id = Column(Integer(), primary_key = True)
	created_date = Column(DateTime())
	soldProducts = relationship('DatabaseSoldProduct', backref = 'orders')


	def __repr__(self):
		return f'DatabaseOrder({self.id}, {self.created_date}, {self.product}, {self.unit}, {self.order})'

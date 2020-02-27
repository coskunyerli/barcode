from model.db.base import Base
from model.db.databaseOrder import DatabaseOrder
from model.db.databaseSoldProduct import DatabaseSoldProduct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship


class DatabaseServiceModel(object):
	def __init__(self):
		engine = create_engine(f'sqlite:///database.db', echo = True)
		Session = sessionmaker(bind = engine)
		self.session = Session()
		Base.metadata.create_all(engine)


	def rollback(self):
		self.session.rollback()


	def commit(self):
		self.session.commit()


	def add(self, data):
		self.session.add(data.toDatabase())


	def delete(self, data):
		self.session.delete(data.toDatabase())


	def save(self, data):
		self.add(data)
		self.commit()


	def query(self, dataClass):
		return self.session.query(dataClass.getClass())


	def flush(self):
		self.session.flush()


_databaseServiceModel = DatabaseServiceModel()


class DatabaseService(object):

	def databaseService(self):
		return _databaseServiceModel

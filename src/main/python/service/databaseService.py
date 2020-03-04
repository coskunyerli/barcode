import traceback

from model.db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseServiceModel(object):
	def __init__(self):
		engine = create_engine(f'sqlite:///database.db', echo = True)
		Session = sessionmaker(bind = engine)
		self.session = Session()
		Base.metadata.create_all(engine)


	def rollback(self):
		try:
			self.session.rollback()
			return True
		except Exception as e:
			return False


	def commit(self):
		try:
			self.session.commit()
			return True
		except Exception as e:
			traceback.print_exc()
			return False


	def add(self, data):
		self.session.add(data.toDatabase())


	def add_all(self, arr):
		self.session.add_all(list(map(lambda object: object.toDatabase(), arr)))


	def delete(self, data):
		self.session.delete(data.toDatabase())


	def save(self, data):
		self.add(data)
		return self.commit()


	def query(self, dataClass):
		query = self.session.query(dataClass.getClass())
		return query


	def flush(self):
		try:
			self.session.flush()
			return False
		except Exception as e:
			return False


_databaseServiceModel = None


class DatabaseService(object):

	def databaseService(self):
		return _databaseServiceModel

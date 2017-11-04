from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, \
	Float, Boolean

from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	name = Column(String(20), nullable = False)
	legal_name = Column(String(30), nullable = False)
	password = Column(String(20), nullable = False)
	school_name = Column(String(20), nullable = False)
	phone_number = Column(String(12), nullable = False)
	profile = Column(String(200), nullable = True)


class Day(Base):
	__tablename__ = 'dayTime'
	id = Column(Integer, primary_key = True)
	time = Column(Integer, nullable = False)
	day = Column(Integer, nullable = False)
	available_location = Column(String(100), nullable = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


# class Time(Base):
#	_tablename_= 'Time'
#	id = Column(Integer, primary_key = True)
#	user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
#	user = relationship(User)

engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
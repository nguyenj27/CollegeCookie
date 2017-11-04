from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, \
	Float, Boolean

from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	password = Column(String(250), nullable = False)
	school_name = Column(String(50), nullable = False)
	breakfast = Column(Integer, nullable = True)
	lunch = Column(Integer, nullable = True)
	dinner = Column(Integer, nullable = True)
	profile = Column(String(200), nullable = True)


# class Time(Base):
#	_tablename_= 'Time'
#	id = Column(Integer, primary_key = True)
#	user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
#	user = relationship(User)

engine = create_engine('sqlite:///main.db')
Base.metadata.create_all(engine)
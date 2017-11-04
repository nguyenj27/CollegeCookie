from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, \
	Float, Boolean

from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	_tablename_ = 'user'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	password = Column(String(250), nullable = False)
	school_name = Column(String(50), nullable = False)
	breakfast = Column(Float, nullable = True)
	lunch = Column(Float, nullable = True)
	dinner = Column(Float, nullable = True)

# class Time(Base):
#	_tablename_= 'Time'
#	id = Column(Integer, primary_key = True)
#	user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
#	user = relationship(User)

engine = create_engine('sqlite:///main.db')
Base.metadate.create_all(engine)
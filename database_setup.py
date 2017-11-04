from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, DateTime, func, Boolean, \
	Float
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	_tablename_ = 'user'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	password = Column(String(250), nullable = False)
	school_name = Column(String(50), nullable = False)


class Time(Base):
	_tablename_= 'Time'
	interval = Column(Integer, primary_key = True)
	breakfast = Column(float, nullable = False)

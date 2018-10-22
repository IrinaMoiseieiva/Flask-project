from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    city = Column(String(32))
    count_of_workers = Column(String(32))

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    education = Column(String(32))
    passport = Column(String(32))
    city = Column(String(32))
    age = Column(Integer)

    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", backref=backref("clients", order_by=id))

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    suma = Column(Integer)
    credit_state = Column(String(32))
    currency = Column(String(32))
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", backref=backref("applications", order_by=id))

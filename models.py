from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, Float
from database import Base

class Employee(Base):
    __tablename__  = 'employees'

    employeeid = Column(Integer, primary_key = True, index = True)
    firstname = Column(String, index = True)
    lastname = Column(String, index = True)
    birthdate = Column(Date, index = True)
    hiredate = Column(DateTime, index = True)
    salary = Column(Float, index = True)
    isactive = Column(Boolean, index = True)
    email = Column(String, index = True)
    phonenumber = Column(Integer, index = True)

# class EmployeeCreate(Base):
#     firstName = Column(String, index = True)
#     lastName = Column(String, index = True)
#     birthDate = Column(Date, index = True)
#     hireDate = Column(DateTime, index = True)
#     salary = Column(Float, index = True)
#     isActive = Column(Boolean, index = True)
#     email = Column(String, index = True)
#     phoneNumber = Column(String, index = True)

# class EmployeeUpdate(Base):
#     firstName = Column(String, index = True)
#     lastName = Column(String, index = True)
#     birthDate = Column(Date, index = True)
#     hireDate = Column(DateTime, index = True)
#     salary = Column(Float, index = True)
#     isActive = Column(Boolean, index = True)
#     email = Column(String, index = True)
#     phoneNumber = Column(String, index = True)



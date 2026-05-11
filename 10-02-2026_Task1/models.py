from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)#primary key & auto increment
    name = Column(String, nullable=False)# non empty
    email = Column(String, unique=True, nullable=False, index=True)#unique and non empty
    department = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)#Status of an employee
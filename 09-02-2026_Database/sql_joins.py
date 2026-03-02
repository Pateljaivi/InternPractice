from sqlalchemy import create_engine,Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base,relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = 'Departments'
    DeptId = Column(Integer, primary_key=True)
    DeptName = Column(String)

class Employee(Base):
    __tablename__ = 'Employees'
    EmployeeId = Column(Integer, primary_key=True)
    Name = Column(String)
    DeptID = Column(Integer, ForeignKey('Departments.DeptId'))
    department = relationship("Department")

engine = create_engine(
     "mssql+pyodbc://@localhost/JoinsDB"
    "?driver=ODBC+Driver+17+for+SQL+Server" 
    "&trusted_connection=yes"
)

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(Employee).join(Department).all()

for emp in results:
    print(emp.EmployeeId,emp.Name,emp.department.DeptName)


session.close()



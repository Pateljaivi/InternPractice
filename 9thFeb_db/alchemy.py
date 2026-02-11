from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    completed = Column(Boolean)

    def __repr__(self):
        return f"Task(id={self.id},title={self.title})"

engine = create_engine(
    "mssql+pyodbc://@localhost/StudentDB"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)


Session = sessionmaker(bind=engine)
session = Session()

task = session.query(Task).filter_by(title='Call the bank').first()
print(task)




session.close()
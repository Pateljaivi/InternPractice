# from sqlalchemy import create_engine,Column,Integer,String,Boolean
# from sqlalchemy.orm import sessionmaker,declarative_base
#
# Base = declarative_base()
#
# class Task(Base):
#     __tablename__ = 'task'
#     id = Column(Integer,primary_key=True)
#     title = Column(String)
#     completed = Column(Boolean)
#
#     def __repr__(self):
#         return f"Task(id={self.id},title={self.title})"
#
# engine = create_engine(
#     "mssql+pyodbc://@localhost/StudentDB"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
#     "&trusted_connection=yes"
# )
#
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# task = session.query(Task).filter_by(title='Call the bank').first()
# print(task)
#
#
#
#
# session.close()

#my example

from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base

Base = declarative_base()

class Cricket2(Base):
    __tablename__ = 'Cricket2'
    player_id = Column(Integer,primary_key=True)
    name = Column(String)
    points = Column(Boolean)

    def __repr__(self):
        return f"Cricket(player_id={self.player_id},player_name={self.name},points={self.points})"

engine = create_engine(
    "mssql+pyodbc://@localhost/CricketDB"
    "?driver=ODBC+Driver+17+for+SQL+Server" 
    "&trusted_connection=yes"
)

Session = sessionmaker(bind=engine)# Creates a 'Session' class factory linked to our engine
session = Session()# Creates an actual workspace (the session) for database operations

cri = session.query(Cricket2).filter_by(name="Axar Patel").first()
#Generate select * from cricket2 command,adds where name = 'Axar Patel' clause,limits the result to just one row.If no player is found,it returns None.

print(cri)

#Triggers the __repr__ method you defined earlier to display the data nicely


session.close()
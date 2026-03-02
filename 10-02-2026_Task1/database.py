from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DATABASE_URL = (
    "mssql+pyodbc://@localhost/EmployeeDB"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)  #address of db url ->fastapi will understand which db,which driver used

engine = create_engine(DATABASE_URL, echo=False)#engine -> bridge between backend aur database
SessionLocal = sessionmaker(bind=engine)
#for every api there is a create new session

Base = declarative_base()
#->every model inherit from this base
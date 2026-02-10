from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def fetch_all(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)

@app.get("/employees/{id}", response_model=schemas.EmployeeResponse)
def fetch_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_employee(db, id)

@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, emp)

@app.put("/employees/{id}", response_model=schemas.EmployeeResponse)
def update(id: int, emp: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    return crud.update_employee(db, id, emp)

@app.patch("/employees/{id}/status")
def change_status(id: int, is_active: bool, db: Session = Depends(get_db)):
    emp = crud.update_status(db, id, is_active)
    return {"message": "Status updated", "is_active": emp.is_active}

@app.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    crud.delete_employee(db, id)
from sqlalchemy.orm import Session
import models, schemas, exceptions

def get_all_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee(db: Session, emp_id: int):
    employee = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not employee:
        exceptions.employee_not_found()
    return employee

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    if db.query(models.Employee).filter(models.Employee.email == employee.email).first():
        exceptions.duplicate_email()

    emp = models.Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def update_employee(db: Session, emp_id: int, data: schemas.EmployeeUpdate):
    emp = get_employee(db, emp_id)
    for key, value in data.dict().items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

def update_status(db: Session, emp_id: int, status: bool):
    emp = get_employee(db, emp_id)
    emp.is_active = status
    db.commit()
    return emp

def delete_employee(db: Session, emp_id: int):
    emp = get_employee(db, emp_id)
    db.delete(emp)
    db.commit()

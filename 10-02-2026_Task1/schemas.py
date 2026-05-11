from pydantic import BaseModel, EmailStr, Field

#pydantic->for data validation


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr #automatically check email is in proper format or not
    department: str
    salary: float = Field(gt=0) #salary must be grater than zero
    phone_number: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
#in response ID and status
    class Config:
        orm_mode = True #SQLAlchemy object ko JSON me convert karne ke liye


#this file for validate incoming aur outgoing data
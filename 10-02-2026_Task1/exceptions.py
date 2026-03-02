from fastapi import HTTPException, status

def employee_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

def duplicate_email():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email already exists"
    )  #if same email exists raise an error


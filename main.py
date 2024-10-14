from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Annotated, Optional
from pydantic_extra_types.phone_numbers import PhoneNumber
import models
# from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
import database

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

class Employee(BaseModel):
    employeeID: int
    firstName: str
    lastName: str
    birthDate: date
    hireDate: datetime
    salary: float
    isActive: bool
    email: EmailStr
    phoneNumber: int

class EmployeeCreate(BaseModel):
    firstName: str
    lastName: str
    birthDate: date
    hireDate: datetime
    salary: float
    isActive: bool
    email: EmailStr
    phoneNumber: int

# class EmployeeCreate(BaseModel):
#     firstName: str
#     lastName: str
#     birthDate: date
#     hireDate: datetime
#     salary: float
#     isActive: bool
#     email: EmailStr
#     phoneNumber: PhoneNumber

# class EmployeeUpdate(BaseModel):
#     firstName: Optional[str]
#     lastName: Optional[str]
#     birthDate: Optional[date]
#     hireDate: Optional[datetime]
#     salary: Optional[float]
#     isActive: Optional[bool]
#     email: Optional[EmailStr]
#     phoneNumber: Optional[PhoneNumber]

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

# @app.get("/employeesAll/")
# async def read_all_employees(db: db_dependency):
#     result = db.query(models.Employee).all()
#     if not result:
#         raise HTTPException(status_code=404, detail='Employee does not exist')
#     else:
#         return result

# @app.get("/employeesById/{Id}")
# async def read_employees(Id: int, db: db_dependency):
#     result = db.query(models.Employee).filter(models.Employee.employeeid == Id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail='Employee does not exist')
#     else:
#         return result
    
# @app.post("/employeesCreate/")
# async def create_employee(employee: Employee, db: db_dependency):
#     db_firstname = models.Employee(firstname=employee.firstName)
#     db_lastname = models.Employee(lastname=employee.lastName)
#     db_birthdate = models.Employee(birthdate=employee.birthDate)
#     db_hiredate = models.Employee(hiredate=employee.hireDate)
#     db_salary = models.Employee(salary=employee.salary)
#     db_isActive = models.Employee(isActive=employee.isActive)
#     db_email = models.Employee(email=employee.email)
#     db_phoneNumber = models.Employee(phoneNumber=employee.phoneNumber)

#     db.add(db_firstname)
#     db.add(db_lastname)

def get_db():
    return database.get_db_connection()

@app.get("/employeesAll/")
async def read_all_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    results = cur.fetchall()

    if not results:
        raise HTTPException(status_code=404, detail='Employee does not exist')
    conn.close()

    columns = [desc[0] for desc in cur.description]
    employees = []
    for result in results:
        employee = dict(zip(columns, result))
        employees.append(employee)
    return employees


@app.get("/employeesById/{Id}")
async def read_employees(Id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employeeid = %s", (Id,))
    result = cur.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail='Employee does not exist')
    conn.close()
    
    columns = [desc[0] for desc in cur.description]
    employee = dict(zip(columns, result))
    return employee

@app.post("/employeesCreate/")
async def create_employee(employee: EmployeeCreate):
    conn = get_db()
    cur = conn.cursor()

    """{
        "firstName": "Emily",
        "lastName": "Chen",
        "birthDate": "1992-06-15",
        "hireDate": "2018-03-01T09:00:00",
        "salary": 60000.0,
        "isActive": false,
        "email": "emily.chen@example.com",
        "phoneNumber": 19876543210
    }"""
    cur.execute("""
        INSERT INTO employees (firstname, lastname, birthdate, hiredate, salary, isactive, email, phonenumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            employee.firstName,
            employee.lastName,
            employee.birthDate,
            employee.hireDate,
            employee.salary,
            employee.isActive,
            employee.email,
            employee.phoneNumber
        ))
    conn.commit()
    conn.close()
    return {"message": "Employee created successfully"}


    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


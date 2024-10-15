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
import psycopg2.extras 
import json

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

class EmployeeUpdate(BaseModel):
    firstName: Optional[str] = 'null'
    lastName: Optional[str] = 'null'
    birthDate: Optional[date] = 'null'
    hireDate: Optional[datetime] = 'null'
    salary: Optional[float] = 0
    isActive: Optional[bool] = False
    email: Optional[EmailStr] = 'null'
    phoneNumber: Optional[int] = 0

def get_db():
    return database.get_db_connection()

@app.get("/employeesAll/")
async def read_all_employees() -> list:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM employees")
    results = cur.fetchall()

    if not results:
        raise HTTPException(status_code=404, detail='Employee does not exist')
    conn.close()

    employees = json.dumps(results, default=str)
    # print(type(json.loads(employees)))
    return json.loads(employees)


@app.get("/employeesById/{Id}")
async def read_employees(Id: int) -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM employees WHERE employeeid = %s", (Id,))
    result = cur.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail='Employee does not exist')
    conn.close()

    employees = json.dumps(result, default=str)
    print(type(json.loads(employees)))
    return json.loads(employees)

@app.post("/employeesCreate/")
async def create_employee(employee: EmployeeCreate) -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
        INSERT INTO public.employees (firstname, lastname, birthdate, hiredate, salary, isactive, email, phonenumber)
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
    conn.close()

    conn.commit()
    conn.close()
    return {"message": "Employee created successfully"}

@app.put("/employeesUpdate/{Id}")
async def update_employee(Id: int, employee: EmployeeUpdate) -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
        UPDATE public.employees
        SET firstname=%s, lastname=%s, birthdate=%s, hiredate=%s, salary=%s, isactive=%s, email=%s, phonenumber=%s
        WHERE employeeid=%s;        
        """, (
            employee.firstName,
            employee.lastName,
            employee.birthDate,
            employee.hireDate,
            employee.salary,
            employee.isActive,
            employee.email,
            employee.phoneNumber,
            Id
        ))
    conn.commit()
    conn.close()
    return {"message": f"Employee {Id} updated successfully"}

@app.delete("/employeesDelete/{Id}")
async def delete_employee(Id: int) -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
        DELETE FROM public.employees
        WHERE employeeid=%s;        
        """, (Id, ))
    conn.commit()
    conn.close()
    return {"message": f"Employee {Id} deleted successfully"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Annotated, Optional
import uvicorn
import database
import psycopg2.extras 
import json
from psycopg2 import Error

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
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    birthDate: Optional[date] = None
    hireDate: Optional[datetime] = None
    salary: Optional[float] = 0
    isActive: Optional[bool] = False
    email: Optional[EmailStr] = None
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
    try:
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
        conn.commit()
        return {"message": "Employee created successfully"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        conn.close()
    
@app.put("/employeesUpdate/{Id}")
async def update_employee(Id: int, employee: EmployeeUpdate) -> dict:
    try:
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
        return {"message": f"Employee {Id} updated successfully"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        conn.close()
    

@app.delete("/employeesDelete/{Id}")
async def delete_employee(Id: int) -> dict:
    try:
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
        return {"message": f"Employee {Id} deleted successfully"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        conn.close()
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


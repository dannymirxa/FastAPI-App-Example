from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

class EmployeeCreate(BaseModel):
    firstName: str
    lastName: str
    birthDate: date
    hireDate: datetime
    salary: float
    isActive: bool
    email: EmailStr
    phoneNumber: PhoneNumber

class EmployeeUpdate(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    birthDate: Optional[date]
    hireDate: Optional[datetime]
    salary: Optional[float]
    isActive: Optional[bool]
    email: Optional[EmailStr]
    phoneNumber: Optional[PhoneNumber]

class EmployeeOut(BaseModel):
    employeeID: int
    firstName: str
    lastName: str
    birthDate: date
    hireDate: datetime
    salary: float
    isActive: bool
    email: EmailStr
    phoneNumber: PhoneNumber

    class Config:
        orm_mode = True
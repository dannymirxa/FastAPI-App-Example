from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm.session import sessionmaker
from typing import List
from schemas import EmployeeOut

router = APIRouter()

# Database connection settings
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/Employees"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

@router.get("/employees/", response_model=List[EmployeeOut])
async def read_employees():
    query = text("SELECT * FROM Employees")
    async with get_session() as session:
        result = await session.execute(query)
        return [dict(row) for row in result]
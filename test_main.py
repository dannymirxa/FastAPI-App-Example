import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app, get_db

client = TestClient(app)

# Mock database connection
@pytest.fixture
def mock_db():
    with patch('main.get_db') as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock_conn

def test_read_all_employees(mock_db):
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "employeeID": 1,
            "firstName": "John",
            "lastName": "Doe",
            "birthDate": "1990-01-01",
            "hireDate": "2020-01-01T09:00:00",
            "salary": 50000.0,
            "isActive": True,
            "email": "john.doe@example.com",
            "phoneNumber": 1234567890
        }
    ]
    
    response = client.get("/employeesAll/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "employeeID": 1,
            "firstName": "John",
            "lastName": "Doe",
            "birthDate": "1990-01-01",
            "hireDate": "2020-01-01T09:00:00",
            "salary": 50000.0,
            "isActive": True,
            "email": "john.doe@example.com",
            "phoneNumber": 1234567890
        }
    ]

def test_read_employee_by_id(mock_db):
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "employeeID": 1,
        "firstName": "John",
        "lastName": "Doe",
        "birthDate": "1990-01-01",
        "hireDate": "2020-01-01T09:00:00",
        "salary": 50000.0,
        "isActive": True,
        "email": "john.doe@example.com",
        "phoneNumber": 1234567890
    }
    
    response = client.get("/employeesById/1")
    assert response.status_code == 200
    assert response.json() == {
        "employeeID": 1,
        "firstName": "John",
        "lastName": "Doe",
        "birthDate": "1990-01-01",
        "hireDate": "2020-01-01T09:00:00",
        "salary": 50000.0,
        "isActive": True,
        "email": "john.doe@example.com",
        "phoneNumber": 1234567890
    }

def test_create_employee(mock_db):
    mock_cursor = mock_db.cursor.return_value
    
    response = client.post("/employeesCreate/", json={
        "firstName": "Emily",
        "lastName": "Chen",
        "birthDate": "1992-06-15",
        "hireDate": "2018-03-01T09:00:00",
        "salary": 60000.0,
        "isActive": False,
        "email": "emily.chen@example.com",
        "phoneNumber": 19876543210
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Employee created successfully"}

def test_update_employee(mock_db):
    mock_cursor = mock_db.cursor.return_value
    
    response = client.put("/employeesUpdate/1", json={
        "firstName": "Emily",
        "lastName": "Chen",
        "birthDate": "1992-06-15",
        "hireDate": "2018-03-01T09:00:00",
        "salary": 60000.0,
        "isActive": False,
        "email": "emily.chen@example.com",
        "phoneNumber": 19876543210
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Employee 1 updated successfully"}

def test_delete_employee(mock_db):
    mock_cursor = mock_db.cursor.return_value
    
    response = client.delete("/employeesDelete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Employee 1 deleted successfully"}

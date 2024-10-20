# FastAPI-App-Example

## 1. Objectives

### 1.1 To deploy a FASTApi app

### 1.2 To learn how to use Jenkins for automation

## 2. Custom Docker Images and Containers

### 2.1 Write the dockerfile

This dockerfile create a new PosgreSQL image and run `init.sql` during initialization.

```dockerfile
FROM postgres:latest

ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=Employees

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
```

This dockerfile run the FastAPI app.

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .

EXPOSE 8000

CMD ["python", "main.py"]

```

### 2.2 Build the docker images

```bash
docker build -f posgres-dockerfile -t employee-posgres . 
```

```bash
docker build -f fastapi-dockerfile -t fastapi-employee . 
```

### 2.3 Write the compose Yaml named posgres-compose.yaml

```yaml
services:
  postgres:
    image: employee-posgres
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=Employees
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
    container_name: employee_db
volumes:
  db-data:
```

### 2.4 Write the compose Yaml named fastapi-compose.yaml

```yaml
services:
  fastapi_app:
    image: fastapi-employee
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENV=production
    container_name: employee_app
```

### 2.4 Run the docker compose command

```bash
docker compose -f posgres-compose.yaml up
```

```bash
docker compose -f fastapi-compose.yaml up
```

## 3. Jenkins Steps

### 3.1 Build Simple Testing Pipeline

#### 3.1.1 Build a simple pipeline by clcking 'New Item'

<!-- ![alt text](./Images/Test%20Pipeline.png) -->

<img src="./Images/Test Pipeline Create.png" alt="Alt Text" width="1000">

#### 3.1.2 Write a Pipeline Script

For now just print 'Testing Pipeline with Jenkins'. Done forget to click 'Save'.

<img src="./Images/Test Pipeline Script.png" alt="Alt Text" width="1000">

#### 3.1.3 Click 'Build Now'

<img src="./Images/Test Pipeline Build.png" alt="Alt Text" width="500">

#### 3.1.4 Check the Build Result

<img src="./Images/Test Pipeline Build Result.png" alt="Alt Text" width="500">

#### 3.1.5 Check the Build Stage

<img src="./Images/Test Pipeline Stages.png" alt="Alt Text" width="500">

### 3.2 Build Simple Multi-Stage Testing Pipeline

#### 3.2.1 Just continue from Step 3.1.2, update the Pipline script

<img src="./Images/Test Pipeline Multistage Script.png" alt="Alt Text" width="500">

#### 3.2.2 Check the stages

<img src="./Images/Test Pipeline Multistage Stages.png" alt="Alt Text" width="500">
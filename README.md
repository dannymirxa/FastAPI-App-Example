# FastAPI App Example

## How to run

### 1. Create Docker Network

```docker
docker network create app-network
```

### 2. Run Docker Compose Posgres

```docker
docker compose -f posgres-compose.yaml up
```

### 3. Run Docker Compose FastAPI App

```docker
docker compose -f fastapi-compose.yaml up
```

## Architecture

<img src="./Architecture.png" style="width:600px;"/>
# Application Setup and Run Guide

This document outlines the steps to set up and run this FastAPI application

---

## Prerequisites

Ensure the following tools are installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Step 1: Clone the Repository

Clone the FastAPI application repository to your local machine:

```bash
git clone <repository_url>
cd <repository_name>
```
---

## Step 2: Update Environment Variables

- copy `.env.example` to `.env`
- configure as needed
---

## Step 3: Build and Start Docker Containers

The repository includes a `docker-compose.yml` file. Run the following commands to build and start the containers:

### Build the Containers

```bash
docker-compose build
```

### Start the Containers

```bash
docker-compose up -d
```

This will:

- Set up a PostgreSQL database container.
- Set up a FastAPI application container.
- Set up an Nginx container as a reverse proxy which can be accessed on localhost:8000.

---

### Verify Running Services

Check that all services are running:

```bash
docker-compose ps
```
You should see containers for the app, postgres, and nginx running.

---

## Step 4: Apply Alembic database migrations
Run following command to apply the migrations
```bash
docker-compose exec app alembic upgrade head
```

## Step 5: Access the Application

The application should now be accessible at `http://localhost:8000`

### API Documentation

FastAPI provides interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


### Endpoints
`/api/v1/auth/register`
`/api/v1/auth/token`
`/api/v1/auth/refresh`



---

## Step 6: Stopping the Application

To stop the application and associated containers, run:

```bash
docker-compose down
```

This will stop and remove all containers defined in the `docker-compose.yml` file.


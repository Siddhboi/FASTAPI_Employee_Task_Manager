# 🚀 Employee Task Manager API - Enterprise Edition

A **production-ready**, **enterprise-grade** FastAPI application for managing employees and tasks with advanced features including JWT authentication, PostgreSQL support, Docker deployment, and comprehensive API documentation.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Authentication](#-authentication)
- [API Endpoints](#-api-endpoints)
- [Advanced Usage](#-advanced-usage)
- [Docker Deployment](#-docker-deployment)
- [Database Migrations](#-database-migrations)
- [Environment Configuration](#-environment-configuration)
- [Testing](#-testing)

---

## ✨ Features

### Core Features
- ✅ **Complete CRUD Operations** for Employees and Tasks
- ✅ **Advanced Filtering & Search** with multiple parameters
- ✅ **Pagination** with metadata (total count, skip, limit)
- ✅ **Task Status Management** (pending, in_progress, completed)
- ✅ **Employee-Task Assignment** with relationship tracking

### Bonus Level 1 ✨
- ✅ **Advanced Filtering**: Filter by status, employee, role, search terms
- ✅ **Enhanced Pagination**: Includes total count and metadata
- ✅ **API Key Authentication**: Simple header-based security

### Bonus Level 2 🚀
- ✅ **PostgreSQL Support**: Production-grade database
- ✅ **Alembic Migrations**: Database schema versioning
- ✅ **Docker & Docker Compose**: Containerized deployment
- ✅ **Environment Configuration**: .env file support

### Bonus Level 3 🔐
- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **OAuth2 Compatible**: Industry-standard authentication
- ✅ **User Management**: Multiple user support with roles

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | Modern web framework |
| **SQLAlchemy** | 2.0.23 | ORM for database operations |
| **Pydantic** | 2.5.0 | Data validation |
| **PostgreSQL** | 15 | Production database |
| **SQLite** | - | Development database |
| **Alembic** | 1.13.0 | Database migrations |
| **JWT/OAuth2** | - | Authentication |
| **Docker** | - | Containerization |
| **Uvicorn** | 0.24.0 | ASGI server |

---

## 📁 Project Structure

```
fastapi_task/
│
├── main.py                      # Application entry point
├── config.py                    # Configuration management
├── database.py                  # Database connection & session
├── models.py                    # SQLAlchemy models
├── schemas.py                   # Pydantic schemas
├── auth.py                      # API Key authentication
├── jwt_auth.py                  # JWT authentication
├── sample_data.py               # Sample data generator
│
├── routers/
│   ├── __init__.py
│   ├── employees.py             # Employee endpoints
│   ├── tasks.py                 # Task endpoints
│   └── auth_router.py           # JWT auth endpoints
│
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .env                         # Your configuration (not in git)
│
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker services orchestration
├── .dockerignore
│
├── setup.sh                     # Linux/Mac setup script
├── setup.bat                    # Windows setup script
│
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Option 1: Local Development (SQLite)

#### **Windows:**
```cmd
# Run setup script
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sample_data.py
uvicorn main:app --reload
```

#### **Linux/Mac:**
```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python sample_data.py
uvicorn main:app --reload
```

### Option 2: Docker (Recommended for Production)

```bash
# Start PostgreSQL + API
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Access the API

- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Info**: http://localhost:8000/info

---

## 🔐 Authentication

This API supports **two authentication methods**:

### Method 1: API Key (Simple)

Add header to your requests:
```
X-API-Key: your-secret-api-key-12345
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","role":"Developer"}'
```

### Method 2: JWT Bearer Token (Advanced)

#### Step 1: Get Token
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Step 2: Use Token
```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","role":"Manager"}'
```

### Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin    | secret   | Admin |
| demo     | secret   | User |

---

## 📡 API Endpoints

### 🔓 Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/info` | API information |
| GET | `/employees/` | List all employees |
| GET | `/employees/{id}` | Get employee by ID |
| GET | `/tasks/` | List all tasks |
| GET | `/tasks/{id}` | Get task by ID |

### 🔐 Protected Endpoints (Authentication Required)

#### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/employees/` | Create employee |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |

#### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| POST | `/tasks/{id}/assign/{employee_id}` | Assign task |

#### Authentication (JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/token` | Get JWT token |
| GET | `/auth/me` | Get current user |
| GET | `/auth/test-token` | Test token validity |

---

## 🎯 Advanced Usage

### Filtering & Search

#### Filter Employees by Role
```bash
curl "http://localhost:8000/employees/?role=Developer"
```

#### Search Employees
```bash
curl "http://localhost:8000/employees/?search=john"
```

#### Filter Tasks by Status
```bash
curl "http://localhost:8000/tasks/?status=pending"
```

#### Filter Tasks by Employee
```bash
curl "http://localhost:8000/tasks/?employee_id=1"
```

#### Combined Filters
```bash
curl "http://localhost:8000/tasks/?status=in_progress&employee_id=1"
```

### Pagination

```bash
# Get first 10 items
curl "http://localhost:8000/employees/?skip=0&limit=10"

# Get next 10 items
curl "http://localhost:8000/employees/?skip=10&limit=10"
```

**Response includes metadata:**
```json
{
  "total": 25,
  "skip": 0,
  "limit": 10,
  "items": [...]
}
```

---

## 🐳 Docker Deployment

### Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up -d --build

# Stop services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

### Production

1. **Update environment variables** in `docker-compose.yml`
2. **Change default passwords** in `.env`
3. **Use production-grade secrets** for JWT and API keys
4. **Enable HTTPS** using reverse proxy (nginx/traefik)
5. **Set up proper backup** for PostgreSQL volume

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🗄 Database Migrations

### Using Alembic

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

### Switch to PostgreSQL

1. **Install PostgreSQL** locally or use Docker
2. **Update `.env` file:**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/employee_task_db
```
3. **Run migrations:**
```bash
alembic upgrade head
```
4. **Restart server:**
```bash
uvicorn main:app --reload
```

---

## ⚙️ Environment Configuration

### Create `.env` file

```bash
cp .env.example .env
```

### Configuration Options

```env
# Database (choose one)
DATABASE_URL=sqlite:///./employee_task_manager.db
# DATABASE_URL=postgresql://user:pass@host:5432/dbname

# PostgreSQL (if using)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=employee_task_db

# Security
API_KEY=your-secret-api-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# Application
APP_NAME=Employee Task Manager API
APP_VERSION=2.0.0
DEBUG=True
```

### Environment Priority

1. Environment variables (highest priority)
2. `.env` file
3. Default values in `config.py`

---

## 🧪 Testing

### Manual Testing with Swagger UI

1. Open http://localhost:8000/
2. Try out endpoints interactively
3. Use "Authorize" button for authentication

### Using cURL

**Create Employee:**
```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "role": "Senior Developer"
  }'
```

**Create Task:**
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement Feature X",
    "description": "Add new feature to the application",
    "status": "pending",
    "employee_id": 1
  }'
```

**Assign Task:**
```bash
curl -X POST "http://localhost:8000/tasks/1/assign/2" \
  -H "X-API-Key: your-secret-api-key-12345"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-12345"
headers = {"X-API-Key": API_KEY}

# Create employee
employee = {
    "name": "Bob Smith",
    "email": "bob@example.com",
    "role": "QA Engineer"
}
response = requests.post(f"{BASE_URL}/employees/", json=employee, headers=headers)
print(response.json())

# Get all employees
response = requests.get(f"{BASE_URL}/employees/")
print(response.json())
```

---

## 📊 Sample Data

Run the sample data script to populate your database:

```bash
python sample_data.py
```

This creates:
- 10 employees with various roles
- 12 tasks with different statuses
- Task assignments to employees

---

## 🔒 Security Best Practices

1. **Change default credentials** immediately
2. **Use strong API keys** (32+ characters)
3. **Use environment variables** for secrets
4. **Enable HTTPS** in production
5. **Implement rate limiting** (using FastAPI-Limiter)
6. **Add request validation** (already implemented with Pydantic)
7. **Use PostgreSQL** in production (not SQLite)
8. **Regular security updates** of dependencies
9. **Implement proper logging** and monitoring
10. **Add input sanitization** for search queries

---

## 🚦 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-endpoint

# 2. Make changes

# 3. Test locally
uvicorn main:app --reload

# 4. Create migration if needed
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# 5. Commit changes
git add .
git commit -m "feat: add new endpoint"

# 6. Push and create PR
git push origin feature/new-endpoint
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com

---

## 🎉 Acknowledgments

- FastAPI framework
- SQLAlchemy ORM
- Pydantic validation
- All open-source contributors

---

**Built with ❤️ using FastAPI**

---

## ✅ Complete Feature Checklist

### Core Requirements
- [x] FastAPI server runs without errors
- [x] All endpoints work correctly
- [x] Swagger docs show all APIs
- [x] Proper Pydantic validation
- [x] Clean folder structure
- [x] Sample data script (10+ employees and tasks)
- [x] README with setup instructions
- [x] Clear commit message structure
- [x] Code readability
- [x] Type hints used throughout
- [x] Error handling (HTTPException)
- [x] No hard-coded paths
- [x] Modular router structure

### Bonus Level 1
- [x] Advanced task filtering (`/tasks?status=pending`)
- [x] Enhanced pagination with metadata
- [x] API key authentication

### Bonus Level 2
- [x] PostgreSQL support with SQLAlchemy
- [x] Alembic migrations
- [x] Docker & Docker Compose setup

### Bonus Level 3
- [x] JWT authentication
- [x] OAuth2 compatible
- [x] User management system

---

**Last Updated:** 2025  
**Version:** 2.0.0 (Enterprise Edition)
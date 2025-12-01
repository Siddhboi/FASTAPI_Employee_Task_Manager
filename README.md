# FASTAPI_Employee_Task_Manager
Enterprise-grade Employee &amp; Task Management REST API with JWT + API Key auth, PostgreSQL, Docker, Alembic migrations, and React dashboard

# 🚀 FastAPI Employee Task Manager - Enterprise Edition

A complete, production-ready RESTful API for managing employees and tasks with advanced features including dual authentication, database migrations, Docker deployment, and a beautiful React dashboard.

## ✨ Key Features

- **🔐 Dual Authentication**: JWT Bearer Token + API Key authentication
- **👥 User Management**: Registration, login, role-based access (Admin/Client)
- **💼 Employee Management**: Full CRUD operations with advanced filtering
- **✅ Task Management**: Create, assign, track, and update tasks
- **🗄️ Database Support**: SQLite (dev) & PostgreSQL (production)
- **🔄 Alembic Migrations**: Automatic schema versioning and migration
- **🐳 Docker Ready**: Complete containerization with docker-compose
- **🎨 React Dashboard**: Beautiful, responsive UI to consume the API
- **📊 Advanced Features**: Pagination, filtering, search, role-based permissions
- **📚 Auto Documentation**: Swagger UI and ReDoc included

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.104.1, Python 3.8+
- **Database**: PostgreSQL 15 / SQLite
- **ORM**: SQLAlchemy 2.0.23
- **Migrations**: Alembic 1.13.0
- **Authentication**: JWT (python-jose), BCrypt
- **Containerization**: Docker & Docker Compose
- **Frontend**: React 18 (single-file dashboard)
- **Documentation**: Swagger UI, ReDoc

## 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/fastapi-employee-task-manager.git
cd fastapi-employee-task-manager

# Setup and run
python start.py

# Or with Docker
docker-compose up -d
```

Access at: http://localhost:8000

## 📖 Documentation

- Full API docs at `/` (Swagger UI)
- Authentication guide in `AUTHENTICATION_GUIDE.md`
- Docker setup in `DOCKER_SETUP.md`
- Alembic migrations in `ALEMBIC_GUIDE.md`

## 🔐 Authentication

Two methods supported:
1. **JWT Bearer Token** - For web/mobile apps
2. **API Key** - For server-to-server

Default credentials:
- Admin: `admin` / `admin123`
- Client: `client` / `client123`
- API Key: `your-secret-api-key-12345`

## 🎯 Use Cases

- Employee & HR management systems
- Project task tracking
- Team collaboration tools
- Workflow management
- Learning FastAPI best practices
- Production-ready API template

## 📦 What's Included

✅ Complete FastAPI backend with all CRUD operations
✅ JWT + API Key dual authentication system
✅ Role-based access control (Admin/Client)
✅ Database migrations with Alembic
✅ Docker & Docker Compose configuration
✅ PostgreSQL support for production
✅ Sample data generation scripts
✅ React dashboard for API consumption
✅ Comprehensive documentation
✅ Production-ready code structure

## 🏆 Perfect For

- Learning advanced FastAPI concepts
- Building production APIs
- Microservices architecture
- Team projects
- Portfolio projects
- Startup MVPs

## 📄 License

MIT License - Free to use for personal and commercial projects

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## ⭐ Support

If this project helped you, please give it a star!
```

---

## **🏷️ GitHub Topics/Tags:**

Add these topics to your repository:

fastapi
python
rest-api
jwt-authentication
postgresql
docker
docker-compose
sqlalchemy
alembic
react
employee-management
task-management
api-key
swagger
oauth2
enterprise
microservices
```
backend
full-stack
production-ready

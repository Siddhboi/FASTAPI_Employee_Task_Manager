from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import employees, tasks, auth_router
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    A comprehensive **Enterprise-Grade API** for managing employees and their tasks.
    
    ## 🎯 Features
    
    * **Employee Management**: Full CRUD operations with advanced filtering and search
    * **Task Management**: Create, update, assign, and track tasks with status management
    * **Authentication**: 
        - API Key authentication for basic security
        - JWT (Bearer token) authentication for advanced use cases
    * **Advanced Filtering**: Search and filter by multiple parameters
    * **Pagination**: Efficient data retrieval with metadata
    * **Database Support**: SQLite (default) or PostgreSQL
    * **Docker Ready**: Containerized deployment with Docker Compose
    * **Database Migrations**: Alembic support for schema management
    
    ## 🔐 Authentication Methods
    
    ### Method 1: API Key (Simple)
    Add header: `X-API-Key: your-secret-api-key-12345`
    
    ### Method 2: JWT Bearer Token (Advanced)
    1. Get token from `/auth/token` endpoint
    2. Use credentials: `admin`/`secret` or `demo`/`secret`
    3. Add header: `Authorization: Bearer <your_token>`
    
    ## 🚀 Quick Start
    
    1. **Public Endpoints** (No auth required):
       - GET /employees/
       - GET /employees/{id}
       - GET /tasks/
       - GET /tasks/{id}
       - GET /health
    
    2. **Protected Endpoints** (Require auth):
       - All POST, PUT, DELETE operations
    
    ## 📚 Tech Stack
    
    * FastAPI + Uvicorn
    * SQLAlchemy ORM
    * PostgreSQL / SQLite
    * Alembic Migrations
    * JWT Authentication
    * Docker & Docker Compose
    """,
    version=settings.APP_VERSION,
    docs_url="/",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(employees.router)
app.include_router(tasks.router)

@app.get("/health", tags=["✅ Health Check"])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Employee Task Manager API is running successfully! 🚀",
        "authentication": "JWT Bearer Token"
    }

@app.get("/info", tags=["ℹ️ Information"])
def api_info():
    """
    Get API information and authentication instructions
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "authentication": {
            "methods": {
                "jwt": {
                    "type": "JWT Bearer Token",
                    "description": "Token-based authentication for web/mobile apps",
                    "steps": [
                        "1. POST /auth/login with credentials",
                        "2. Copy the access_token from response",
                        "3. Click 'Authorize' → Select 'HTTPBearer'",
                        "4. Enter your token (without 'Bearer' prefix)",
                        "5. Click Authorize"
                    ],
                    "demo_users": {
                        "note": "Run create_default_users.py first",
                        "admin": {"username": "admin", "password": "admin123"},
                        "client": {"username": "client", "password": "client123"}
                    },
                    "header": "Authorization: Bearer <token>"
                },
                "api_key": {
                    "type": "API Key",
                    "description": "Simple key-based auth for server-to-server",
                    "steps": [
                        "1. Click 'Authorize' → Select 'APIKeyHeader'",
                        "2. Enter: your-secret-api-key-12345",
                        "3. Click Authorize"
                    ],
                    "default_key": "your-secret-api-key-12345",
                    "header": "X-API-Key: <your_key>",
                    "access": "Admin privileges"
                }
            },
            "priority": "If both JWT and API Key are provided, JWT takes precedence"
        },
        "roles": {
            "admin": {
                "description": "Full access to all endpoints",
                "auth_methods": ["JWT (admin user)", "API Key"]
            },
            "client": {
                "description": "Can create and update, but not delete",
                "auth_methods": ["JWT (client user)"]
            }
        },
        "documentation": {
            "swagger": "/",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
🐳 Docker Setup Guide - Complete & Error-Free
🎯 Prerequisites
Docker Desktop installed and running
Windows: Download Docker Desktop
Mac: Download Docker Desktop
Linux: Install Docker Engine and Docker Compose
Verify Docker is running:
bash
docker --version
docker-compose --version
🚀 Quick Start (3 Commands)
bash
# 1. Build and start everything
docker-compose up --build -d

# 2. Check if containers are running
docker-compose ps

# 3. View logs
docker-compose logs -f api
That's it! Your API is now running at: http://localhost:8000

📋 Step-by-Step Setup
Step 1: Prepare Your Project
Make sure you have all these files:

fastapi_task/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── jwt_auth.py
├── create_default_users.py
├── sample_data.py
├── routers/
│   ├── __init__.py
│   ├── employees.py
│   ├── tasks.py
│   └── auth_router.py
└── .dockerignore
Step 2: Build Docker Images
bash
docker-compose build
This will:

✅ Pull PostgreSQL image
✅ Build your FastAPI application image
✅ Install all Python dependencies
Expected output:

[+] Building 45.2s (15/15) FINISHED
 => [api internal] load build definition from Dockerfile
 => [api] building...
 => Successfully built abc123def456
 => Successfully tagged fastapi_task_api:latest
Step 3: Start Containers
bash
docker-compose up -d
The -d flag runs containers in detached mode (background).

What happens:

✅ PostgreSQL container starts
✅ Waits for PostgreSQL to be ready
✅ Creates database tables
✅ Creates default users (admin, client)
✅ Creates sample data
✅ Starts FastAPI server
Expected output:

[+] Running 3/3
 ✔ Network fastapi_task_app-network  Created
 ✔ Container employee_task_postgres   Started
 ✔ Container employee_task_api        Started
Step 4: Verify Everything is Running
bash
docker-compose ps
Expected output:

NAME                      STATUS          PORTS
employee_task_postgres    Up 30 seconds   0.0.0.0:5432->5432/tcp
employee_task_api         Up 25 seconds   0.0.0.0:8000->8000/tcp
Both containers should show "Up" status.

Step 5: Check Logs
bash
# View all logs
docker-compose logs

# Follow API logs
docker-compose logs -f api

# Follow PostgreSQL logs
docker-compose logs -f postgres
Successful startup logs should show:

api  | Waiting for PostgreSQL to be ready...
api  | PostgreSQL is ready!
api  | Creating database tables...
api  | ✅ Database tables created
api  | Creating default users...
api  | ✅ Default users created successfully!
api  | Creating sample data...
api  | ✅ Sample data created successfully!
api  | Starting API server...
api  | INFO: Uvicorn running on http://0.0.0.0:8000
api  | INFO: Application startup complete.
🧪 Testing the Setup
1. Health Check
bash
curl http://localhost:8000/health
Expected response:

json
{
  "status": "healthy",
  "app_name": "Employee Task Manager API",
  "version": "2.0.0",
  "message": "Employee Task Manager API is running successfully! 🚀",
  "authentication": "JWT Bearer Token"
}
2. Login with Default User
bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
Expected response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "is_active": true
  }
}
3. Access Swagger UI
Open browser: http://localhost:8000/

🔧 Useful Docker Commands
View Running Containers
bash
docker-compose ps
View Logs
bash
# All logs
docker-compose logs

# Specific service
docker-compose logs api
docker-compose logs postgres

# Follow logs (live)
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api
Restart Services
bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
docker-compose restart postgres
Stop Containers
bash
# Stop but keep containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers and volumes (CAUTION: deletes data!)
docker-compose down -v
Rebuild After Code Changes
bash
# Rebuild and restart
docker-compose up --build -d

# Force rebuild (no cache)
docker-compose build --no-cache
docker-compose up -d
Execute Commands Inside Container
bash
# Access API container shell
docker exec -it employee_task_api bash

# Access PostgreSQL
docker exec -it employee_task_postgres psql -U postgres -d employee_task_db

# Run Python script
docker exec -it employee_task_api python create_default_users.py
🔍 Troubleshooting
Problem: Port 5432 already in use
Solution 1: Stop local PostgreSQL

bash
# Windows
net stop postgresql

# Linux/Mac
sudo systemctl stop postgresql
Solution 2: Change port in docker-compose.yml

yaml
postgres:
  ports:
    - "5433:5432"  # Change to 5433
Problem: Port 8000 already in use
Solution: Change port in docker-compose.yml

yaml
api:
  ports:
    - "8001:8000"  # Change to 8001
Then access at: http://localhost:8001

Problem: Container keeps restarting
Check logs:

bash
docker-compose logs api
Common causes:

Database connection failed
Python syntax error
Missing dependencies
Solution:

bash
# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
Problem: Database connection error
Error message:

sqlalchemy.exc.OperationalError: could not connect to server
Solution:

bash
# Check if postgres is healthy
docker-compose ps

# Restart postgres
docker-compose restart postgres

# Wait a moment and restart api
docker-compose restart api
Problem: Default users not created
Solution: Run manually

bash
docker exec -it employee_task_api python create_default_users.py
Problem: Cannot access from browser
Checklist:

✅ Containers running? docker-compose ps
✅ Correct URL? http://localhost:8000
✅ Firewall blocking? Check Windows Firewall
✅ Docker Desktop running? Check system tray
Problem: Changes not reflected
Solution: Rebuild

bash
docker-compose down
docker-compose up --build -d
🗄️ Database Management
Access PostgreSQL CLI
bash
docker exec -it employee_task_postgres psql -U postgres -d employee_task_db
Useful PostgreSQL commands:

sql
-- List all tables
\dt

-- View users table
SELECT * FROM users;

-- View employees table
SELECT * FROM employees;

-- View tasks table
SELECT * FROM tasks;

-- Count records
SELECT COUNT(*) FROM users;

-- Exit
\q
Backup Database
bash
docker exec employee_task_postgres pg_dump -U postgres employee_task_db > backup.sql
Restore Database
bash
docker exec -i employee_task_postgres psql -U postgres -d employee_task_db < backup.sql
Reset Database
bash
# Stop containers and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d
🔒 Security Considerations
Change Default Passwords
Edit docker-compose.yml:

yaml
environment:
  POSTGRES_PASSWORD: YOUR_SECURE_PASSWORD_HERE
  DATABASE_URL: postgresql://postgres:YOUR_SECURE_PASSWORD_HERE@postgres:5432/employee_task_db
Change JWT Secret
yaml
environment:
  JWT_SECRET_KEY: your-new-secret-key-here
Production Recommendations
✅ Use Docker secrets for passwords
✅ Enable SSL/TLS
✅ Use environment-specific configs
✅ Implement rate limiting
✅ Add monitoring and logging
📊 Monitoring
Check Container Resource Usage
bash
docker stats
Check Container Health
bash
docker inspect employee_task_api | grep -A 20 Health
🚀 Production Deployment
Build for Production
Create docker-compose.prod.yml:

yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    # No port exposure (internal only)

  api:
    build: .
    restart: always
    environment:
      DATABASE_URL: ${DATABASE_URL}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      DEBUG: "False"
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
Deploy:

bash
docker-compose -f docker-compose.prod.yml up -d
📝 Quick Reference
Daily Workflow
bash
# Start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop
docker-compose stop
After Code Changes
bash
# Rebuild and restart
docker-compose up --build -d
Clean Slate
bash
# Remove everything (including data!)
docker-compose down -v

# Remove images
docker rmi $(docker images 'fastapi_task*' -q)

# Start fresh
docker-compose up --build -d
✅ Success Checklist
 Docker Desktop is running
 docker-compose up -d completed successfully
 Both containers show "Up" status
 http://localhost:8000/health returns 200 OK
 Can login with admin/admin123
 Swagger UI loads correctly
 Can create employees/tasks
🎉 You're Done!
Your API is now running in Docker with PostgreSQL!

Access Points:

🌐 Swagger UI: http://localhost:8000/
📚 ReDoc: http://localhost:8000/redoc
🗄️ PostgreSQL: localhost:5432
Default Credentials:

Username: admin
Password: admin123
Need Help?

Check logs: docker-compose logs -f api
View this guide: DOCKER_SETUP.md
Authentication guide: AUTHENTICATION_GUIDE.md

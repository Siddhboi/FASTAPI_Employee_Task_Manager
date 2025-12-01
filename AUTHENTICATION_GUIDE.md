# 🔐 Complete Authentication Guide

## Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Default Users
```bash
python create_default_users.py
```

### Step 3: Start Server
```bash
uvicorn main:app --reload
```

---

## 🎯 How to Use Authentication

### Method 1: Using Swagger UI (Easiest)

1. **Open Swagger UI**
   - Go to: http://localhost:8000/

2. **Login**
   - Find: `POST /auth/login`
   - Click "Try it out"
   - Enter credentials:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Click "Execute"
   - Copy the `access_token` from response

3. **Authorize**
   - Click the **"Authorize" button** 🔓 (top right)
   - In the popup, enter: `Bearer <your_access_token>`
   - Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - Click "Authorize"
   - Click "Close"

4. **Test Protected Endpoints**
   - Try any endpoint with 🔒 icon
   - It will now work with your token!

---

### Method 2: Using cURL

#### Register New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "New User",
    "role": "client"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    ...
  }
}
```

#### Use Token in Requests
```bash
# Set token as variable
TOKEN="your_access_token_here"

# Create employee (requires authentication)
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Developer"
  }'

# Delete employee (requires admin role)
curl -X DELETE "http://localhost:8000/employees/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Method 3: Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["access_token"]
print(f"Token: {token}")

# 2. Set headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 3. Create employee
employee_data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "role": "Manager"
}
response = requests.post(
    f"{BASE_URL}/employees/",
    json=employee_data,
    headers=headers
)
print(response.json())

# 4. Get current user info
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(response.json())
```

---

## 👥 Default Users

After running `create_default_users.py`:

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| admin | admin123 | ADMIN | Full access |
| demoadmin | demo123 | ADMIN | Demo admin |
| client | client123 | CLIENT | Limited access |

---

## 🔑 User Roles & Permissions

### ADMIN Role
✅ Can create employees  
✅ Can update employees  
✅ Can delete employees (admin only)  
✅ Can create tasks  
✅ Can update tasks  
✅ Can delete tasks (admin only)  
✅ Can assign tasks  
✅ Can view all users  
✅ Can create other admins  

### CLIENT Role
✅ Can create employees  
✅ Can update employees  
❌ Cannot delete employees  
✅ Can create tasks  
✅ Can update tasks  
❌ Cannot delete tasks  
✅ Can assign tasks  
❌ Cannot view all users  
❌ Cannot create admins  

---

## 📋 Complete API Workflow

### Step-by-Step Example

```bash
# 1. Register new client user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "role": "client"
  }'

# 2. Login to get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'

# Save the access_token from response
TOKEN="<your_token_here>"

# 3. Get current user info
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/auth/me"

# 4. Create an employee
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "role": "Developer"
  }'

# 5. Create a task
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix bug in login",
    "description": "Users cannot login with email",
    "status": "pending"
  }'

# 6. Assign task to employee
curl -X POST "http://localhost:8000/tasks/1/assign/1" \
  -H "Authorization: Bearer $TOKEN"

# 7. Update task status
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

---

## 🔍 Troubleshooting

### "Could not validate credentials"
- Token might be expired (24 hours validity)
- Token format incorrect (must be: `Bearer <token>`)
- Login again to get new token

### "Admin privileges required"
- Endpoint requires admin role
- Login with admin account

### "Username already registered"
- Choose a different username
- Or login with existing account

### "Incorrect username or password"
- Check credentials
- Passwords are case-sensitive

---

## 🛡️ Security Best Practices

1. **Change Default Passwords**
   ```bash
   # After first login, change all default passwords
   ```

2. **Use Strong Passwords**
   - Minimum 8 characters
   - Mix of letters, numbers, symbols

3. **Keep Tokens Secret**
   - Never share your token
   - Don't commit tokens to git

4. **Token Expiration**
   - Tokens expire after 24 hours
   - Login again to get new token

5. **HTTPS in Production**
   - Always use HTTPS in production
   - Never send tokens over HTTP

---

## 📱 Testing with Postman

1. **Create New Request**
   - Method: POST
   - URL: `http://localhost:8000/auth/login`
   - Body → raw → JSON:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Send → Copy `access_token`

2. **Set Up Authorization**
   - Go to Authorization tab
   - Type: Bearer Token
   - Paste your token

3. **Test Protected Endpoint**
   - Create new request
   - Authorization will be auto-added
   - Works for all protected endpoints!

---

## 🎓 Advanced Usage

### Create Admin User (Admin Only)
```bash
curl -X POST "http://localhost:8000/auth/create-admin" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newadmin",
    "email": "newadmin@example.com",
    "password": "secure123",
    "full_name": "New Admin"
  }'
```

### List All Users (Admin Only)
```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/auth/users"
```

### Verify Token
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/auth/verify-token"
```

---

## 💡 Quick Tips

- 🔑 Token lasts 24 hours
- 🔒 Admin can do everything
- 👤 Client cannot delete
- 📝 Register is public
- 🚀 First user can be admin
- ✅ All passwords are hashed
- 🔐 BCrypt is secure

---

**Need Help?**
- Check Swagger UI: http://localhost:8000/
- Check API Info: http://localhost:8000/info
- Check Health: http://localhost:8000/health
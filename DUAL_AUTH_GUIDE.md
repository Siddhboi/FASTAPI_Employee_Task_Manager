# 🔐 Dual Authentication Guide - JWT + API Key

## Overview

Your API now supports **TWO authentication methods**:
1. **JWT Bearer Token** - For web/mobile applications with user login
2. **API Key** - For server-to-server communication

**Both work independently, and you can use either one!**

---

## 🎯 Method 1: JWT Bearer Token

### Use Case
- Web applications
- Mobile apps
- User-specific access control
- Role-based permissions (Admin/Client)

### Steps to Use in Swagger

1. **Login to get token**
   - Go to `POST /auth/login`
   - Click "Try it out"
   - Enter credentials:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Click "Execute"
   - **Copy the `access_token`** from response

2. **Authorize in Swagger**
   - Click the **🔓 Authorize** button (top right)
   - You'll see TWO authentication methods
   - Select **HTTPBearer (http, Bearer)**
   - Paste your token (without "Bearer" prefix)
   - Click "Authorize"
   - Click "Close"

3. **Test Protected Endpoints**
   - Try `POST /employees/` - Works! ✅
   - Try `DELETE /employees/1` - Works if you're admin! ✅

### Using in Code (cURL)

```bash
# Step 1: Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'

# Response: Copy the access_token
# {"access_token": "eyJhbG...", "token_type": "bearer", "user": {...}}

# Step 2: Use the token
TOKEN="eyJhbG..."

# Create employee
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Developer"
  }'
```

### Using in Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# Use token in headers
headers = {"Authorization": f"Bearer {token}"}

# Create employee
employee_data = {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "Manager"
}
response = requests.post(
    f"{BASE_URL}/employees/",
    json=employee_data,
    headers=headers
)
print(response.json())
```

---

## 🔑 Method 2: API Key

### Use Case
- Server-to-server communication
- Automated scripts/bots
- CI/CD pipelines
- No user login required
- **Always has ADMIN privileges**

### Steps to Use in Swagger

1. **Authorize in Swagger**
   - Click the **🔓 Authorize** button (top right)
   - Select **APIKeyHeader (apiKey)**
   - Enter: `your-secret-api-key-12345`
   - Click "Authorize"
   - Click "Close"

2. **Test Protected Endpoints**
   - Try `POST /employees/` - Works! ✅
   - Try `DELETE /employees/1` - Works (API key = admin)! ✅

### Using in Code (cURL)

```bash
# Create employee with API key
curl -X POST "http://localhost:8000/employees/" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Johnson",
    "email": "bob@example.com",
    "role": "Developer"
  }'

# Delete employee with API key
curl -X DELETE "http://localhost:8000/employees/1" \
  -H "X-API-Key: your-secret-api-key-12345"
```

### Using in Python

```python
import requests

BASE_URL = "http://localhost:8000"

# API Key in headers (no login needed!)
headers = {"X-API-Key": "your-secret-api-key-12345"}

# Create employee
employee_data = {
    "name": "Alice Brown",
    "email": "alice@example.com",
    "role": "Designer"
}
response = requests.post(
    f"{BASE_URL}/employees/",
    json=employee_data,
    headers=headers
)
print(response.json())

# Delete employee (admin access)
response = requests.delete(
    f"{BASE_URL}/employees/1",
    headers=headers
)
print(response.status_code)  # 204
```

---

## 🆚 Comparison

| Feature | JWT Token | API Key |
|---------|-----------|---------|
| **Use Case** | User authentication | Server-to-server |
| **Requires Login** | ✅ Yes | ❌ No |
| **Expires** | ✅ Yes (24 hours) | ❌ Never |
| **Role-Based** | ✅ Admin/Client | ⚠️ Always Admin |
| **Header** | `Authorization: Bearer <token>` | `X-API-Key: <key>` |
| **Best For** | Web/Mobile Apps | Scripts/Automation |

---

## 🎯 Which One to Use?

### Use JWT When:
- Building a web application
- Building a mobile app
- Need user-specific permissions
- Need role-based access (admin vs client)
- Users need to log in

### Use API Key When:
- Building server-to-server integration
- Writing automated scripts
- CI/CD pipelines
- No user interaction
- Always need admin access
- Don't want to deal with token expiration

---

## 🔄 Can I Use Both?

**Yes!** You can provide both authentication methods in the same request.

**Priority:**
1. JWT is checked first
2. If JWT fails/missing, API Key is checked
3. If both fail/missing, returns 401 Unauthorized

**Example:**
```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

In this case, **JWT will be used** (it has priority).

---

## 📋 Complete Examples

### Example 1: Create Employee with JWT

```bash
# 1. Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Copy access_token, then:
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Employee",
    "email": "test@example.com",
    "role": "Tester"
  }'
```

### Example 2: Create Employee with API Key

```bash
# One step - no login needed!
curl -X POST "http://localhost:8000/employees/" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Employee",
    "email": "test@example.com",
    "role": "Tester"
  }'
```

### Example 3: Client Role (JWT Only)

```bash
# Login as client
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"client","password":"client123"}'

# Can create
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer <client_token>" \
  -H "Content-Type: application/json" \
  -d '{...}'
# ✅ Works!

# Cannot delete
curl -X DELETE "http://localhost:8000/employees/1" \
  -H "Authorization: Bearer <client_token>"
# ❌ 403 Forbidden - Admin privileges required
```

---

## 🧪 Testing in Swagger

### Scenario 1: Test JWT Authentication

1. Go to http://localhost:8000/
2. POST /auth/login → Login as admin
3. Copy access_token
4. Click Authorize → HTTPBearer → Paste token
5. Try POST /employees/ → ✅ Works
6. Try DELETE /employees/1 → ✅ Works (admin)

### Scenario 2: Test API Key Authentication

1. Clear any JWT authorization (click Logout in HTTPBearer)
2. Click Authorize → APIKeyHeader
3. Enter: `your-secret-api-key-12345`
4. Try POST /employees/ → ✅ Works
5. Try DELETE /employees/1 → ✅ Works (API key = admin)

### Scenario 3: Test Client Role Limits

1. Login as client (client/client123)
2. Copy access_token
3. Click Authorize → HTTPBearer → Paste token
4. Try POST /employees/ → ✅ Works
5. Try DELETE /employees/1 → ❌ 403 Forbidden

---

## 🔒 Security Notes

1. **Change Default API Key** in production
   ```env
   API_KEY=your-new-secure-random-key-here
   ```

2. **JWT Tokens Expire** after 24 hours
   - Need to login again to get new token
   - API keys never expire

3. **API Key = Admin Access**
   - Keep it secret!
   - Don't expose in client-side code
   - Only use for backend/server communication

4. **HTTPS in Production**
   - Always use HTTPS to protect credentials
   - Never send auth over plain HTTP

---

## 🐛 Troubleshooting

### "Could not validate credentials"
- **JWT**: Token expired or invalid → Login again
- **API Key**: Key doesn't match → Check spelling

### "Admin privileges required"
- Using client JWT token → Use admin login or API key
- Client role cannot delete

### "Authentication required"
- No JWT or API Key provided
- Check Authorize button is properly set

### Both Showing in Swagger?
**YES! This is correct!**
- HTTPBearer = JWT authentication
- APIKeyHeader = API Key authentication
- Use either one (or both)

---

## ✅ Quick Reference

```bash
# JWT Authentication
Authorization: Bearer <your_access_token>

# API Key Authentication
X-API-Key: your-secret-api-key-12345

# Default Credentials
Admin JWT: admin / admin123
Client JWT: client / client123
API Key: your-secret-api-key-12345
```

---

**Both authentication methods are now working perfectly! 🎉**
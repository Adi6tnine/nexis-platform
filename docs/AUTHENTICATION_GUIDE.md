# Authentication System Guide

## Overview

NEXIS now includes a complete authentication system with user registration, login, logout, and profile management.

## Features

### User Authentication
- **Registration**: Create new account with email and password
- **Login**: Secure JWT-based authentication
- **Logout**: Clean session termination
- **Profile Management**: View and manage user profile
- **Session Persistence**: Auto-login on return visits

### Security Features
- Password hashing with bcrypt
- JWT tokens with 24-hour expiration
- Secure token storage in localStorage
- Automatic token refresh on API calls
- Protected routes requiring authentication

## User Flow

### 1. New User Registration
```
1. User visits app → Login screen
2. Click "Create Account"
3. Fill registration form:
   - Full Name
   - Email
   - Phone (optional)
   - Password (min 8 characters)
   - Confirm Password
4. Submit → Account created + Auto-login
5. Redirect to Consent screen
```

### 2. Existing User Login
```
1. User visits app → Login screen
2. Enter email and password
3. Submit → Authentication
4. Redirect based on profile status:
   - Has score → Dashboard
   - Has consent → Dashboard
   - No consent → Consent screen
```

### 3. User Session
```
- Token stored in localStorage
- Auto-login on page refresh
- Token sent with all API requests
- Logout clears token and redirects to login
```

## API Endpoints

### Authentication Endpoints

#### POST /api/v1/auth/register
Register new user account

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": "NEX-A1B2C3D4",
  "email": "john@example.com",
  "name": "John Doe",
  "message": "Registration successful"
}
```

#### POST /api/v1/auth/login
Login with credentials

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": "NEX-A1B2C3D4",
  "email": "john@example.com",
  "name": "John Doe",
  "message": "Login successful"
}
```

#### GET /api/v1/auth/me
Get current user profile (requires authentication)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "user_id": "NEX-A1B2C3D4",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "consent_given": true,
  "profile_completed": true,
  "has_score": true,
  "trust_score": 742,
  "risk_level": "Low",
  "last_scored_at": "2026-02-17T10:30:00Z",
  "created_at": "2026-02-15T08:00:00Z"
}
```

#### POST /api/v1/auth/logout
Logout user (requires authentication)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Logout successful. Please discard your access token."
}
```

## Database Schema Updates

### Users Table - New Fields

```sql
-- Authentication fields
hashed_password VARCHAR NOT NULL
is_active BOOLEAN DEFAULT TRUE
is_verified BOOLEAN DEFAULT FALSE

-- Profile fields
profile_completed BOOLEAN DEFAULT FALSE
last_login DATETIME

-- Consent tracking (modified)
consent_timestamp DATETIME NULL  -- Now nullable
```

## Frontend Implementation

### Token Management

```javascript
// Token storage
tokenManager.setToken(token);    // Store token
tokenManager.getToken();          // Retrieve token
tokenManager.removeToken();       // Clear token
tokenManager.hasToken();          // Check if token exists
```

### Protected API Calls

All API calls automatically include the auth token if available:

```javascript
// Automatically adds Authorization header
const profile = await api.getCurrentUser();
const score = await api.calculateScore(userId, data);
```

### Authentication State

```javascript
const [isAuthenticated, setIsAuthenticated] = useState(false);
const [userId, setUserId] = useState(null);
const [userName, setUserName] = useState('');
```

## Setup Instructions

### 1. Run Database Migration

```bash
cd backend
alembic upgrade head
```

This will add the authentication fields to the users table.

### 2. Install Dependencies

Backend dependencies are already in requirements.txt:
- python-jose[cryptography] - JWT handling
- passlib[bcrypt] - Password hashing

```bash
pip install -r requirements.txt
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 4. Start Frontend

```bash
cd frontend
npm run dev
```

## Testing the Authentication

### Test Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "password": "TestPass123!"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <your_token_here>"
```

## Security Best Practices

### Password Requirements
- Minimum 8 characters
- Stored as bcrypt hash
- Never logged or exposed

### Token Security
- 24-hour expiration
- Stored in localStorage (consider httpOnly cookies for production)
- Automatically cleared on logout
- Validated on every request

### API Security
- Rate limiting on auth endpoints
- HTTPS required in production
- CORS properly configured
- SQL injection protection via SQLAlchemy

## Troubleshooting

### "Invalid authentication credentials"
- Token expired (24 hours)
- Token corrupted
- Solution: Logout and login again

### "Email already registered"
- User already exists
- Solution: Use login instead or different email

### "Incorrect email or password"
- Wrong credentials
- Solution: Check email/password or register new account

### Token not persisting
- localStorage disabled
- Private browsing mode
- Solution: Enable localStorage or use regular browsing

## Future Enhancements

- [ ] Email verification
- [ ] Password reset flow
- [ ] Two-factor authentication (2FA)
- [ ] OAuth integration (Google, Facebook)
- [ ] Remember me functionality
- [ ] Session management dashboard
- [ ] Account deletion
- [ ] Password change
- [ ] Profile picture upload

## Related Documentation

- [API Documentation](../backend/README.md)
- [Security Configuration](../backend/app/core/security.py)
- [Database Models](../backend/app/db/models.py)
- [Frontend API Service](../frontend/src/services/api.js)

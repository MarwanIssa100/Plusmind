# Plusmind API Documentation

## URL Names for Frontend Implementation

### Authentication URLs
- Therapist Register: `register-therapist`
- Patient Register: `register-patient`
- Therapist Login: `therapist-login`
- Patient Login: `patient-login`

- Therapist Logout: `therapist-logout`
- Patient Logout: `patient-logout`
- Password Reset: `password-reset`

### Therapist URLs
- Get Sessions: `therapist-sessions`

## Authentication Endpoints

### Therapist Authentication

#### Register Therapist
- **Endpoint**: `POST /accounts/register/therapist/`
- **URL Name**: `register-therapist`
- **Description**: Register a new therapist account
- **Request Body**:
```json
{
    "email": "therapist@example.com",
    "password": "securepassword123",
    "name": "John Doe",
    "gender": "male",
    "role": "therapist"
}
```

#### Login Therapist
- **Endpoint**: `POST /accounts/login/therapist/`
- **URL Name**: `therapist-login`
- **Description**: Authenticate therapist and get access tokens
- **Request Body**:
```json
{
    "email": "therapist@example.com",
    "password": "securepassword123"
}
```
- **Response**:
```json
{
    "therapist": {
        "id": 1,
        "user": {
            "id": 5,
            "email": "therapist@example.com"
        },
        "specialty": "Cognitive Therapy"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJh...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

#### Logout Therapist
- **Endpoint**: `POST /accounts/logout/therapist/`
- **URL Name**: `therapist-logout`
- **Description**: Blacklist the refresh token to log out
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```
- **Response**:
```json
{
    "detail": "Successfully logged out."
}
```

### Patient Authentication

#### Register Patient
- **Endpoint**: `POST /accounts/register/patient/`
- **URL Name**: `register-patient`
- **Description**: Register a new patient account
- **Request Body**:
```json
{
    "email": "patient@example.com",
    "password": "strongpassword123",
    "name": "Jane Smith",
    "gender": "female",
    "role": "patient"
}
```

#### Login Patient
- **Endpoint**: `POST /accounts/login/patient/`
- **URL Name**: `patient-login`
- **Description**: Authenticate patient and get access tokens
- **Request Body**:
```json
{
    "email": "patient@example.com",
    "password": "strongpassword123"
}
```
- **Response**:
```json
{
    "patient": {
        "id": 2,
        "user": {
            "id": 7,
            "email": "patient@example.com"
        },
        "address": "Cairo, Egypt",
        "Birth_date": "1990-05-01"
    },
    "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
}
```

#### Logout Patient
- **Endpoint**: `POST /accounts/logout/patient/`
- **URL Name**: `patient-logout`
- **Description**: Blacklist the refresh token to log out
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
- **Response**:
```json
{
    "detail": "Successfully logged out."
}
```

### Password Reset

#### Request Password Reset
- **Endpoint**: `POST /accounts/password-reset/request_reset/`
- **URL Name**: `password-reset`
- **Description**: Send password reset link to the provided email
- **Request Body**:
```json
{
    "email": "user@example.com"
}
```
- **Response**:
```json
{
    "detail": "Password reset link sent to your email."
}
```

## Therapist Endpoints

### Get Therapist Sessions
- **Endpoint**: `GET /therapist/sessions/`
- **URL Name**: `therapist-sessions`
- **Description**: Get all sessions for the authenticated therapist
- **Authentication**: Required
- **Response**:
```json
[
    {
        "id": 1,
        "therapist": 1,
        "patient": 2,
        "session_date": "2024-03-20T10:00:00Z",
        "status": "scheduled",
        "notes": "Initial consultation"
    }
]
```

## Error Responses

### Authentication Errors
```json
{
    "non_field_errors": ["Invalid credentials for therapist."]
}
```

### Validation Errors
```json
{
    "email": ["User with this email does not exist."]
}
```

### Token Errors
```json
{
    "error": "Token is invalid or expired"
}
```

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Status Codes

- 200: Success
- 201: Created
- 205: Reset Content (Logout)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
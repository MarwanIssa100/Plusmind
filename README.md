# Plusmind

## 📘 **Accounts API Endpoints**


### **Login Endpoints**

#### 1. **Therapist Login**

* **URL**: `POST /login/therapist/`
* **Description**: Authenticate a therapist and return JWT tokens.
* **Request Body**:

  ```json
  {
    "email": "therapist@example.com",
    "password": "yourpassword"
  }
  ```
* **Response**:

  ```json
  {
    "refresh": "token...",
    "access": "token...",
    "user_id": 1,
    "email": "therapist@example.com"
  }
  ```

#### 2. **Patient Login**

* **URL**: `POST /login/patient/`
* **Description**: Authenticate a patient and return JWT tokens.
* **Request Body**:

  ```json
  {
    "email": "patient@example.com",
    "password": "yourpassword"
  }
  ```
* **Response**: Same as therapist login, with `role: "patient"` claim in token.

---

### **Registration Endpoints**

#### 3. **Therapist Registration**

* **URL**: `POST /register/therapist/`
* **Description**: Create a new therapist and associated user.
* **Request Body**:

  ```json
  {
    "user": {
      "email": "therapist@example.com",
      "password": "yourpassword",
      "username": "therapist1",
      "name": "John Doe",
      "gender": "male"
    },
    "specialty": "Cognitive Therapy",
    "photo": null,
    "working_hours": "9AM - 5PM",
    "certificates": "Licensed Therapist",
    "experience": "5 years"
  }
  ```

#### 4. **Patient Registration**

* **URL**: `POST /register/patient/`
* **Description**: Create a new patient and associated user.
* **Request Body**:

  ```json
  {
    "user": {
      "email": "patient@example.com",
      "password": "yourpassword",
      "username": "patient1",
      "name": "Jane Smith",
      "gender": "female"
    },
    "address": "123 Main St",
    "Birth_date": "2000-01-01"
  }
  ```

---

### **Password Reset**

#### 5. **Request Password Reset**

* **URL**: `POST /password-reset/request_reset/`
* **Description**: Accepts an email and sends a password reset link if the user exists.
* **Request Body**:

  ```json
  {
    "email": "user@example.com"
  }
  ```
* **Response**:

  ```json
  {
    "detail": "Password reset link sent to your email."
  }
  ```


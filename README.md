# Taskly API Documentation

A RESTful API for task management with user authentication, built with Django REST Framework.

## Base URL
```
https://public-egret-kenward-4f7ef820.koyeb.app/api
```

## Authentication

This API uses session-based authentication. After login, the server will set session cookies that are automatically included in subsequent requests. Make sure to include cookies in your requests.

## Endpoints

### Authentication Endpoints

#### Register User
- **URL**: `/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Description**: Register a new user account

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "your_password",
    "password2": "your_password"
}
```

**Success Response:**
```json
{
    "message": "User registered successfully.",
    "email_sent": true
}
```

#### Login User
- **URL**: `/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Description**: Login with email and password

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

**Success Response:**
```json
{
    "message": "User logged in successfully."
}
```

*Note: Session cookies will be set automatically after successful login.*

### Task Management Endpoints

#### List Tasks / Create Task
- **URL**: `/tasks/`
- **Methods**: `GET`, `POST`
- **Auth Required**: Yes

**GET - List Tasks**
- **Description**: Get all tasks for the authenticated user
- **Query Parameters**:
  - `search` (optional): Search in title and description
  - `completed` (optional): Filter by completion status (true/false)

**Success Response:**
```json
[
    {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the Django API project",
        "completed": false,
        "due_date": "2025-07-25T10:00:00Z",
        "created_at": "2025-07-20T16:30:00Z",
        "updated_at": "2025-07-20T16:30:00Z",
        "owner": 1
    }
]
```

**POST - Create Task**
- **Description**: Create a new task

**Request Body:**
```json
{
    "title": "New Task",
    "description": "Task description",
    "due_date": "2025-07-25T10:00:00Z"
}
```

#### Task Details
- **URL**: `/tasks/{id}/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Auth Required**: Yes
- **Description**: Retrieve, update, or delete a specific task

**GET Success Response:**
```json
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the Django API project",
    "completed": false,
    "due_date": "2025-07-25T10:00:00Z",
    "created_at": "2025-07-20T16:30:00Z",
    "updated_at": "2025-07-20T16:30:00Z",
    "owner": 1
}
```

**PUT/PATCH Request Body:**
```json
{
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true,
    "due_date": "2025-07-26T10:00:00Z"
}
```

#### Update Task Status
- **URL**: `/tasks/{id}/status/`
- **Method**: `PATCH`
- **Auth Required**: Yes
- **Description**: Update only the completion status of a task

**Request Body:**
```json
{
    "completed": true
}
```

#### Toggle Task Status
- **URL**: `/tasks/{id}/toggle/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Description**: Toggle the completion status of a task

**Success Response:**
```json
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the Django API project",
    "completed": true,
    "due_date": "2025-07-25T10:00:00Z",
    "created_at": "2025-07-20T16:30:00Z",
    "updated_at": "2025-07-20T16:30:00Z",
    "owner": 1
}
```

#### Completed Tasks
- **URL**: `/tasks/completed/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Description**: Get all completed tasks for the authenticated user

#### Pending Tasks
- **URL**: `/tasks/pending/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Description**: Get all pending (incomplete) tasks for the authenticated user

### Statistics Endpoint

#### Task Statistics
- **URL**: `/tasks/stats/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Description**: Get task statistics for the authenticated user

**Success Response:**
```json
{
    "total_tasks": 10,
    "completed_tasks": 6,
    "pending_tasks": 4,
    "overdue_tasks": 2,
    "completion_rate": 60.0
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

*Note: This usually means you need to login first to establish a session.*

### 404 Not Found
```json
{
    "error": "Task not found or you do not have permission to access it."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error."
}
```

## Features

- **User Registration & Authentication**: Secure user registration with email verification
- **Task Management**: Full CRUD operations for tasks
- **Task Filtering**: Search and filter tasks by completion status
- **Task Statistics**: Get insights into task completion rates
- **Email Notifications**: Automatic email notifications for registration and task creation
- **User Isolation**: Users can only access their own tasks

## Usage Examples

### Register and Login Flow

1. **Register:**
```bash
curl -X POST https://public-egret-kenward-4f7ef820.koyeb.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
  }'
```

2. **Login:**
```bash
curl -X POST https://public-egret-kenward-4f7ef820.koyeb.app/api/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Task Management Examples

1. **Create a Task:**
```bash
curl -X POST https://public-egret-kenward-4f7ef820.koyeb.app/api/tasks/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Complete Documentation",
    "description": "Write comprehensive API documentation",
    "due_date": "2025-07-25T15:00:00Z"
  }'
```

2. **Get All Tasks:**
```bash
curl -X GET https://public-egret-kenward-4f7ef820.koyeb.app/api/tasks/ \
  -b cookies.txt
```

3. **Search Tasks:**
```bash
curl -X GET "https://public-egret-kenward-4f7ef820.koyeb.app/api/tasks/?search=documentation" \
  -b cookies.txt
```

4. **Toggle Task Status:**
```bash
curl -X POST https://public-egret-kenward-4f7ef820.koyeb.app/api/tasks/1/toggle/ \
  -b cookies.txt
```

5. **Get Task Statistics:**
```bash
curl -X GET https://public-egret-kenward-4f7ef820.koyeb.app/api/tasks/stats/ \
  -b cookies.txt
```

## Technical Details

- **Framework**: Django REST Framework
- **Authentication**: Session-based authentication with cookies
- **Database**: PostgreSQL (production), SQLite (development)
- **Email Service**: Configured for welcome and task creation notifications
- **API Documentation**: OpenAPI/Swagger compatible

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

**Note**: This API uses session-based authentication. Make sure to save cookies after login (using `-c cookies.txt`) and include them in subsequent requests (using `-b cookies.txt`) when using curl.
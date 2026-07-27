Disaster Relief & Emergency Resource Management System

Project Overview

The Disaster Relief & Emergency Resource Management System is a backend REST API developed using FastAPI. The application is designed to manage disaster relief operations by providing secure authentication, relief camp management, victim registration, resource distribution, volunteer management, and reporting features. The system follows role-based access control using JWT authentication and stores data in a relational database using SQLAlchemy ORM.

Objectives

The primary objective of this project is to simplify disaster relief management by allowing administrators and relief coordinators to efficiently manage camps, victims, resources, and volunteers while ensuring secure access through authentication and authorization.

Technology Stack

Programming Language
Python 3.9+

Framework
FastAPI

Database
SQLite

ORM
SQLAlchemy

Authentication
JWT (JSON Web Token)

Validation
Pydantic

Server
Uvicorn

Testing
Pytest

Project Structure

```
disaster_relief_management_system/

│── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── camps.py
│   │   ├── victims.py
│   │   ├── resources.py
│   │   ├── volunteers.py
│   │   └── reports.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   └── utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_camps.py
│   ├── test_victims.py
│   ├── test_resources.py
│   ├── test_volunteers.py
│   └── test_reports.py
│
├── .env
├── requirements.txt
├── README.md
└── test.db
```

Features

Authentication

• User Registration

• User Login

• JWT Token Authentication

• Password Hashing using Bcrypt

• Role-Based Authorization

User Roles

Admin

• Full access to all modules.

Relief Coordinator

• Manage camps.

• Register and update victims.

• Manage resources.

• Manage volunteers.

• View reports.

Volunteer

• View only assigned camp details.

Relief Camp Management

The system allows coordinators to create and manage relief camps.

Camp Information

• Camp Name

• Location

• District

• Capacity

• Available Capacity

• Status

Operations

• Create Camp

• View All Camps

• View Camp by ID

• Update Camp

• Delete Camp

Victim Management

Victims affected by disasters can be registered under relief camps.

Victim Information

• Name

• Age

• Gender

• Contact Number

• Family Members

• Assigned Camp

Operations

• Register Victim

• View Victims

• View Victim by ID

• Update Victim

Resource Distribution

Resources distributed to camps are recorded for tracking purposes.

Resource Information

• Camp

• Resource Type

• Stock

• Quantity Distributed

• Distributed By

• Distribution Date

Operations

• Create Resource Distribution

• View Resource History

• View Resource by ID

Volunteer Management

Volunteers can be assigned to relief camps.

Volunteer Information

• Name

• Email

• Phone Number

• Assigned Camp

• Availability Status

Operations

• Create Volunteer

• View Volunteers

• Assign Volunteer to Camp

Reports

The reporting module provides useful information for administrators and coordinators.

Available Reports

• Search Camps by District

• Filter Victims by Camp

• Resource Distribution History

• Volunteer Assignments

• Pagination Support

Business Rules

• Camp capacity cannot be exceeded.

• Camp availability updates automatically when victims are registered.

• Resource quantity cannot exceed available stock.

• Volunteer email must be unique.

• A volunteer can be assigned to only one active camp.

• Capacity and quantity must always be greater than zero.

Authentication Flow

The application uses JWT authentication.

1. Register a new user.

2. Login using email and password.

3. Receive an access token.

4. Authorize using the Bearer token in Swagger or API requests.

Database Tables

Users

Stores authentication details and user roles.

Camps

Stores relief camp information.

Victims

Stores victim registration details.

Resources

Stores resource distribution records.

Volunteers

Stores volunteer information and assignments.

API Endpoints

Authentication

POST /auth/register

POST /auth/login

Relief Camps

POST /camps

GET /camps

GET /camps/{camp_id}

PUT /camps/{camp_id}

DELETE /camps/{camp_id}

Victims

POST /victims

GET /victims

GET /victims/{victim_id}

PUT /victims/{victim_id}

Resources

POST /resources

GET /resources

GET /resources/{resource_id}

Volunteers

POST /volunteers

GET /volunteers

POST /volunteers/{volunteer_id}/assign/{camp_id}

GET /volunteers/my-camp

Reports

GET /reports/search/camps

GET /reports/filter/victims

GET /reports/history/resources

GET /reports/volunteer-assignments

Pagination

Every list endpoint supports pagination using:

page

limit

Installation

Clone the repository.

```
git clone <repository_url>
```

Move into the project folder.

```
cd disaster_relief_management_system
```

Create a virtual environment.

Windows

```
python -m venv venv
```

Activate the virtual environment.

Windows

```
venv\Scripts\activate
```

Install all required packages.

```
pip install -r requirements.txt
```

Create the environment file.

```
DATABASE_URL=sqlite:///./disaster_relief.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Running the Application

Start the FastAPI server.

```
uvicorn app.main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

Testing

Run all test cases.

```
pytest -v
```

The test suite covers

• Authentication

• Camp Management

• Victim Management

• Resource Management

• Volunteer Management

• Reports

Validation Rules

• Email addresses must be unique.

• Passwords are securely hashed.

• Camp capacity must be greater than zero.

• Available capacity must be greater than zero.

• Resource quantity must be greater than zero.

• Stock must be greater than zero.

• Unauthorized users cannot access protected endpoints.

Security

• JWT Authentication

• Password Hashing using Passlib Bcrypt

• Role-Based Authorization

• Protected API Routes

• Input Validation with Pydantic

Future Enhancements

• Email notifications

• SMS notifications

• QR code-based victim identification

• GPS-based relief camp tracking

• Resource inventory management

• Dashboard analytics

• File upload support

• Disaster incident management

Conclusion

The Disaster Relief & Emergency Resource Management System provides a secure and scalable backend solution for managing disaster relief operations. The application follows REST API principles, implements JWT authentication and role-based authorization, enforces business rules through validation, and includes automated test cases to ensure reliability and maintainability.

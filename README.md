Health Information System API
A RESTful API for managing health programs and client enrollments, built with Flask, SQLAlchemy, and SQLite. The API supports creating programs, registering clients, enrolling clients in programs, searching clients, and retrieving client profiles, with data encryption, authentication, and caching. Swagger UI is integrated for API documentation.

<h1>Table of Contents</h1>

Features
Project Structure
Prerequisites
Setup
Running the Application
API Endpoints
Testing
Troubleshooting
Contributing
License

Features

Program Management: Create health programs with name and description.
Client Management: Register clients with encrypted personal data (name, date of birth).
Enrollment: Enroll clients in programs with a many-to-many relationship.
Search: Search clients by name (async support).
Profile Retrieval: Get client profiles with enrolled programs (cached for performance).
Security: Token-based authentication and data encryption using cryptography.
Documentation: Swagger UI for interactive API documentation at /apidocs/.
Modular Design: Code organized into modules (app, models, routes, etc.) for maintainability.

Project Structure
HIS/
├── .venv/ # Virtual environment (ignored by Git)
├── .git/ # Git repository
├── .gitignore # Git ignore file
├── README.md # This file
├── requirements.txt # Python dependencies
├── health_system.db # SQLite database (ignored by Git)
├── test_health_system.py # Unit tests
├── app/ # Python package
│ ├── **init**.py # Marks app/ as a package
│ ├── app.py # Flask app initialization
│ ├── config.py # Configuration (database URI, etc.)
│ ├── models.py # SQLAlchemy models (Program, Client)
│ ├── routes.py # API routes and Swagger documentation
│ ├── schemas.py # JSON schemas for validation
│ ├── utils.py # Utility functions (encryption)

Prerequisites

Python 3.8+: Ensure Python is installed.
Git: For cloning and version control.
Git Bash (Windows): For running commands (or equivalent terminal).
SQLite: For the database (included with Python).

Setup

Clone the Repository:
git clone https://github.com/your-username/health-information-system.git
cd health-information-system

Create a Virtual Environment:
python -m venv .venv
source .venv/bin/activate # On Windows Git Bash

# Or: source .venv/Scripts/activate

Install Dependencies:
pip install -r requirements.txt

Dependencies include:

flask
flask-sqlalchemy
flasgger
jsonschema
flask-caching
flask-httpauth
cryptography

Initialize the Database:The SQLite database (health_system.db) is created automatically when the app runs. To create it manually:
python -c "from app.app import create_app; app=create_app(); app.app_context().push(); from app.models import db; db.create_all()"

Running the Application

Activate the Virtual Environment:
source .venv/bin/activate

Run the Flask App:
python -m app.app

The server runs at http://localhost:5001.

Access Swagger UI:Open http://localhost:5001/apidocs/ in a browser to view API documentation.

API Endpoints
All endpoints require authentication with the header Authorization: Bearer secret-token-123.

Endpoint
Method
Description
Payload Example

/programs
POST
Create a health program
{"name": "TB", "description": "Tuberculosis Treatment"}

/clients
POST
Register a client
{"name": "John Doe", "date_of_birth": "1990-01-01", "gender": "Male"}

/clients/<client_id>/enroll
POST
Enroll a client in a program
{"program_id": "uuid-string"}

/clients/search
GET
Search clients by name
Query: ?name=John

/clients/<client_id>
GET
Get client profile and enrolled programs
None

Example Usage:
curl -H "Authorization: Bearer secret-token-123" -X POST -H "Content-Type: application/json" -d '{"name":"TB","description":"Tuberculosis Treatment"}' http://localhost:5001/programs

Testing
Run unit tests to verify functionality:
python -m unittest test_health_system.py

Tests cover program creation, client registration, enrollment, search, and profile retrieval.
Troubleshooting

No health_system.db: Run python -m app.app or the manual database creation command above.
/apidocs/ 404: Ensure flasgger is installed (pip install flasgger) and Swagger(app) is in app/app.py.
Port Conflicts: If port 5001 is in use, kill the process or change the port in app/app.py:app.run(host='0.0.0.0', port=5002, debug=True)

OneDrive Issues: If sync errors occur, move the project:mv /c/Users/User/OneDrive/Desktop/Interview/HIS /c/Users/User/Desktop/HIS

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

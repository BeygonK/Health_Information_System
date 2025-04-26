# Health Information System API

A RESTful API for managing health programs and client enrollments, built with Flask, SQLAlchemy, and SQLite. The API supports creating programs, registering clients, enrolling clients in programs, searching clients, and retrieving client profiles, with data encryption, authentication, and caching. Swagger UI is integrated for API documentation.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Program Management**: Create health programs with name and description.
- **Client Management**: Register clients with encrypted personal data (name, date of birth).
- **Enrollment**: Enroll clients in programs with a many-to-many relationship.
- **Search**: Search clients by name (async support).
- **Profile Retrieval**: Get client profiles with enrolled programs (cached for performance).
- **Security**: Token-based authentication and data encryption using cryptography.
- **Documentation**: Swagger UI for interactive API documentation at `/apidocs/`.
- **Modular Design**: Code organized into modules (`app`, `models`, `routes`, etc.) for maintainability.

---

## Project Structure

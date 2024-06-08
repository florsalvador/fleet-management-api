# Fleet Management API

## Description

This project involves the development of a REST API for a Fleet Management Software designed to track the locations of the vehicles of a taxi company in Beijing, China. The API allows for the management and querying of the locations of nearly 10,000 taxis.

## Technologies used

- **Python**: Main programming language.
- **Flask**: Framework for web application development.
- **SQLAlchemy**: ORM for easier database interaction.
- **PostgreSQL**: Relational database management system.
- **Postman**: Tool used for API testing.

## API Functionalities

### 1. List taxis

- Description: Provides a list of all taxis.
- Method: GET
- Route: /taxis
- Parameters:  page (optional), limit (optional)

### 2. Location history

- Description: Provides all locations of a taxi given its ID and a specific date.
- Method: GET
- Route: /trajectories
- Parameters: taxiId (required), date (optional)

### 3. Last location

- Description: Gets the last reported location of each taxi.
- Method: GET
- Route: /trajectories/latest
- Parameteres: page (optional), limit (optional)

### 4. User management

- Description: Set of endpoints to perform CRUD operations on the platform's users.
- Methods: GET, POST, PATCH, DELETE
- Routes:
  - List users: /users
  - Create user: /users
  - Update user: /users/uid
  - Delete user: /users/uid

### 5. User authentication with JWT

- Description: Allows users to authenticate using their email and password, and receive a JSON Web Token.
- Method: POST
- Route: /auth/login

### 6. JWT-Protected endpoints

- Description: Ensures all API endpoints are protected using a JWT token in the authorization header of each request.
- Implementation: Flask middleware to verify JWT tokens on protected routes.

### 7. Export to Excel

- Description: Exports all locations of a taxi on a specific date in Excel format and sends the file via email.
- Method: GET
- Route: /trajectories/export
- Parameters: taxiId, date, email (all required)

### 8. Command-Line Interface (CLI)

A CLI was developed to efficiently load over 17 million location records from text files into the PostgreSQL database. It handles the process of reading and inserting data by generating SQL queries for each text file.

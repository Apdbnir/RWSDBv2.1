# Railway Station Database v2.1 (RWSDBv2.1) - HTTP Server Edition

An advanced database management system for railway station operations, transformed from the desktop application of BDSM v2.0 to a web-based HTTP server application with RESTful API. Built with enhanced capabilities and improvements based on the latest requirements.

## Project Structure

```
RWSDBv2.1/
├── app/                    # Main application entry point
│   ├── __init__.py
│   └── main.py            # Main application entry point
├── database/              # Database management and models
│   ├── __init__.py
│   ├── manager.py         # Core database operations (PostgreSQL)
│   ├── models/            # Data models
│   │   └── __init__.py
│   ├── postgres_create_schema.sql  # PostgreSQL schema creation
│   ├── postgres_populate_lookup_tables.sql  # Populate lookup tables
│   ├── postgres_generate_main_data.sql  # Generate main table data
│   └── postgres_functions_triggers.sql  # PostgreSQL functions/triggers
├── ui/                    # User interface components (legacy)
│   ├── __init__.py
│   ├── mainwindow.py      # Main application window (legacy)
│   ├── connection_dialog.py  # PostgreSQL connection dialog (legacy)
│   ├── login_dialog.py    # Authentication dialog (legacy)
│   ├── splash_screen.py   # Startup splash screen (legacy)
│   ├── sql_queries.py     # Predefined SQL queries (legacy)
│   ├── lab_queries.py     # Laboratory work specific queries (legacy)
│   ├── sql_syntax_highlighter.py  # SQL syntax highlighting (legacy)
│   ├── styles.qss         # Application styling (legacy)
│   ├── icons/             # Application icons (legacy)
│   └── dialogs/           # Dialog windows (legacy)
│       └── __init__.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── constants.py       # Application constants
│   ├── translations.py    # Multilingual support
│   ├── query_history.py   # Query history management
│   ├── security.py        # Security utilities
│   ├── export_utils.py    # Data export utilities
│   ├── db_logging.py      # Database logging
│   └── backup/            # Backup functionality
│       ├── __init__.py
│       ├── backup_manager.py  # Backup management
│       └── postgres_backup_manager.py  # PostgreSQL-specific backup
├── data/                  # Database files and backups
├── docs/                  # Documentation
├── tests/                 # Test files
├── server.py              # HTTP server implementation
├── __main__.py            # Entry point for python -m RWSDBv2.1 (now runs server)
├── config.json            # Configuration file
└── requirements.txt       # Python dependencies
```

## Features

- **HTTP Server Architecture**: RESTful API server for database operations
- **JSON Request/Response**: All communication in JSON format
- **PostgreSQL Backend**: Full PostgreSQL database support using libpq-compatible library
- **Standard HTTP Methods**: GET, POST, PUT, DELETE for CRUD operations
- **User Role Management**: Regular users and superusers with different permissions
- **Lookup Table Protection**: Only superusers can modify lookup tables
- **Secure Authentication**: Superuser actions require password authentication
- **Database Backup**: Superusers can create database backups via API
- **Filtering Support**: Query parameters for filtering table data
- **CORS Support**: Cross-origin resource sharing enabled

## API Endpoints

The server provides the following RESTful endpoints:

| Method | Endpoint                     | Description                          |
|--------|------------------------------|--------------------------------------|
| GET    | `/api/employees`             | Get all employees                    |
| POST   | `/api/employees`             | Create new employee (superuser only for lookup tables) |
| PUT    | `/api/employees/{id}`        | Update employee                      |
| DELETE | `/api/employees/{id}`        | Delete employee (superuser only for lookup tables) |
| GET    | `/api/students`              | Get all students                     |
| POST   | `/api/students`              | Create new student                   |
| PUT    | `/api/students/{id}`         | Update student                       |
| DELETE | `/api/students/{id}`         | Delete student                       |
| GET    | `/api/groups`                | Get all groups                       |
| POST   | `/api/groups`                | Create new group                     |
| PUT    | `/api/groups/{id}`           | Update group                         |
| DELETE | `/api/groups/{id}`           | Delete group                         |
| GET    | `/api/marks`                 | Get all marks                        |
| POST   | `/api/marks`                 | Create new mark                      |
| PUT    | `/api/marks/{id}`            | Update mark                          |
| DELETE | `/api/marks/{id}`            | Delete mark                          |
| GET    | `/api/lessons`               | Get all lessons                      |
| POST   | `/api/lessons`               | Create new lesson                    |
| PUT    | `/api/lessons/{id}`          | Update lesson                        |
| DELETE | `/api/lessons/{id}`          | Delete lesson                        |
| GET    | `/api/subjects`              | Get all subjects                     |
| POST   | `/api/subjects`              | Create new subject (superuser only)  |
| PUT    | `/api/subjects/{id}`         | Update subject (superuser only)      |
| DELETE | `/api/subjects/{id}`         | Delete subject (superuser only)      |
| GET    | `/api/lesson-types`          | Get all lesson types                 |
| POST   | `/api/lesson-types`          | Create new lesson type (superuser only) |
| PUT    | `/api/lesson-types/{id}`     | Update lesson type (superuser only)  |
| DELETE | `/api/lesson-types/{id}`     | Delete lesson type (superuser only)  |
| GET    | `/api/positions`             | Get all positions                    |
| POST   | `/api/positions`             | Create new position (superuser only) |
| PUT    | `/api/positions/{id}`        | Update position (superuser only)     |
| DELETE | `/api/positions/{id}`        | Delete position (superuser only)     |
| GET    | `/api/employees-subjects`    | Get all employee-subject relations   |
| POST   | `/api/employees-subjects`    | Create new relation                  |
| PUT    | `/api/employees-subjects/{id}`| Update relation                      |
| DELETE | `/api/employees-subjects/{id}`| Delete relation                      |
| POST   | `/api/backup`                | Create database backup (superuser only) |

## User Roles & Permissions

### Regular User
- Can view all tables (GET requests)
- Can save query results
- Can edit all tables except lookup tables
- Cannot create database backups
- Cannot modify lookup tables

### Superuser
- Same rights as regular user
- Can edit lookup tables (positions, lesson_types, subjects)
- Can create database backups
- Superuser actions require password authentication via Authorization header

## Authentication

Superuser actions require authentication using Bearer token in the Authorization header:

```
Authorization: Bearer {admin_password}
```

Example curl command for superuser action:
```bash
curl -X POST http://localhost:8080/api/backup \
  -H "Authorization: Bearer 4444" \
  -H "Content-Type: application/json"
```

## Installation

1. Clone or download the repository
2. Ensure PostgreSQL is installed and running on your system
3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Linux/Mac
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## PostgreSQL Setup

Before running the application, you need to set up PostgreSQL:

1. Install PostgreSQL (version 10 or higher recommended)
2. Create a database for the application:
   ```sql
   CREATE DATABASE railway_station;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE railway_station TO postgres;
   ```
3. Update the `config.json` file with your PostgreSQL connection details

## Usage

### Running the HTTP Server

```bash
python -m RWSDBv2.1
```

Or directly:
```bash
python __main__.py
```

By default, the server runs on port 8080. You can specify a different port:
```bash
python __main__.py 9000
```

### Setting up the PostgreSQL Database

1. Connect to PostgreSQL and create the schema:
   ```bash
   psql -h localhost -U postgres -d railway_station -f database/postgres_create_schema.sql
   ```

2. Populate lookup tables with initial data:
   ```bash
   psql -h localhost -U postgres -d railway_station -f database/postgres_populate_lookup_tables.sql
   ```

3. Generate main table data:
   ```bash
   psql -h localhost -U postgres -d railway_station -f database/postgres_generate_main_data.sql
   ```

4. Create functions and triggers:
   ```bash
   psql -h localhost -U postgres -d railway_station -f database/postgres_functions_triggers.sql
   ```

### API Usage Examples

#### Get all employees
```bash
curl http://localhost:8080/api/employees
```

#### Get employees with filters
```bash
curl "http://localhost:8080/api/employees?position=engineer&limit=10"
```

#### Create a new employee (regular user)
```bash
curl -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Doe", "position_id": 1, "salary": 50000}'
```

#### Update an employee
```bash
curl -X PUT http://localhost:8080/api/employees/123 \
  -H "Content-Type: application/json" \
  -d '{"salary": 55000}'
```

#### Create a new subject (requires superuser)
```bash
curl -X POST http://localhost:8080/api/subjects \
  -H "Authorization: Bearer 4444" \
  -H "Content-Type: application/json" \
  -d '{"subject_name": "Mathematics", "credits": 3}'
```

#### Create a database backup (requires superuser)
```bash
curl -X POST http://localhost:8080/api/backup \
  -H "Authorization: Bearer 4444" \
  -H "Content-Type: application/json"
```

## Configuration

Update `config.json` with your PostgreSQL connection details:
```json
{
  "admin_password": "4444",
  "pg_host": "localhost",
  "pg_database": "railway_station",
  "pg_user": "postgres",
  "pg_password": "postgres",
  "pg_port": 5432
}
```

Note: The `pg_password` field has been added to support database authentication.

## Testing

Run the test suite with:
```bash
python -m pytest tests/
```

Or run individual tests:
```bash
python tests/test_basic.py
```

## Development

This project transforms the desktop application from BDSM v2.0 into a web-based HTTP server application, maintaining all the original functionality while providing a RESTful API interface. The implementation uses psycopg2 (which is based on libpq) for PostgreSQL interaction as required.

## Laboratory Work Requirements Implementation

This implementation satisfies the requirements for laboratory work #7:

1. **User Role Management**:
   - Regular users: Can view, save query results, and edit all tables except lookup tables
   - Superusers: Same rights as regular users, plus ability to edit lookup tables and create database backups
   - Superuser actions require password authentication

2. **HTTP Server Architecture**:
   - Server-side application implemented as an HTTP server
   - Request/response bodies in JSON format
   - Standard HTTP methods (GET, POST, PUT, DELETE) for resource operations

3. **Resource Endpoints**:
   - `/api/employees`: employees table
   - `/api/students`: students table
   - `/api/groups`: groups table
   - `/api/marks`: marks table
   - `/api/lessons`: lessons table
   - `/api/subjects`: subjects table (lookup table)
   - `/api/lesson-types`: lesson_types table (lookup table)
   - `/api/positions`: positions table (lookup table)
   - `/api/employees-subjects`: employees_subjects table

4. **Database Operations**:
   - View tables with filtering support
   - Add/update/delete records
   - Execute special queries
   - Create database backups
   - Save query results to files

5. **Lookup Table Protection**:
   - Subjects, lesson_types, and positions are protected as lookup tables
   - Only superusers can modify lookup tables
   - Clear distinction between operational and lookup tables

6. **Technical Implementation**:
   - Uses psycopg2 library (based on libpq) for PostgreSQL interaction
   - Implements proper authentication and authorization
   - Follows RESTful API design principles
   - Includes comprehensive error handling
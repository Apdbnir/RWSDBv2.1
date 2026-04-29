# RWSDBv2.1 - Quick Start Guide
# Laboratory Work №1 - Variant 18

## Prerequisites

1. **PostgreSQL 10+** installed and running
2. **Python 3.8+** installed
3. **pg_dump** and **psql** in your PATH

## Installation Steps

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create PostgreSQL Database

Open psql as postgres user and run:

```sql
CREATE DATABASE railway_station;
```

Or from command line:

```bash
createdb -U postgres railway_station
```

### Step 3: Create Database Schema

Run the SQL scripts in order:

```bash
# 1. Create schema (tables, constraints, indexes, views)
psql -h localhost -U postgres -d railway_station -f database/postgres_create_schema.sql

# 2. Populate lookup tables
psql -h localhost -U postgres -d railway_station -f database/postgres_populate_lookup_tables.sql

# 3. Generate test data (1500+ records)
psql -h localhost -U postgres -d railway_station -f database/postgres_generate_main_data.sql

# 4. Create functions and triggers
psql -h localhost -U postgres -d railway_station -f database/postgres_functions_triggers.sql

# 5. Create backup/restore functions
psql -h localhost -U postgres -d railway_station -f database/postgres_backup_restore.sql
```

### Step 4: Verify Database Setup

Run the test script:

```bash
psql -h localhost -U postgres -d railway_station -f database/test_database.sql
```

You should see all tests passing.

### Step 5: Configure Server

Edit `config.json` if needed:

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

### Step 6: Start HTTP Server

```bash
python server.py
```

Or:

```bash
python -m RWSDBv2.1
```

Server will start on port 8080 by default.

### Step 7: Test API

Run the API test script:

```bash
tests\test_api.bat
```

Or test manually with curl:

```bash
# Get all employees
curl http://localhost:8080/api/employees

# Get positions (lookup table)
curl http://localhost:8080/api/positions

# Get database statistics
curl -X PATCH http://localhost:8080/api/statistics
```

## API Usage Examples

### GET - Retrieve Data

```bash
# All employees
curl http://localhost:8080/api/employees

# Filtered employees
curl "http://localhost:8080/api/employees?position=Director"

# With pagination
curl "http://localhost:8080/api/students?limit=10&offset=20"
```

### POST - Create Record

```bash
# Create employee (regular user)
curl -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","position":"Engineer","experience":5}'

# Create position (requires superuser)
curl -X POST http://localhost:8080/api/positions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 4444" \
  -d '{"name":"Senior Engineer"}'
```

### PUT - Update Record

```bash
# Update employee
curl -X PUT http://localhost:8080/api/employees/1 \
  -H "Content-Type: application/json" \
  -d '{"experience":10}'

# Update position (requires superuser)
curl -X PUT http://localhost:8080/api/positions/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 4444" \
  -d '{"description":"Updated description"}'
```

### DELETE - Remove Record

```bash
# Delete employee
curl -X DELETE http://localhost:8080/api/employees/1

# Delete position (requires superuser)
curl -X DELETE http://localhost:8080/api/positions/1 \
  -H "Authorization: Bearer 4444"
```

### PATCH - Custom Operations

```bash
# Custom SELECT query
curl -X PATCH http://localhost:8080/api/custom_query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * FROM employees WHERE experience > 10"}'

# Get statistics
curl -X PATCH http://localhost:8080/api/statistics

# Export to CSV
curl -X PATCH http://localhost:8080/api/export \
  -H "Content-Type: application/json" \
  -d '{"table":"employees","format":"csv"}' \
  -o employees.csv

# Export to Excel
curl -X PATCH http://localhost:8080/api/export \
  -H "Content-Type: application/json" \
  -d '{"table":"employees","format":"excel"}' \
  -o employees.xlsx
```

### POST - Backup

```bash
# Create backup (requires superuser)
curl -X POST http://localhost:8080/api/backup \
  -H "Authorization: Bearer 4444"
```

## Backup and Restore

### Using API

```bash
# Create backup via API
curl -X POST http://localhost:8080/api/backup \
  -H "Authorization: Bearer 4444"
```

### Using Scripts

```bash
# Create backup
database\backup_database.bat

# Restore from backup
database\restore_database.bat
```

### Using psql/pg_dump

```bash
# Backup
pg_dump -h localhost -U postgres -d railway_station -F c -b -f backup.dump

# Restore
pg_restore -h localhost -U postgres -d railway_station -c --if-exists backup.dump
```

## Project Structure

```
RWSDBv2.1/
├── server.py                      # HTTP server
├── config.json                    # Configuration
├── requirements.txt               # Python dependencies
├── database/
│   ├── postgres_create_schema.sql         # Schema creation
│   ├── postgres_populate_lookup_tables.sql # Lookup data
│   ├── postgres_generate_main_data.sql    # Test data
│   ├── postgres_functions_triggers.sql    # Functions/triggers
│   ├── postgres_backup_restore.sql        # Backup functions
│   ├── backup_database.bat                # Backup script
│   ├── restore_database.bat               # Restore script
│   └── test_database.sql                  # DB test script
├── tests/
│   ├── test_basic.py              # Basic tests
│   └── test_api.bat               # API test script
├── docs/
│   ├── specifications.md          # Technical specs (ГОСТ)
│   └── laboratory_work_report.md  # Lab report
└── data/
    └── backups/                   # Backup files
```

## Troubleshooting

### Server won't start

1. Check if PostgreSQL is running
2. Verify config.json credentials
3. Check if port 8080 is available

### Database connection errors

```bash
# Test connection
psql -h localhost -U postgres -d railway_station

# Check PostgreSQL status
pg_isready -h localhost -p 5432
```

### pg_dump not found

Add PostgreSQL bin directory to PATH:

```bash
# Windows
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin

# Linux
export PATH=$PATH:/usr/lib/postgresql/15/bin
```

## Available Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/{table} | Get data | No |
| POST | /api/{table} | Create record | Superuser for lookup |
| PUT | /api/{table}/{id} | Update record | Superuser for lookup |
| DELETE | /api/{table}/{id} | Delete record | Superuser for lookup |
| POST | /api/backup | Create backup | Yes (Superuser) |
| PATCH | /api/custom_query | Execute SELECT | No |
| PATCH | /api/export | Export data | No |
| PATCH | /api/statistics | DB statistics | No |

## Lookup Tables

These tables require superuser authentication for modifications:
- `positions` - Job positions
- `subjects` - Academic subjects
- `lesson_types` - Lesson types

## Default Credentials

- **Superuser password**: `4444`
- **Database user**: `postgres`
- **Database password**: `postgres`

Change these in production!

---

For more information, see:
- `docs/specifications.md` - Technical specifications
- `docs/laboratory_work_report.md` - Full lab report
- `README.md` - Project overview

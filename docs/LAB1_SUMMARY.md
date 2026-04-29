# LAB WORK №1 - SUMMARY
## Railway Station Database System v2.1

---

## 📋 Quick Start

### 1. Setup Database (Windows)
```bash
cd C:\VS_Code\RWSDBv2.1
database\setup_database.bat
```

### 2. Start Server
```bash
python server.py
```

### 3. Test API
```bash
curl http://localhost:8080/api/schedule
curl http://localhost:8080/api/statistics
```

### 4. Open Web Client
```
http://localhost:8080/
```

---

## 🗄️ Database Structure

### Lookup Tables (Read-only for regular users)
| Table | Records | Description |
|-------|---------|-------------|
| `train` | 15 | Trains (number, speed, year, type, cars) |
| `platform` | 10 | Platforms (number, capacity, location) |
| `service` | 15 | Services (name, price, type) |
| `employee` | 15 | Employees (name, position, experience) |

### Operational Tables (Editable)
| Table | Records | Description |
|-------|---------|-------------|
| `schedule` | 500 | **MAIN TABLE** - Train schedules |
| `passenger` | 300 | Passengers information |
| `ticket` | 500 | Ticket sales |
| `appointment` | 100 | Service assignments |
| `work` | 200 | Employee train assignments |

---

## 🔗 API Endpoints

### CRUD Operations
```
GET    /api/{table}           - Get all records
GET    /api/{table}?field=val - Filter records
POST   /api/{table}           - Create record
PUT    /api/{table}/{id}      - Update record
DELETE /api/{table}/{id}      - Delete record
```

### Special Endpoints
```
POST   /api/custom_query  - Execute SQL query
GET    /api/statistics    - Database statistics
POST   /api/backup        - Create backup (superuser)
PATCH  /api/export        - Export to file
```

---

## 🔐 User Roles

### Regular User
- ✅ View all tables
- ✅ Filter data
- ✅ Edit operational tables (schedule, ticket, passenger, etc.)
- ✅ Execute SELECT queries
- ✅ Export data

### Superuser
- ✅ All regular user rights
- ✅ Edit lookup tables (train, platform, service, employee)
- ✅ Create database backups

**Superuser password:** `4444`

---

## 📊 Example Requests

### Get Schedule
```bash
curl http://localhost:8080/api/schedule
```

### Filter Trains
```bash
curl "http://localhost:8080/api/train?type=Пассажирский"
```

### Create Ticket
```bash
curl -X POST http://localhost:8080/api/ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_number": "TKT000501",
    "carriage_number": "5",
    "ticket_price": 1500.00,
    "seat_number": "12В",
    "passenger_number": "PASS000001",
    "train_number": "001А"
  }'
```

### Superuser Action
```bash
curl -X POST http://localhost:8080/api/backup \
  -H "Authorization: Bearer 4444"
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `server.py` | HTTP server (Python + libpq) |
| `config.json` | Database configuration |
| `database/postgres_create_schema_lab1.sql` | Schema creation |
| `database/populate_lookup_tables_lab1.sql` | Lookup data |
| `database/generate_main_data_lab1.sql` | Test data generation |
| `database/setup_database.bat` | Quick setup script |
| `docs/TECHNICAL_SPECIFICATIONS_GOST.md` | GOST specifications |
| `docs/LABORATORY_WORK_REPORT.md` | Lab report |

---

## 🏗️ Architecture

```
┌─────────────┐      HTTP/JSON     ┌─────────────┐
│   Browser   │ ◄────────────────► │   Python    │
│  (React UI) │                    │ HTTP Server │
└─────────────┘                    └──────┬──────┘
                                          │
                                          │ libpq
                                          │ (psycopg2)
                                          ▼
                                   ┌─────────────┐
                                   │ PostgreSQL  │
                                   │   Database  │
                                   └─────────────┘
```

---

## ✅ Lab Requirements Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| HTTP Server | ✅ | Python http.server |
| JSON Format | ✅ | All requests/responses in JSON |
| HTTP Methods | ✅ | GET, POST, PUT, DELETE |
| Unique URLs | ✅ | /api/{table} pattern |
| View Tables | ✅ | GET /api/{table} |
| Filter Data | ✅ | Query parameters |
| Add Records | ✅ | POST /api/{table} |
| Update Records | ✅ | PUT /api/{table}/{id} |
| Delete Records | ✅ | DELETE /api/{table}/{id} |
| Special Queries | ✅ | PATCH /api/custom_query |
| Backups | ✅ | POST /api/backup (superuser) |
| Export | ✅ | PATCH /api/export |
| User Roles | ✅ | User & Superuser |
| Lookup Tables | ✅ | train, platform, service, employee |
| libpq Usage | ✅ | psycopg2-binary (libpq wrapper) |

---

## 📝 Database Schema Details

### Main Table: schedule

```sql
CREATE TABLE schedule (
    schedule_number VARCHAR(20) PRIMARY KEY,
    arrival_time TIME,
    departure_time TIME,
    date DATE DEFAULT CURRENT_DATE,
    carriage_numbering VARCHAR(100),
    train_number VARCHAR(20) REFERENCES train(train_number),
    platform_number VARCHAR(10) REFERENCES platform(platform_number),
    ticket_number VARCHAR(20)
);
```

### Relationships

```
train ──┐
        ├─► schedule
platform ─┘

schedule ──► ticket ──► passenger

employee ──┬──► work ──► train
           └──► appointment ──► service
```

---

## 🚀 Testing

### Verify Record Counts
```sql
SELECT 'schedule' as table_name, COUNT(*) FROM schedule
UNION ALL SELECT 'passenger', COUNT(*) FROM passenger
UNION ALL SELECT 'ticket', COUNT(*) FROM ticket
UNION ALL SELECT 'appointment', COUNT(*) FROM appointment
UNION ALL SELECT 'work', COUNT(*) FROM work;
```

Expected:
- schedule: 500
- passenger: 300
- ticket: 500
- appointment: 100
- work: 200

### Test Views
```sql
SELECT * FROM schedule_details LIMIT 10;
SELECT * FROM ticket_details LIMIT 10;
SELECT * FROM employee_assignments LIMIT 10;
SELECT * FROM train_workload;
```

---

## 📞 Support

For issues or questions:
1. Check `docs/TECHNICAL_SPECIFICATIONS_GOST.md`
2. Review `docs/LABORATORY_WORK_REPORT.md`
3. See `database/setup_database.bat` for setup steps

---

**Version:** 2.1  
**Variant:** 18  
**Date:** March 2026

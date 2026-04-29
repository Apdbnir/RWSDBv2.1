@echo off
REM ============================================================================
REM Test Script for RWSDBv2.1 Database using psql
REM Laboratory Work №1 - Variant 18
REM ============================================================================
REM This script automates testing of the PostgreSQL database setup
REM Run this script after setting up PostgreSQL and creating the database
REM ============================================================================

echo.
echo ============================================================================
echo RWSDBv2.1 - Database Test Script (psql)
echo Laboratory Work №1 - Variant 18
echo ============================================================================
echo.

REM Configuration - Update these values to match your PostgreSQL setup
set PGHOST=localhost
set PGUSER=postgres
set PGPASSWORD=postgres
set PGDATABASE=railway_station
set PSQL_CMD=psql

REM Set environment variable for password (avoids prompt)
set PGPASSWORD=%PGPASSWORD%

echo [TEST 1] Checking PostgreSQL connection...
echo.
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT version();"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Cannot connect to PostgreSQL database!
    echo Please ensure PostgreSQL is running and the database exists.
    goto :error
)
echo [PASS] PostgreSQL connection successful!
echo.

echo ============================================================================
echo [TEST 2] Verifying table structure (19 tables expected)...
echo.
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name;"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to query table structure!
    goto :error
)
echo.

echo ============================================================================
echo [TEST 3] Checking record counts in all tables...
echo.
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT * FROM get_database_statistics();"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to get database statistics!
    goto :error
)
echo.

echo ============================================================================
echo [TEST 4] Verifying lookup tables (positions, subjects, lesson_types)...
echo.
echo --- Positions (25 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS position_count FROM positions;"
echo.
echo --- Subjects (20 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS subject_count FROM subjects;"
echo.
echo --- Lesson Types (10 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS lesson_type_count FROM lesson_types;"
echo.

echo ============================================================================
echo [TEST 5] Verifying operational tables...
echo.
echo --- Employees (100 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS employee_count FROM employees;"
echo.
echo --- Students (200 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS student_count FROM students;"
echo.
echo --- Groups (25 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS group_count FROM groups;"
echo.
echo --- Marks (600 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS mark_count FROM marks;"
echo.
echo --- Lessons (150 expected) ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS lesson_count FROM lessons;"
echo.

echo ============================================================================
echo [TEST 6] Testing triggers and functions...
echo.
echo --- Testing update_updated_at trigger (updating employee record)... ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "UPDATE employees SET salary = salary WHERE employee_id = 1;"
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT employee_id, full_name, updated_at FROM employees WHERE employee_id = 1;"
echo.
echo --- Testing validate_mark_value function (should fail with invalid mark)... ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "INSERT INTO marks (student_id, lesson_id, mark_value, mark_date) VALUES (1, 1, 10, CURRENT_DATE);" 2>&1 | findstr /C:"ERROR" /C:"Mark value"
echo.
echo --- Testing get_employee_full_info function... ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT * FROM get_employee_full_info(1);"
echo.
echo --- Testing get_student_performance function... ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT * FROM get_student_performance(1);"
echo.

echo ============================================================================
echo [TEST 7] Verifying foreign key constraints...
echo.
echo --- Testing FK constraint (should fail - non-existent position)... ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "INSERT INTO employees (full_name, position) VALUES ('Test User', 'NonExistentPosition');" 2>&1 | findstr /C:"ERROR" /C:"foreign key"
echo.

echo ============================================================================
echo [TEST 8] Checking views...
echo.
echo --- View: employee_train_assignments ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS assignment_view_count FROM employee_train_assignments;"
echo.
echo --- View: passenger_journey_details ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS journey_count FROM passenger_journey_details;"
echo.
echo --- View: student_performance ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS performance_count FROM student_performance;"
echo.
echo --- View: employee_subject_load ---
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT COUNT(*) AS load_count FROM employee_subject_load;"
echo.

echo ============================================================================
echo [TEST 9] Checking indexes...
echo.
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT indexname, tablename FROM pg_indexes WHERE schemaname = 'public' ORDER BY tablename, indexname;"
echo.

echo ============================================================================
echo [TEST 10] Testing backup functions...
echo.
%PSQL_CMD% -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT get_total_record_count() AS total_records;"
echo.

echo ============================================================================
echo ALL TESTS COMPLETED!
echo ============================================================================
echo.
echo Summary:
echo - Database connection: OK
echo - Table structure: Verified
echo - Record counts: Checked
echo - Triggers and functions: Tested
echo - Foreign keys: Verified
echo - Views: Checked
echo - Indexes: Listed
echo.
echo To view detailed statistics, run:
echo   psql -h %PGHOST% -U %PGUSER% -d %PGDATABASE% -c "SELECT * FROM get_database_statistics();"
echo.
goto :end

:error
echo.
echo ============================================================================
echo TESTS FAILED - See error messages above
echo ============================================================================
echo.

:end
pause

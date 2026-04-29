@echo off
REM ============================================================================
REM HTTP API Test Script for RWSDBv2.1
REM Laboratory Work №1
REM Variant 18
REM ============================================================================
REM Description: Tests all HTTP API endpoints using curl
REM Usage: Run after starting the server: test_api.bat
REM Requirements: curl must be in PATH, server must be running on port 8080
REM ============================================================================

set SERVER_URL=http://localhost:8080
set ADMIN_TOKEN=4444

echo ============================================================================
echo RWSDBv2.1 HTTP API Test Suite
echo ============================================================================
echo Server URL: %SERVER_URL%
echo.

REM Check if curl is available
where curl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: curl not found in PATH
    echo Please install curl or add it to PATH
    pause
    exit /b 1
)

REM Check if server is running
echo Checking server availability...
curl -s -o nul -w "%%{http_code}" %SERVER_URL%/api/positions >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Server is not responding at %SERVER_URL%
    echo Please start the server first: python server.py
    pause
    exit /b 1
)
echo Server is running!
echo.

REM ============================================================================
REM TEST 1: GET endpoints
REM ============================================================================
echo ============================================================================
echo TEST 1: GET Endpoints (Retrieve Data)
echo ============================================================================

echo.
echo [TEST 1.1] GET /api/positions (Lookup Table)
curl -s %SERVER_URL%/api/positions | python -m json.tool | head -20
echo.

echo [TEST 1.2] GET /api/subjects (Lookup Table)
curl -s %SERVER_URL%/api/subjects | python -m json.tool | head -20
echo.

echo [TEST 1.3] GET /api/lesson-types (Lookup Table)
curl -s %SERVER_URL%/api/lesson-types | python -m json.tool | head -20
echo.

echo [TEST 1.4] GET /api/employees (Main Table)
curl -s %SERVER_URL%/api/employees | python -m json.tool | head -20
echo.

echo [TEST 1.5] GET /api/employees with limit
curl -s "%SERVER_URL%/api/employees?limit=3" | python -m json.tool
echo.

echo [TEST 1.6] GET /api/students
curl -s "%SERVER_URL%/api/students?limit=3" | python -m json.tool | head -20
echo.

echo [TEST 1.7] GET /api/groups
curl -s %SERVER_URL%/api/groups | python -m json.tool | head -20
echo.

REM ============================================================================
REM TEST 2: POST endpoints (Create Records)
REM ============================================================================
echo ============================================================================
echo TEST 2: POST Endpoints (Create Records)
echo ============================================================================

echo.
echo [TEST 2.1] POST /api/employees (Regular user - should succeed)
curl -s -X POST %SERVER_URL%/api/employees ^
  -H "Content-Type: application/json" ^
  -d "{\"full_name\":\"Test User\",\"position\":\"Engineer\",\"experience\":1,\"hire_date\":\"2024-01-01\"}" ^
  | python -m json.tool
echo.

echo [TEST 2.2] POST /api/positions WITHOUT superuser auth (should FAIL)
curl -s -X POST %SERVER_URL%/api/positions ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Position\"}" ^
  | python -m json.tool
echo.

echo [TEST 2.3] POST /api/positions WITH superuser auth (should succeed)
curl -s -X POST %SERVER_URL%/api/positions ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  -d "{\"name\":\"Test Position\"}" ^
  | python -m json.tool
echo.

REM ============================================================================
REM TEST 3: PUT endpoints (Update Records)
REM ============================================================================
echo ============================================================================
echo TEST 3: PUT Endpoints (Update Records)
echo ============================================================================

echo.
echo [TEST 3.1] PUT /api/employees/1 (Update employee)
curl -s -X PUT %SERVER_URL%/api/employees/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"experience\":16}" ^
  | python -m json.tool
echo.

echo [TEST 3.2] PUT /api/positions/1 WITHOUT superuser auth (should FAIL)
curl -s -X PUT %SERVER_URL%/api/positions/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"description\":\"Updated description\"}" ^
  | python -m json.tool
echo.

echo [TEST 3.3] PUT /api/positions/1 WITH superuser auth (should succeed)
curl -s -X PUT %SERVER_URL%/api/positions/1 ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  -d "{\"description\":\"Updated description\"}" ^
  | python -m json.tool
echo.

REM ============================================================================
REM TEST 4: DELETE endpoints
REM ============================================================================
echo ============================================================================
echo TEST 4: DELETE Endpoints
echo ============================================================================

echo.
echo [TEST 4.1] DELETE /api/positions (last position) WITHOUT auth (should FAIL)
curl -s -X DELETE %SERVER_URL%/api/positions/1 ^
  | python -m json.tool
echo.

echo [TEST 4.2] DELETE /api/positions (last position) WITH auth (should succeed)
curl -s -X DELETE %SERVER_URL%/api/positions/1 ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  | python -m json.tool
echo.

REM ============================================================================
REM TEST 5: Custom Query and Export
REM ============================================================================
echo ============================================================================
echo TEST 5: Custom Query and Export
echo ============================================================================

echo.
echo [TEST 5.1] PATCH /api/custom_query
curl -s -X PATCH %SERVER_URL%/api/custom_query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"SELECT * FROM employees LIMIT 5\"}" ^
  | python -m json.tool
echo.

echo [TEST 5.2] PATCH /api/statistics
curl -s -X PATCH %SERVER_URL%/api/statistics ^
  | python -m json.tool | head -30
echo.

echo [TEST 5.3] PATCH /api/export (JSON format)
curl -s -X PATCH %SERVER_URL%/api/export ^
  -H "Content-Type: application/json" ^
  -d "{\"table\":\"employees\",\"format\":\"json\",\"limit\":3}" ^
  | python -m json.tool | head -30
echo.

REM ============================================================================
REM TEST 6: Backup (Superuser Only)
REM ============================================================================
echo ============================================================================
echo TEST 6: Backup Endpoint (Superuser Only)
echo ============================================================================

echo.
echo [TEST 6.1] POST /api/backup WITHOUT auth (should FAIL)
curl -s -X POST %SERVER_URL%/api/backup ^
  | python -m json.tool
echo.

echo [TEST 6.2] POST /api/backup WITH auth (should succeed)
curl -s -X POST %SERVER_URL%/api/backup ^
  -H "Authorization: Bearer %ADMIN_TOKEN%" ^
  | python -m json.tool
echo.

REM ============================================================================
REM TEST 7: Error Handling
REM ============================================================================
echo ============================================================================
echo TEST 7: Error Handling
echo ============================================================================

echo.
echo [TEST 7.1] Invalid endpoint
curl -s %SERVER_URL%/api/invalid_table | python -m json.tool
echo.

echo [TEST 7.2] Invalid query (non-SELECT)
curl -s -X PATCH %SERVER_URL%/api/custom_query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"DELETE FROM employees\"}" ^
  | python -m json.tool
echo.

REM ============================================================================
REM SUMMARY
REM ============================================================================
echo ============================================================================
echo TEST SUMMARY
echo ============================================================================
echo All API tests completed!
echo.
echo To view full JSON responses, run individual curl commands manually.
echo.
echo Example:
echo   curl %SERVER_URL%/api/employees ^| python -m json.tool
echo ============================================================================

pause

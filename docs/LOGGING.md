# Logging System Documentation

## Overview

The RWSDBv2.1 project now includes comprehensive logging throughout both backend and frontend components to help with debugging, monitoring, and auditing.

## Backend Logging

### Configuration

- **Location**: `backend/server.py`
- **Log Directory**: `logs/` (in project root)
- **Log Files**:
  - `logs/server.log` - Main application log (10MB max, 5 backups)
  - `logs/error.log` - Error-only log (5MB max, 3 backups)

### Log Levels

- **DEBUG**: Detailed debugging information (request bodies, SQL queries, etc.)
- **INFO**: General operational information (requests, responses, operations)
- **WARNING**: Potentially harmful situations (failed auth attempts, permission denied)
- **ERROR**: Error conditions that allow the system to continue

### What Gets Logged

#### HTTP Requests (RequestHandler)
- All incoming requests with method, path, and client IP
- Response status codes and sizes
- Request headers (in debug mode)

#### Authentication
- Successful login attempts with client IP
- Failed login attempts with client IP
- Missing credentials

#### CRUD Operations
- INSERT operations with table names
- UPDATE operations with table names and record IDs
- DELETE operations with table names and record IDs
- Permission denied events

#### Custom Queries
- All executed SQL queries (first 200 chars for audit trail)
- Number of rows returned
- Security violations (blocked keywords, non-SELECT queries)

#### Export Operations
- Export format (JSON, CSV, Excel)
- Table name or custom query flag
- Number of rows exported

#### Database Operations
- Connection/disconnection events
- Backup creation
- Database initialization steps

### Log Format

**Console Output:**
```
2026-04-03 14:23:45,123 - server - INFO - Request: GET /api/passenger from 127.0.0.1
```

**File Output (more detailed):**
```
2026-04-03 14:23:45,123 - server - INFO - [server.py:892] - Request: GET /api/passenger from 127.0.0.1
```

## Frontend Logging

### Configuration

- **Location**: `web/src/services/api.js`
- **Output**: Browser console

### Log Levels

- **DEBUG**: Detailed request/response data (only in development mode)
- **INFO**: Request/response events with timestamps
- **WARN**: Authentication failures, token clearing
- **ERROR**: Failed requests, error details

### Log Format

```
[INFO] 2026-04-03T14:23:45.123Z - GET /api/passenger
[INFO] 2026-04-03T14:23:45.234Z - Response 200: GET /api/passenger
[ERROR] 2026-04-03T14:23:45.345Z - Response error 401: POST /api/passenger
```

## BerkeleyDB Converter Logging

The converter now uses the Python logging module instead of print statements:

- Connection events
- Table conversion progress
- Record counts
- Error conditions

## Viewing Logs

### Backend Logs

**During Development:**
- Logs appear in console where you run the server
- Also written to `logs/server.log` and `logs/error.log`

**Production Monitoring:**
```bash
# View main log
tail -f logs/server.log

# View only errors
tail -f logs/error.log
```

### Frontend Logs

Open browser developer tools (F12) and view the Console tab. All API requests and responses are logged with timestamps.

## Log Rotation

Logs are automatically rotated to prevent disk space issues:

- **server.log**: Rotates at 10MB, keeps 5 backups
- **error.log**: Rotates at 5MB, keeps 3 backups

Old logs are automatically deleted according to these limits.

## Security Considerations

- Custom SQL queries are logged for audit trail (first 200 characters)
- Failed authentication attempts are logged with IP addresses
- Permission violations are logged at WARNING level
- Sensitive data (passwords) are NOT logged

## Troubleshooting

### Backend Issues

**No logs appearing:**
- Check that the `logs/` directory exists and is writable
- Verify logging is properly initialized in `server.py`

**Too much logging:**
- Change console handler level from INFO to WARNING in `setup_logging()`
- Debug logs only appear in file, not console

### Frontend Issues

**No logs in console:**
- Open browser developer tools (F12)
- Ensure console filtering isn't hiding logs
- Check that you're using the updated `api.js`

## Adding New Log Points

When adding new functionality, use the existing `logger` instance:

```python
logger.info("Descriptive message about what happened")
logger.warning("Potentially problematic event")
logger.error("Error condition with details", exc_info=True)  # includes traceback
logger.debug("Detailed debugging info", extra={'key': 'value'})
```

For frontend, use the `logger` object in `api.js`:

```javascript
logger.info('User action description');
logger.warn('Warning about condition');
logger.error('Error occurred', error_object);
logger.debug('Detailed data', data_object); // Only in development
```

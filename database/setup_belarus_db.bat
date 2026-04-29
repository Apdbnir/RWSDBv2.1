@echo off
set PGPASSWORD=postgres
echo Dropping and recreating database...
psql -h localhost -U postgres -d postgres -c "DROP DATABASE IF EXISTS \"Railway sstation\";"
psql -h localhost -U postgres -d postgres -c "CREATE DATABASE \"Railway sstation\";"

echo Creating schema...
psql -h localhost -U postgres -d "Railway sstation" -f database\postgres_create_schema_belarus.sql

echo Populating with Belarusian data...
psql -h localhost -U postgres -d "Railway sstation" -f database\populate_belarus_data.sql

echo Verifying data...
psql -h localhost -U postgres -d "Railway sstation" -c "SELECT 'train' as table_name, COUNT(*) as count FROM train UNION ALL SELECT 'platform', COUNT(*) FROM platform UNION ALL SELECT 'schedule', COUNT(*) FROM schedule UNION ALL SELECT 'passenger', COUNT(*) FROM passenger UNION ALL SELECT 'ticket', COUNT(*) FROM ticket UNION ALL SELECT 'service', COUNT(*) FROM service UNION ALL SELECT 'employee', COUNT(*) FROM employee;"

echo Done!
pause

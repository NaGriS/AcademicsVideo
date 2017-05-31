cd %PROGRAMFILES%\PostgreSQL\9.6\bin\
cmd /C psql.exe -h localhost -p 5432 -U postgres -c "CREATE DATABASE academicsvideo_db"
cmd /C psql.exe -h localhost -p 5432 -U postgres -d academicsvideo_db -c "CREATE USER superuser WITH PASSWORD 'Password'"
cmd /C psql.exe -h localhost -p 5432 -U postgres -d academicsvideo_db -c "ALTER ROLE superuser SET client_encoding TO 'utf8'"
cmd /C psql.exe -h localhost -p 5432 -U postgres -d academicsvideo_db -c "ALTER ROLE superuser SET default_transaction_isolation TO 'read committed'"
cmd /C psql.exe -h localhost -p 5432 -U postgres -d academicsvideo_db -c "ALTER ROLE superuser SET timezone TO 'UTC'"
cmd /C psql.exe -h localhost -p 5432 -U postgres -d academicsvideo_db -c "GRANT ALL PRIVILEGES ON DATABASE academicsVideo_db TO superuser"
cmd /C pause
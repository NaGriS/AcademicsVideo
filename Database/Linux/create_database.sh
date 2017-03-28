#!/bin/bash
psql -c "CREATE DATABASE academicsvideo_db"
psql -d academicsvideo_db -c "CREATE USER superuser WITH PASSWORD 'Password'"
psql -d academicsvideo_db -c "ALTER ROLE superuser SET client_encoding TO 'utf8'"
psql -d academicsvideo_db -c "ALTER ROLE superuser SET default_transaction_isolation TO 'read committed'"
psql -d academicsvideo_db -c "ALTER ROLE superuser SET timezone TO 'UTC'"
psql -d academicsvideo_db -c "GRANT ALL PRIVILEGES ON DATABASE academicsVideo_db TO superuser"

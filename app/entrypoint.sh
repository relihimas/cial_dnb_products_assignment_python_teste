#!/bin/bash
set -e

# Start PostgreSQL service
service postgresql start

# Run PostgreSQL commands
su -u postgres psql <<EOF
ALTER USER postgres PASSWORD 'postgres';
CREATE DATABASE cial;
\c cial
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    stock TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
EOF

# Create backup directory if not exists
mkdir -p /var/backups/postgres

# Backup database
pg_dump cial > /var/backups/postgres/cial_backup.sql

# Start the Flask application
nohup python3 /app/app/stock_server.py 

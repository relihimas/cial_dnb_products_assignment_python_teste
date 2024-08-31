#!/bin/bash
set -e

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

mkdir -p /var/backups/postgres

pg_dump cial > /var/backups/postgres/cial_backup.sql
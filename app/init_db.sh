#!/bin/bash

sudo service postgresql start

sleep 10

sudo -u postgres psql -c "CREATE DATABASE stock_db;"
sudo -u postgres psql -c "CREATE USER stock_user WITH ENCRYPTED PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE stock_db TO stock_user;"
sudo -u postgres psql -d stock_db -c "CREATE TABLE stock (id SERIAL PRIMARY KEY, stock TEXT NOT NULL, amount NUMERIC(10, 2) NOT NULL, created_on TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);"

echo "Database and table created successfully"

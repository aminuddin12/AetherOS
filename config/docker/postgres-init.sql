-- AetherOS PostgreSQL Initialization Script
-- This script sets up the initial database schema and users

-- Create database if not exists
CREATE DATABASE aetheros;

-- Create test database if not exists
CREATE DATABASE aetheros_test;

-- Create main user
CREATE USER aetheros WITH PASSWORD 'aetheros';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE aetheros TO aetheros;
GRANT ALL PRIVILEGES ON DATABASE aetheros_test TO aetheros;

-- Create schema for AetherOS
\c aetheros
CREATE SCHEMA IF NOT EXISTS aetheros;
CREATE SCHEMA IF NOT EXISTS workspace;
CREATE SCHEMA IF NOT EXISTS storage;
CREATE SCHEMA IF NOT EXISTS repository;
CREATE SCHEMA IF NOT EXISTS artifact;
CREATE SCHEMA IF NOT EXISTS organization;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA aetheros TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA workspace TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA storage TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA repository TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA artifact TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA organization TO aetheros;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set up test database schema
\c aetheros_test
CREATE SCHEMA IF NOT EXISTS aetheros;
CREATE SCHEMA IF NOT EXISTS workspace;
CREATE SCHEMA IF NOT EXISTS storage;
CREATE SCHEMA IF NOT EXISTS repository;
CREATE SCHEMA IF NOT EXISTS artifact;
CREATE SCHEMA IF NOT EXISTS organization;

GRANT ALL PRIVILEGES ON SCHEMA aetheros TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA workspace TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA storage TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA repository TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA artifact TO aetheros;
GRANT ALL PRIVILEGES ON SCHEMA organization TO aetheros;
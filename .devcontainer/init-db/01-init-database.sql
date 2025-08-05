-- =============================================================================
-- DATABASE INITIALIZATION SCRIPT
-- =============================================================================
-- This script initializes the PostgreSQL database for the Inventory API
-- It runs automatically when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist (handled by POSTGRES_DB env var)
-- CREATE DATABASE IF NOT EXISTS inventory_api;

-- Connect to the database
\c inventory_api;

-- =============================================================================
-- EXTENSIONS
-- =============================================================================
-- Enable useful PostgreSQL extensions

-- UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- HSTORE extension for key-value storage
CREATE EXTENSION IF NOT EXISTS "hstore";

-- PostGIS extension (uncomment if you need geospatial features)
-- CREATE EXTENSION IF NOT EXISTS "postgis";

-- Full text search extensions
CREATE EXTENSION IF NOT EXISTS "unaccent";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- =============================================================================
-- CUSTOM FUNCTIONS
-- =============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to generate a random string
CREATE OR REPLACE FUNCTION random_string(length INTEGER)
RETURNS TEXT AS $$
DECLARE
    chars TEXT := 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    result TEXT := '';
    i INTEGER := 0;
BEGIN
    IF length < 0 THEN
        RAISE EXCEPTION 'Given length cannot be less than 0';
    END IF;
    FOR i IN 1..length LOOP
        result := result || substr(chars, floor(random() * length(chars))::INTEGER + 1, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- INITIAL DATA SETUP
-- =============================================================================

-- Create a schema for application data (optional)
-- CREATE SCHEMA IF NOT EXISTS inventory;

-- Grant permissions to the application user
GRANT ALL PRIVILEGES ON DATABASE inventory_api TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- =============================================================================
-- PERFORMANCE OPTIMIZATIONS
-- =============================================================================

-- Set some performance-related parameters
ALTER DATABASE inventory_api SET shared_preload_libraries = 'pg_stat_statements';

-- =============================================================================
-- LOGGING
-- =============================================================================

-- Log database initialization
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully';
    RAISE NOTICE 'Extensions enabled: uuid-ossp, hstore, unaccent, pg_trgm';
    RAISE NOTICE 'Custom functions created: update_updated_at_column, random_string';
END $$;
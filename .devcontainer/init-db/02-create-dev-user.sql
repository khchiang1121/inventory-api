-- =============================================================================
-- DEVELOPMENT USER SETUP
-- =============================================================================
-- This script creates additional database users and configurations for development

-- Connect to the inventory_api database
\c inventory_api;

-- =============================================================================
-- CREATE DEVELOPMENT USERS
-- =============================================================================

-- Create a read-only user for reporting/analytics
CREATE USER IF NOT EXISTS inventory_readonly WITH PASSWORD 'readonly123';

-- Grant read-only permissions
GRANT CONNECT ON DATABASE inventory_api TO inventory_readonly;
GRANT USAGE ON SCHEMA public TO inventory_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO inventory_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO inventory_readonly;

-- Ensure future tables are also readable by readonly user
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO inventory_readonly;

-- Create a development user with more privileges (for testing, etc.)
CREATE USER IF NOT EXISTS inventory_dev WITH PASSWORD 'dev123';

-- Grant development permissions
GRANT CONNECT ON DATABASE inventory_api TO inventory_dev;
GRANT ALL PRIVILEGES ON SCHEMA public TO inventory_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO inventory_dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO inventory_dev;

-- Ensure future tables are accessible by dev user
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inventory_dev;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO inventory_dev;

-- =============================================================================
-- DEVELOPMENT DATABASE SETTINGS
-- =============================================================================

-- Enable statement logging for development (helps with debugging)
ALTER DATABASE inventory_api SET log_statement = 'all';
ALTER DATABASE inventory_api SET log_min_duration_statement = 0;

-- Enable query statistics
ALTER DATABASE inventory_api SET track_activities = on;
ALTER DATABASE inventory_api SET track_counts = on;
ALTER DATABASE inventory_api SET track_functions = all;

-- =============================================================================
-- CREATE DEVELOPMENT SCHEMAS (Optional)
-- =============================================================================

-- Create a testing schema for running tests
CREATE SCHEMA IF NOT EXISTS testing;
GRANT ALL PRIVILEGES ON SCHEMA testing TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA testing TO inventory_dev;

-- Create a temporary schema for ad-hoc queries
CREATE SCHEMA IF NOT EXISTS temp;
GRANT ALL PRIVILEGES ON SCHEMA temp TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA temp TO inventory_dev;
GRANT USAGE ON SCHEMA temp TO inventory_readonly;

-- =============================================================================
-- SAMPLE DATA SETUP (Optional)
-- =============================================================================

-- Note: Sample data will be created by Django fixtures or management commands
-- This section is reserved for any database-level sample data

-- =============================================================================
-- DEVELOPMENT VIEWS
-- =============================================================================

-- Create a view to show database statistics
CREATE OR REPLACE VIEW dev_stats AS
SELECT 
    schemaname,
    tablename,
    attname as column_name,
    n_distinct,
    correlation
FROM pg_stats 
WHERE schemaname = 'public'
ORDER BY schemaname, tablename, attname;

GRANT SELECT ON dev_stats TO inventory_dev;
GRANT SELECT ON dev_stats TO inventory_readonly;

-- Create a view to show table sizes
CREATE OR REPLACE VIEW table_sizes AS
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

GRANT SELECT ON table_sizes TO inventory_dev;
GRANT SELECT ON table_sizes TO inventory_readonly;

-- =============================================================================
-- LOGGING AND MONITORING
-- =============================================================================

-- Log development user creation
DO $$
BEGIN
    RAISE NOTICE 'Development users created:';
    RAISE NOTICE '  - inventory_readonly (read-only access)';
    RAISE NOTICE '  - inventory_dev (full development access)';
    RAISE NOTICE 'Development schemas created:';
    RAISE NOTICE '  - testing (for running tests)';
    RAISE NOTICE '  - temp (for ad-hoc queries)';
    RAISE NOTICE 'Development views created:';
    RAISE NOTICE '  - dev_stats (database statistics)';
    RAISE NOTICE '  - table_sizes (table size information)';
END $$;
#!/bin/bash

###############################################################################
# PostgreSQL Database Setup Script
# Creates database and user for Tangail Doctors project
# Run this as root user
###############################################################################

set -e

echo "====================================================================="
echo "  Phase 3: PostgreSQL Database Setup"
echo "====================================================================="

# Generate random password for database user
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

echo "📊 Creating PostgreSQL database and user..."

# Create database and user
sudo -u postgres psql <<EOF
-- Create database
CREATE DATABASE tangail_doctors;

-- Create user with password
CREATE USER tangail_user WITH PASSWORD '$DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE tangail_doctors TO tangail_user;

-- Connect to database
\c tangail_doctors

-- Grant schema privileges (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO tangail_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tangail_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tangail_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tangail_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tangail_user;

-- Exit
\q
EOF

echo ""
echo "✅ Database created successfully!"
echo ""
echo "====================================================================="
echo "  Database Connection Details (SAVE THIS!)"
echo "====================================================================="
echo ""
echo "Database Name: tangail_doctors"
echo "Database User: tangail_user"
echo "Database Password: $DB_PASSWORD"
echo "Database Host: localhost"
echo "Database Port: 5432"
echo ""
echo "DATABASE_URL format:"
echo "postgresql://tangail_user:$DB_PASSWORD@localhost:5432/tangail_doctors"
echo ""
echo "====================================================================="
echo ""
echo "⚠️  IMPORTANT: Save these credentials! You'll need them for .env file"
echo ""

# Save to file
cat > /root/database-credentials.txt <<EOF
Database Credentials - Tangail Doctors
Created: $(date)

Database Name: tangail_doctors
Database User: tangail_user
Database Password: $DB_PASSWORD
Database Host: localhost
Database Port: 5432

DATABASE_URL:
postgresql://tangail_user:$DB_PASSWORD@localhost:5432/tangail_doctors
EOF

echo "✅ Credentials saved to: /root/database-credentials.txt"
echo ""
echo "Test connection:"
echo "psql -U tangail_user -d tangail_doctors -h localhost"
echo ""

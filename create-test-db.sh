#!/bin/bash
set -e
set -u

echo "Creating test Database"

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" <<-EOSQL
    CREATE DATABASE ${POSTGRES_TEST_DB};
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_TEST_DB} TO ${POSTGRES_USER};
EOSQL

echo "Test Database created successfully"

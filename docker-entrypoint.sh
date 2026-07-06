#!/bin/bash
set -e

# AetherOS Docker Entrypoint Script
# This script handles container initialization and startup

echo "=== AetherOS Container Starting ==="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Set default environment variables if not provided
: ${AETHEROS_ENV:=development}
: ${AETHEROS_PORT:=8000}
: ${AETHEROS_HOST:=0.0.0.0}
: ${AETHEROS_WORKERS:=4}
: ${AETHEROS_TIMEOUT:=300}
: ${AETHEROS_LOG_LEVEL:=info}

# Export environment variables
export AETHEROS_ENV
 export AETHEROS_PORT
 export AETHEROS_HOST
 export AETHEROS_WORKERS
 export AETHEROS_TIMEOUT
 export AETHEROS_LOG_LEVEL

# Print configuration
echo "AetherOS Environment: ${AETHEROS_ENV}"
echo "AetherOS Port: ${AETHEROS_PORT}"
echo "AetherOS Host: ${AETHEROS_HOST}"
echo "AetherOS Workers: ${AETHEROS_WORKERS}"
echo "AetherOS Timeout: ${AETHEROS_TIMEOUT}"
echo "AetherOS Log Level: ${AETHEROS_LOG_LEVEL}"

# Check if we're running as root and warn
if [ "$(id -u)" -eq 0 ]; then
    echo "WARNING: Container is running as root user. This is not recommended for production."
fi

# Handle different startup commands based on arguments
case "$1" in
    "dev"|"development")
        echo "Starting AetherOS in development mode..."
        exec python -m aether_cli.app --dev
        ;;
    "prod"|"production")
        echo "Starting AetherOS in production mode..."
        exec gunicorn --bind "${AETHEROS_HOST}:${AETHEROS_PORT}" --workers "${AETHEROS_WORKERS}" --timeout "${AETHEROS_TIMEOUT}" aether_cli.app:app
        ;;
    "test"|"tests")
        echo "Running AetherOS tests..."
        exec pytest /workspace/tests -v
        ;;
    "bash"|"sh"|"shell")
        echo "Starting interactive shell..."
        exec "$@"
        ;;
    "migrate"|"migration")
        echo "Running database migrations..."
        # Add migration command here when available
        exec python -c "print('Migrations would run here')"
        ;;
    "worker"|"background")
        echo "Starting background worker..."
        # Add worker command here when available
        exec python -c "print('Worker would start here')"
        ;;
    *)
        echo "Starting with custom command: $@"
        exec "$@"
        ;;
esac
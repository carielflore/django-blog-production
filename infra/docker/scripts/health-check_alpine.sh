#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"

cd "$DOCKER_DIR"

echo "Checking Docker services status..."

sleep 15

if docker-compose ps | grep -q "Exit\|unhealthy"; then
    echo "Some services failed:"
    docker-compose ps
    exit 1
else
    echo "All services are running healthy:"
    docker-compose ps
    exit 0
fi

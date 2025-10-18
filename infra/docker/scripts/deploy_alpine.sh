#!/bin/sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$DOCKER_DIR")")"

echo "Deploying Django application from: $DOCKER_DIR"

cd "$DOCKER_DIR"

if ! command -v docker &> /dev/null; then
	echo "Docker is not installed"
	exit 1
fi

echo "Building and starting containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "Waiting for services to start..."
sleep 15

echo "Running health checks..."
"$SCRIPT_DIR/health-check_alpine.sh"

echo "Deployment completed successfully"

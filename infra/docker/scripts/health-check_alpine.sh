#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"

cd "$DOCKER_DIR"

echo "Docker services health check:"

services="django:8000/ nginx:80/ prometheus:9090/-/healthy grafana:3000/api/health node_exporter:9100/metrics nginx_exporter:9113/metrics"

all_healthy=true

for service in $services; do
    name="${service%:*}"
    endpoint="${service#*:}"

    if curl -s -f --connect-timeout 5 "http://${name}:${endpoint}" > /dev/null; then
        echo "$name is healthy"
    else
        echo "$name health check is failed"
        all_healthy=false
    fi
done

if [ "$all_healthy" = "false" ]; then
    echo "Some services are unhealthy"
    exit 1
else
    echo "All services are healthy"
fi

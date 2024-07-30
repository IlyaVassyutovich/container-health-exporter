#!/usr/bin/env bash

set -e

docker build \
    --tag container-health-exporter/builder/copy-deb:latest \
    -f builder/Dockerfile \
    --target copy-deb \
    --build-arg HTTP_PROXY=http://hermes.myth-vibes.ts.net:9051 \
    --build-arg HTTPS_PROXY=http://hermes.myth-vibes.ts.net:9051 \
        .
docker run \
    -it \
    --rm \
    --name container-health-exporter-builder \
    --mount "type=bind,src=$(realpath ./artifacts/),dst=/artifacts" \
        container-health-exporter/builder/copy-deb:latest

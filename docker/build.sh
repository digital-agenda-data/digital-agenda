#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR="$(dirname "$SCRIPT_DIR")"

(
  cd -- "$SCRIPT_DIR" && \
  docker build -t digital-agenda-base -f base.docker . && \
  mkdir -p wheels && \
  docker build -t digital-agenda-builder -f build.docker . && \
  docker run --rm \
         -v "$APP_DIR":/app \
         -v "$(pwd)"/wheels:/wheelhouse \
         digital-agenda-builder && \
  docker build -t digital-agenda-app -f app.docker . && \
  docker build -t digital-agenda-nginx -f nginx.docker .
)

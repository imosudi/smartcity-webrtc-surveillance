#!/bin/bash

# Repository root
REPO="webrtc-iot-surveillance-gateway"

# Create root directory
mkdir -p "$REPO"

# Create root-level files
touch "$REPO/README.md"
touch "$REPO/LICENSE"
touch "$REPO/requirements.txt"
touch "$REPO/app.py"

# Create templates directory and placeholder
mkdir -p "$REPO/templates"
touch "$REPO/templates/dashboard.html"

# Create static directory and placeholder
mkdir -p "$REPO/static"
touch "$REPO/static/surveillance.js"

# Create docs directory and placeholder SVGs
mkdir -p "$REPO/docs"
touch "$REPO/docs/architecture.svg"
touch "$REPO/docs/signalling-flow.svg"
touch "$REPO/docs/webrtc-security-stack.svg"

# Create deployment directory and placeholder files
mkdir -p "$REPO/deployment"
touch "$REPO/deployment/nginx.conf"
touch "$REPO/deployment/coturn.conf"
touch "$REPO/deployment/systemd.service"

# Create screenshots directory
mkdir -p "$REPO/screenshots"
touch "$REPO/screenshots/live-preview.png"

# Create notes directory
mkdir -p "$REPO/notes"
touch "$REPO/notes/smart-city-architecture.md"

# Success message
echo "Repository structure for '$REPO' created successfully."


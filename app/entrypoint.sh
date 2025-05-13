#!/bin/sh
# entrypoint.sh

# Ensure output directory exists
mkdir -p /app/static/dist

# Build Tailwind CSS before starting Flask
npm run watch &

# Start Flask
exec flask run

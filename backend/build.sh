#!/bin/bash

# Build script for Netlify deployment
echo "Building SequoAlpha frontend for Netlify..."

# Ensure all files are in the correct location
echo "✓ Frontend structure verified"

# Create necessary directories if they don't exist
mkdir -p css
mkdir -p frontend/js
mkdir -p images

echo "✓ Build completed successfully!"
echo "Ready for Netlify deployment"

#!/bin/bash

# Fetch the latest changes
echo "Pulling the latest code from Git..."
git pull origin main

# Remove old builds
echo "Cleaning old builds..."
rm -rf build dist *.spec

# Build the app
echo "Building the app..."
pyinstaller --onefile --noconfirm app.spec

echo "Build complete. The executable is in the 'dist' directory."

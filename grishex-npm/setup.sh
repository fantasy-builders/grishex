#!/bin/bash

# Grishex npm package setup script

echo "Setting up Grishex Language npm package..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Make bin file executable
echo "Making bin file executable..."
chmod +x bin/grishex.js

# Build the package
echo "Building the package..."
npm run build

# Run tests
echo "Running tests..."
npm test

# Link package globally (for development)
echo "Linking package globally for development..."
npm link

echo "Setup complete!"
echo "You can now use the 'grishex' command to create, compile, and deploy smart contracts."
echo "Try 'grishex --help' to see available commands." 
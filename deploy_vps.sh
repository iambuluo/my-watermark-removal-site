#!/bin/bash

# Update system packages
echo "Updating system..."
sudo apt-get update -y
sudo apt-get install -y git curl

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "Docker installed."
else
    echo "Docker is already installed."
fi

# Clone the repository
REPO_URL="https://github.com/iambuluo/my-watermark-removal-site.git"
APP_DIR="my-watermark-removal-site"

if [ -d "$APP_DIR" ]; then
    echo "Updating repository..."
    cd $APP_DIR
    git pull
else
    echo "Cloning repository..."
    git clone $REPO_URL
    cd $APP_DIR
fi

# Build Docker image
echo "Building Docker image (this may take a few minutes)..."
sudo docker build -t iopaint-serverless .

# Stop and remove existing container if running
if [ "$(sudo docker ps -q -f name=iopaint-app)" ]; then
    echo "Stopping existing container..."
    sudo docker stop iopaint-app
    sudo docker rm iopaint-app
fi

# Run new container
echo "Starting application..."
sudo docker run -d -p 80:8000 --restart always --name iopaint-app iopaint-serverless

echo "=========================================="
echo "Deployment Complete!"
echo "Your app should be running at: http://$(curl -s ifconfig.me)"
echo "=========================================="

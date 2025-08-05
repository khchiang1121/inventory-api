#!/bin/bash
set -e

echo "🚀 Setting up Inventory API development environment..."

# Source configuration if it exists
if [ -f "/workspace/.devcontainer/config/proxy.conf" ]; then
    echo "📋 Loading proxy configuration..."
    source /workspace/.devcontainer/config/proxy.conf
fi

# Configure apt proxy if HTTP_PROXY is set
if [ ! -z "$HTTP_PROXY" ]; then
    echo "🔧 Configuring apt proxy..."
    echo "Acquire::http::Proxy \"$HTTP_PROXY\";" | sudo tee /etc/apt/apt.conf.d/99proxy
    echo "Acquire::https::Proxy \"$HTTP_PROXY\";" | sudo tee -a /etc/apt/apt.conf.d/99proxy
fi

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    jq \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Configure pip proxy if HTTP_PROXY is set
if [ ! -z "$HTTP_PROXY" ]; then
    echo "🔧 Configuring pip proxy..."
    mkdir -p ~/.pip
    cat > ~/.pip/pip.conf << EOF
[global]
proxy = $HTTP_PROXY
https_proxy = $HTTP_PROXY
EOF
fi

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install development tools
echo "📦 Installing development tools..."
pip install \
    black \
    flake8 \
    isort \
    mypy \
    pylint \
    pytest \
    pytest-django \
    pytest-cov \
    pre-commit

# Configure git if proxy is set
if [ ! -z "$HTTP_PROXY" ]; then
    echo "🔧 Configuring git proxy..."
    git config --global http.proxy "$HTTP_PROXY"
    git config --global https.proxy "$HTTP_PROXY"
fi

# Create .env file if it doesn't exist
if [ ! -f "/workspace/.env" ]; then
    echo "📝 Creating .env file..."
    cat > /workspace/.env << EOF
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database settings (external database)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Proxy settings (if needed)
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=http://proxy.example.com:8080
# NO_PROXY=localhost,127.0.0.1
EOF
fi

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
cd /workspace
pre-commit install

# Make setup script executable
chmod +x /workspace/.devcontainer/setup.sh

echo "✅ Development environment setup complete!"
echo "🎯 You can now start developing your Inventory API!"
echo "📝 Don't forget to update the .env file with your actual database credentials." 
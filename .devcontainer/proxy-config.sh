#!/bin/bash

# =============================================================================
# PROXY CONFIGURATION SCRIPT
# =============================================================================
# This script configures various tools to work with corporate proxies
# Usage: proxy-config.sh [tool|system]
# Examples:
#   proxy-config.sh apt     - Configure APT package manager
#   proxy-config.sh pip     - Configure pip
#   proxy-config.sh git     - Configure git
#   proxy-config.sh system  - Configure system-wide proxy settings
#   proxy-config.sh all     - Configure all tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables
if [ -f "/workspace/.env" ]; then
    export $(grep -v '^#' /workspace/.env | xargs)
fi

if [ -f "/workspace/.devcontainer/env.local" ]; then
    export $(grep -v '^#' /workspace/.devcontainer/env.local | xargs)
fi

# Check if proxy is configured
check_proxy_config() {
    if [ -n "$HTTP_PROXY" ] || [ -n "$HTTPS_PROXY" ]; then
        return 0
    else
        print_warning "No proxy configuration found in environment variables"
        return 1
    fi
}

# Configure APT proxy
configure_apt_proxy() {
    print_info "Configuring APT proxy settings..."
    
    if check_proxy_config; then
        # Create APT proxy configuration
        sudo tee /etc/apt/apt.conf.d/95proxies > /dev/null <<EOF
Acquire::http::Proxy "$HTTP_PROXY";
Acquire::https::Proxy "$HTTPS_PROXY";
EOF
        
        if [ -n "$NO_PROXY" ]; then
            echo "Acquire::http::Proxy::localhost \"DIRECT\";" | sudo tee -a /etc/apt/apt.conf.d/95proxies > /dev/null
            echo "Acquire::http::Proxy::127.0.0.1 \"DIRECT\";" | sudo tee -a /etc/apt/apt.conf.d/95proxies > /dev/null
        fi
        
        print_success "APT proxy configured"
    else
        print_info "Skipping APT proxy configuration - no proxy settings found"
    fi
    
    # Configure custom APT mirrors if specified
    if [ -n "$APT_MIRROR" ]; then
        print_info "Configuring custom APT mirrors..."
        sudo sed -i.bak "s|http://archive.ubuntu.com/ubuntu|$APT_MIRROR|g" /etc/apt/sources.list
        if [ -n "$APT_SECURITY_MIRROR" ]; then
            sudo sed -i "s|http://security.ubuntu.com/ubuntu|$APT_SECURITY_MIRROR|g" /etc/apt/sources.list
        fi
        print_success "APT mirrors configured"
    fi
}

# Configure pip proxy
configure_pip_proxy() {
    print_info "Configuring pip proxy settings..."
    
    # Create pip config directory
    mkdir -p ~/.config/pip
    
    if check_proxy_config; then
        # Create pip configuration
        cat > ~/.config/pip/pip.conf <<EOF
[global]
proxy = $HTTP_PROXY
trusted-host = pypi.org
               pypi.python.org 
               files.pythonhosted.org
EOF
        
        if [ -n "$PIP_TRUSTED_HOST" ]; then
            echo "trusted-host = $PIP_TRUSTED_HOST" >> ~/.config/pip/pip.conf
        fi
        
        print_success "pip proxy configured"
    else
        print_info "Skipping pip proxy configuration - no proxy settings found"
    fi
    
    # Configure custom PyPI index if specified
    if [ -n "$PIP_INDEX_URL" ]; then
        echo "index-url = $PIP_INDEX_URL" >> ~/.config/pip/pip.conf
        print_success "pip index URL configured"
    fi
    
    if [ -n "$PIP_EXTRA_INDEX_URL" ]; then
        echo "extra-index-url = $PIP_EXTRA_INDEX_URL" >> ~/.config/pip/pip.conf
        print_success "pip extra index URL configured"
    fi
}

# Configure git proxy
configure_git_proxy() {
    print_info "Configuring git proxy settings..."
    
    if check_proxy_config; then
        git config --global http.proxy "$HTTP_PROXY"
        git config --global https.proxy "$HTTPS_PROXY"
        print_success "git proxy configured"
    else
        print_info "Skipping git proxy configuration - no proxy settings found"
    fi
    
    # Configure git user if specified
    if [ -n "$GIT_USER_NAME" ]; then
        git config --global user.name "$GIT_USER_NAME"
        print_success "git user name configured"
    fi
    
    if [ -n "$GIT_USER_EMAIL" ]; then
        git config --global user.email "$GIT_USER_EMAIL"
        print_success "git user email configured"
    fi
}

# Configure system-wide proxy
configure_system_proxy() {
    print_info "Configuring system-wide proxy settings..."
    
    if check_proxy_config; then
        # Add proxy settings to bashrc
        cat >> ~/.bashrc <<EOF

# Proxy settings
export HTTP_PROXY="$HTTP_PROXY"
export HTTPS_PROXY="$HTTPS_PROXY"
export FTP_PROXY="$FTP_PROXY"
export NO_PROXY="$NO_PROXY"
export http_proxy="$HTTP_PROXY"
export https_proxy="$HTTPS_PROXY"
export ftp_proxy="$FTP_PROXY"
export no_proxy="$NO_PROXY"
EOF
        
        # Add proxy settings to profile
        sudo tee /etc/profile.d/proxy.sh > /dev/null <<EOF
export HTTP_PROXY="$HTTP_PROXY"
export HTTPS_PROXY="$HTTPS_PROXY"
export FTP_PROXY="$FTP_PROXY"
export NO_PROXY="$NO_PROXY"
export http_proxy="$HTTP_PROXY"
export https_proxy="$HTTPS_PROXY"  
export ftp_proxy="$FTP_PROXY"
export no_proxy="$NO_PROXY"
EOF
        
        print_success "System proxy configured"
    else
        print_info "Skipping system proxy configuration - no proxy settings found"
    fi
}

# Configure curl proxy
configure_curl_proxy() {
    print_info "Configuring curl proxy settings..."
    
    if check_proxy_config; then
        mkdir -p ~/.curlrc
        cat > ~/.curlrc <<EOF
proxy = $HTTP_PROXY
EOF
        print_success "curl proxy configured"
    else
        print_info "Skipping curl proxy configuration - no proxy settings found"
    fi
}

# Configure SSL/TLS settings
configure_ssl() {
    print_info "Configuring SSL/TLS settings..."
    
    if [ -n "$CUSTOM_CA_BUNDLE" ] && [ -f "$CUSTOM_CA_BUNDLE" ]; then
        export REQUESTS_CA_BUNDLE="$CUSTOM_CA_BUNDLE"
        export CURL_CA_BUNDLE="$CUSTOM_CA_BUNDLE"
        print_success "Custom CA bundle configured"
    fi
    
    if [ "$PYTHONHTTPSVERIFY" = "0" ]; then
        print_warning "SSL verification disabled for Python (not recommended for production)"
    fi
}

# Main function
main() {
    local tool=${1:-"all"}
    
    print_info "Starting proxy configuration for: $tool"
    
    case $tool in
        "apt")
            configure_apt_proxy
            ;;
        "pip")
            configure_pip_proxy
            ;;
        "git")
            configure_git_proxy
            ;;
        "system")
            configure_system_proxy
            configure_curl_proxy
            configure_ssl
            ;;
        "all")
            configure_system_proxy
            configure_apt_proxy
            configure_pip_proxy
            configure_git_proxy
            configure_curl_proxy
            configure_ssl
            ;;
        *)
            print_error "Unknown tool: $tool"
            echo "Usage: $0 [apt|pip|git|system|all]"
            exit 1
            ;;
    esac
    
    print_success "Proxy configuration completed for: $tool"
}

# Run main function with all arguments
main "$@"
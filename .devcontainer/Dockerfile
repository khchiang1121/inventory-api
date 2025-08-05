# Use Python 3.10 as base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# # Create developer user
# RUN groupadd --gid 1000 developer \
#     && useradd --uid 1000 --gid developer --shell /bin/bash --create-home developer

RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true

# setup apt sources to use the local mirror
# Uncomment the following lines to use a local mirror (e.g., Aliyun) for faster package downloads
# Remove the current sources.list and replace it with the mirror sources


# RUN rm -f /etc/apt/sources.list.d/*.list && \
#     && echo "" > /etc/apt/sources.list

# RUN echo "deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
#     echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
#     echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
#     echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Basic utilities
    curl \
    wget \
    git \
    vim \
    unzip \
    sudo \
    # Build dependencies
    build-essential \
    gcc \
    g++ \
    make \
    # PostgreSQL client
    postgresql-client \
    libpq-dev \
    # Network utilities
    net-tools \
    iputils-ping \
    netcat-openbsd \
    # Process utilities
    htop \
    procps \
    # SSL certificates
    ca-certificates \
    # Python and pip
    python3 \
    python3-pip \
    python3-venv \
    # Additional tools
    jq \
    tree \
    # For development
    python3-dev \
    python3-setuptools \
    python3-wheel \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add vscode to sudoers
# RUN echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set working directory
WORKDIR /workspace/invenroty-api

# # Copy proxy configuration script
# COPY proxy-config.sh /usr/local/bin/proxy-config.sh
# RUN chmod +x /usr/local/bin/proxy-config.sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
# RUN /usr/local/bin/proxy-config.sh pip

# Setup pip index URL if needed
# ARG PIP_INDEX_URL
# RUN if [ -n "$PIP_INDEX_URL" ]; then \
#         echo "[global]" > /etc/pip.conf && \
#         echo "trusted-host = $PIP_INDEX_URL" >> /etc/pip.conf && \
#         echo "index-url = $PIP_INDEX_URL" >> /etc/pip.conf && \
#         echo "index = $PIP_INDEX_URL" >> /etc/pip.conf
#     fi

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# # Install additional development tools
# RUN /usr/local/bin/proxy-config.sh pip

# # Create directories for logs and media
# RUN mkdir -p /workspace/logs /workspace/media /workspace/static && \
#     chown -R developer:developer /workspace

# Switch to developer user
USER vscode

# Set up Python environment
ENV PATH="/home/vscode/.local/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8201

# ENTRYPOINT ["../entrypoint.sh"]

CMD ["uvicorn", "virtflow.asgi:application", "--host", "0.0.0.0", "--port", "8201"]

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true

#===================================================================================================
# setup apt sources to use the local mirror
# Uncomment the following lines to use a local mirror (e.g., Aliyun) for faster package downloads
# Remove the current sources.list and replace it with the mirror sources
#===================================================================================================

# 定義 ARG，用於控制是否覆寫 source 以及提供新 sources 內容
ARG OVERWRITE_APT_SOURCE=false
ARG APT_SOURCE_CONTENT=""

# 設定 shell 為 bash 並開啟 errexit + pipefail
SHELL ["/bin/bash", "-c"]

# 條件式執行 sources.list 更新
RUN if [[ "${OVERWRITE_APT_SOURCE}" == "true" ]]; then \
    echo "Overwriting APT source..." && \
    rm -f /etc/apt/sources.list.d/*.list && \
    echo "${APT_SOURCE_CONTENT}" > /etc/apt/sources.list ; \
    else \
    echo "Skipping APT source overwrite."; \
    fi

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Basic utilities
    curl \
    wget \
    git \
    vim \
    sudo \
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
    # Additional tools
    jq \
    tree \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Setup pip index URL if needed
ARG PIP_INDEX_URL
ARG PIP_TRUSTED_HOST
RUN if [ -n "$PIP_INDEX_URL" ]; then \
    echo "[global]" > /etc/pip.conf && \
    echo "trusted-host = $PIP_TRUSTED_HOST" >> /etc/pip.conf && \
    echo "index-url = $PIP_INDEX_URL" >> /etc/pip.conf && \
    echo "index = $PIP_INDEX_URL" >> /etc/pip.conf; \
    fi

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8201

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uvicorn", "inventory_api.asgi:application", "--host", "0.0.0.0", "--port", "8201"]

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

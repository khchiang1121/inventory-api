FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8201

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uvicorn", "inventory_api.asgi:application", "--host", "0.0.0.0", "--port", "8201"]

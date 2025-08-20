# VS Code Dev Container for Inventory API

This directory contains the configuration for a VS Code Dev Container that provides a complete development environment for the Inventory API project.

## Features

- **Python 3.10** development environment
- **Proxy support** for corporate networks
- **Code quality tools**: Black, Flake8, isort, mypy, pylint
- **Testing framework**: pytest with Django support
- **Pre-commit hooks** for automated code formatting
- **pgAdmin4** for database management (external database only)
- **Docker-in-Docker** support
- **Git and GitHub CLI** integration

## Quick Start

1. **Prerequisites**:
   - VS Code with the "Dev Containers" extension installed
   - Docker Desktop running
   - Git repository cloned

2. **Open in Dev Container**:
   - Open the project in VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Select "Dev Containers: Reopen in Container"
   - Wait for the container to build and start

3. **Configure Proxy** (if needed):
   - Edit `.devcontainer/config/proxy.conf`
   - Uncomment and set your proxy settings
   - Rebuild the container

## Configuration Files

### Proxy Configuration

Edit `.devcontainer/config/proxy.conf` to configure proxy settings:

```bash
# Example for corporate proxy
export HTTP_PROXY=http://corporate-proxy.company.com:3128
export HTTPS_PROXY=http://corporate-proxy.company.com:3128
export NO_PROXY=localhost,127.0.0.1,::1,.company.com
```

### Environment Variables

The container uses the following environment variables:

- `PYTHONPATH=/workspace`
- `DJANGO_SETTINGS_MODULE=inventory_api.settings`
- `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` (from proxy.conf)

## Development Workflow

### Running the Application

```bash
# Start Django development server
python manage.py runserver 0.0.0.0:8201

# Or using uvicorn
uvicorn inventory_api.asgi:application --host 0.0.0.0 --port 8201
```

### Database Management

- **pgAdmin4** is available at `http://localhost:5050`
- Default credentials: `admin@inventory.local` / `admin123`
- Configure your external database connection in pgAdmin

### Code Quality

The container includes pre-configured tools:

```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint virtflow/

# Type checking
mypy virtflow/

# Run tests
pytest
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed and will run on every commit:

- Code formatting (Black, isort)
- Linting (Flake8, Pylint)
- Type checking (mypy)
- Security scanning (bandit)

## Ports

- **8201**: Django development server
- **5050**: pgAdmin4 web interface

## Troubleshooting

### Proxy Issues

If you're behind a corporate proxy:

1. Edit `.devcontainer/config/proxy.conf`
2. Set your proxy settings
3. Rebuild the container

### Database Connection

Since the database is not included in the container:

1. Ensure your external database is accessible
2. Update the `.env` file with correct database credentials
3. Configure the connection in pgAdmin4

### Permission Issues

If you encounter permission issues:

```bash
# Fix file permissions
sudo chown -R vscode:vscode /workspace
```

## Customization

### Adding Extensions

Edit `.devcontainer/devcontainer.json` and add extensions to the `extensions` array.

### Modifying Dependencies

- Update `requirements.txt` for Python packages
- Modify `.devcontainer/Dockerfile` for system packages
- Update `.devcontainer/setup.sh` for additional setup steps

### Environment Variables

Add environment variables in `.devcontainer/devcontainer.json` under `environmentVariables`.

## Security Notes

- The container runs as a non-root user (`vscode`)
- SSH keys and git config are mounted read-only
- Proxy credentials are stored in the configuration file (consider using environment variables for sensitive data)

## Support

For issues with the dev container setup:

1. Check the VS Code Dev Containers documentation
2. Review the setup logs in the Dev Container output panel
3. Ensure Docker has sufficient resources allocated

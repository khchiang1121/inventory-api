# Changelog

Timeframe: 2025-08-01 → 2025-08-12

## Highlights
- **Project rename and consolidation**: VirtFlow → Inventory API (docs and configs updated)
- **Dev environment**: VS Code devcontainers, Docker, docker-compose, entrypoint, and APT/pip source management
- **Testing**: Introduced pytest, extensive test suite added, and settings refactored
- **Delivery**: GitLab CI/CD configuration and Helm chart for Kubernetes deployments
- **Platform**: Health check endpoint added; production deployment URL updated

## Detailed changes

### 2025-08-12
- **Refactor**: Rename project from VirtFlow to Inventory API and update related documentation
  - Updated: `.devcontainer/devcontainer.json`, `README.md`
  - Added: `.vscode/launch.json`

### 2025-08-11
- **Feat/Tests**: Introduce pytest config and improve test support
  - Added: `pytest.ini`, multiple tests under `virtflow/api/tests/**`
  - Changed: `virtflow/api/v1/serializers.py`, `virtflow/api/v1/views.py`, `virtflow/settings.py`
- **Chore**: Streamline devcontainer initialization and exposed ports
  - Changed: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`
- **Chore**: Add additional APT sources in devcontainer docker-compose
  - Changed: `.devcontainer/docker-compose.yml`
- **Fix**: Correct env var key in devcontainer compose (APT_SOURCE_CONTENT)
  - Changed: `.devcontainer/docker-compose.yml`

### 2025-08-09
- **Dev**: Container and compose tweaks; entrypoint improvements
  - Changed: `.devcontainer/*`, `docker-compose.yml`, `README.md`, `entrypoint.sh`
- **Data tooling**: Adjust fake data generation command
  - Changed: `virtflow/api/management/commands/generate_fake_data.py`

### 2025-08-06
- **Dev**: Improve Docker configuration for development (APT source management, pip index)
  - Changed: `.devcontainer/Dockerfile`, `.devcontainer/docker-compose.yml`
- **Dev**: Add and refine devcontainer and entrypoint
  - Added: `entrypoint.sh`
  - Changed: `.devcontainer/*`, `Dockerfile`, `docker-compose.yml`

### 2025-08-05
- **Feat**: Initial setup for Inventory API development environment with Docker and PostgreSQL
  - Added: `.devcontainer/` (Dockerfile, compose, env template, init DB SQL, proxy config, setup)

### 2025-08-01
- **Feat**: Health check endpoint for system status monitoring
  - Changed: `virtflow/urls.py`
- **Delivery**: Introduce GitLab CI/CD and Helm deployment scripts
  - Added: `.gitlab-ci.yml`, `helm/deploy.sh`, `helm/virtflow-api/**`
- **Delivery/Refactor**: Migrate Helm chart to `helm/inventory-api/**` and update production URL
  - Renamed/Added: `helm/inventory-api/**`
- **Docs**: Extensive API and design documentation added and reorganized under `docs/**`

## Stats (since 2025-08-01)
- 78 files changed, 5,947 insertions, 812 deletions
- Key areas: `.devcontainer/**`, `helm/inventory-api/**`, `virtflow/api/tests/**`, `virtflow/api/v1/{serializers,views}.py`, `virtflow/settings.py`, `virtflow/urls.py`, CI/CD and entrypoint scripts

## Contributors
- khchiang1121

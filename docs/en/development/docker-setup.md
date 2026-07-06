# Docker Setup for AetherOS

## Overview

This guide provides comprehensive instructions for setting up and using Docker with AetherOS. The Docker configuration includes development and production environments, testing setup, and CI/CD integration.

## Prerequisites

Before using Docker with AetherOS, ensure you have the following installed:

- Docker Engine (v24.0+ recommended)
- Docker Compose (v2.20+ recommended)
- Git
- At least 8GB RAM (16GB recommended for full development setup)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/aetheros/aetheros.git
cd aetheros
```

### 2. Build Development Image

```bash
docker build -t aetheros-dev -f Dockerfile.dev .
```

### 3. Start Development Environment

```bash
docker compose up -d
```

This will start:
- AetherOS application (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Qdrant vector database (port 6333)
- Adminer database UI (port 8080)

### 4. Access Services

- **AetherOS**: http://localhost:8000
- **Adminer (DB UI)**: http://localhost:8080
- **PostgreSQL**: localhost:5432 (user: aetheros, password: aetheros)
- **Redis**: localhost:6379
- **Qdrant**: localhost:6333

## Development Workflow

### Building the Development Image

The development Dockerfile includes:
- Python 3.14
- Poetry for dependency management
- All development dependencies
- Development tools (pre-commit, ruff, mypy, etc.)

```bash
# Build with cache
docker build --cache-from aetheros-dev -t aetheros-dev -f Dockerfile.dev .

# Build without cache
docker build --no-cache -t aetheros-dev -f Dockerfile.dev .
```

### Running the Development Container

```bash
# Start in detached mode
docker compose up -d

# Start with logs
docker compose up

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Interactive Development

```bash
# Access bash shell in running container
docker compose exec aetheros-app bash

# Run tests
docker compose exec aetheros-app pytest tests/

# Run specific test
docker compose exec aetheros-app pytest tests/kernel/ -v

# Run linter
docker compose exec aetheros-app ruff check .

# Run type checker
docker compose exec aetheros-app mypy .
```

## Production Deployment

### Building Production Image

The production Dockerfile is optimized for:
- Minimal image size
- Security best practices
- Non-root user execution
- Only runtime dependencies

```bash
# Build production image
docker build -t aetheros-prod -f Dockerfile.prod .

# Run production container
docker run -d \
  --name aetheros-prod \
  -p 8000:8000 \
  -e AETHEROS_ENV=production \
  aetheros-prod
```

### Production Configuration

Environment variables for production:

```bash
# Minimum required environment variables
export AETHEROS_ENV=production
export SECRET_KEY=your-strong-secret-key
export JWT_SECRET=your-strong-jwt-secret

export POSTGRES_HOST=your-postgres-host
export POSTGRES_PORT=5432
export POSTGRES_DB=aetheros
export POSTGRES_USER=aetheros
export POSTGRES_PASSWORD=your-strong-password

export REDIS_HOST=your-redis-host
export REDIS_PORT=6379

export QDRANT_HOST=your-qdrant-host
export QDRANT_PORT=6333
```

## Testing with Docker

### Running Tests in Isolated Environment

```bash
# Start test services
docker compose -f docker-compose.test.yml up -d

# Run tests
docker compose -f docker-compose.test.yml run test-runner

# Run specific test file
docker compose -f docker-compose.test.yml run test-runner pytest tests/kernel/test_execution.py -v

# Stop test services
docker compose -f docker-compose.test.yml down -v
```

### Test Configuration

The test environment includes:
- Isolated PostgreSQL database
- Isolated Redis instance
- Isolated Qdrant instance
- All test dependencies
- Test-specific environment variables

## Configuration Files

### Environment Variables

Copy the template and customize:

```bash
cp config/docker/.env.template .env
# Edit .env with your configuration
```

### Docker Configuration

The `config/docker/docker-config.yml` file contains centralized configuration for all Docker deployments.

## Customizing Services

### PostgreSQL

Customize PostgreSQL configuration by modifying `docker-compose.yml`:

```yaml
services:
  postgres:
    environment:
      POSTGRES_DB: your_db_name
      POSTGRES_USER: your_username
      POSTGRES_PASSWORD: your_strong_password
    volumes:
      - ./custom-postgres.conf:/etc/postgresql/postgresql.conf
```

### Redis

Configure Redis persistence and memory limits:

```yaml
services:
  redis:
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

### Qdrant

Configure Qdrant storage and performance:

```yaml
services:
  qdrant:
    environment:
      QDRANT__STORAGE__SNAPSHOT_INTERVAL: "60"
      QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS: "8"
```

## Networking

All services communicate through a dedicated Docker network `aetheros-network`:

- **AetherOS**: `aetheros-app`
- **PostgreSQL**: `postgres` (port 5432)
- **Redis**: `redis` (port 6379)
- **Qdrant**: `qdrant` (port 6333)

## Volumes and Data Persistence

### Volume Configuration

```yaml
volumes:
  postgres_data: # PostgreSQL data
  redis_data:    # Redis data
  qdrant_data:   # Qdrant data
  aetheros_cache: # Python cache
  aetheros_data: # Application data
```

### Managing Volumes

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect aetheros-postgres-data

# Remove specific volume
docker volume rm aetheros-postgres-data

# Remove all unused volumes
docker volume prune
```

## Security Best Practices

### Development Security

1. **Never commit secrets**: Use `.env` files and add to `.gitignore`
2. **Use strong passwords**: Change default passwords in production
3. **Limit exposed ports**: Only expose necessary ports
4. **Regular updates**: Keep base images updated

### Production Security

1. **Use production Dockerfile**: Optimized for security
2. **Non-root user**: Container runs as non-root user
3. **Resource limits**: Set CPU and memory limits
4. **Read-only filesystem**: Where possible
5. **Secret management**: Use Docker secrets or vault
6. **Network policies**: Restrict container communication

## Troubleshooting

### Common Issues

**Issue: Port already in use**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Issue: Database connection failed**
```bash
# Check container logs
docker compose logs postgres

# Test connection
docker compose exec postgres psql -U aetheros -d aetheros
```

**Issue: Dependency installation failed**
```bash
# Clean and rebuild
docker compose down -v
docker system prune -a
docker compose build --no-cache
```

### Debugging Commands

```bash
# View container logs
docker compose logs -f

# View specific service logs
docker compose logs -f aetheros-app

# Inspect running container
docker inspect aetheros-app

# Check resource usage
docker stats

# Access database directly
docker compose exec postgres psql -U aetheros -d aetheros
```

## CI/CD Integration

The GitHub Actions workflow (`docker-build-test.yml`) automates:
- Docker image building
- Security scanning
- Test execution
- Image pushing to registries

### Manual CI/CD Execution

```bash
# Run specific workflow
gh workflow run docker-build-test.yml

# View workflow status
gh run list

# View workflow logs
gh run view <RUN_ID>
```

## Performance Optimization

### Development Performance

1. **Use build cache**: Faster rebuilds
2. **Volume mounts**: Live code reloading
3. **Resource limits**: Prevent OOM kills
4. **Selective testing**: Run only relevant tests

### Production Performance

1. **Multi-stage builds**: Smaller images
2. **Alpine base images**: Minimal footprint
3. **Layer caching**: Faster deployments
4. **Resource constraints**: Prevent resource exhaustion

## Upgrading Dependencies

```bash
# Update Python dependencies
docker compose exec aetheros-app poetry update

# Update Docker images
docker compose pull

# Rebuild with updated dependencies
docker compose build --no-cache
```

## Advanced Usage

### Custom Docker Networks

```bash
# Create custom network
docker network create --driver bridge --subnet 172.28.0.0/16 --gateway 172.28.0.1 aetheros-custom

# Use custom network in compose
networks:
  default:
    external:
      name: aetheros-custom
```

### Docker Compose Profiles

```yaml
services:
  monitoring:
    image: prom/prometheus
    profiles: ["monitoring"]

# Start with profile
docker compose --profile monitoring up -d
```

### Multi-architecture Builds

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 -t aetheros-prod --push .
```

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AETHEROS_ENV` | `development` | Environment mode |
| `AETHEROS_PORT` | `8000` | Application port |
| `AETHEROS_HOST` | `0.0.0.0` | Bind address |
| `AETHEROS_WORKERS` | `4` | Worker processes |
| `AETHEROS_LOG_LEVEL` | `info` | Log level |
| `POSTGRES_HOST` | `postgres` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| `aetheros-app` | 8000 | Main application |
| `postgres` | 5432 | PostgreSQL database |
| `redis` | 6379 | Redis cache |
| `qdrant` | 6333 | Vector database |
| `adminer` | 8080 | Database UI |

## Migration from Other Setups

### From Local Development

1. Export your local database
2. Update connection strings in `.env`
3. Start Docker services
4. Import data into Docker database

### From Other Container Systems

1. Update `docker-compose.yml` with your service configurations
2. Map existing volumes to new volume names
3. Update environment variables
4. Test migration in staging environment

## Contributing to Docker Configuration

### Adding New Services

1. Add service to `docker-compose.yml`
2. Update `.dockerignore` if needed
3. Add environment variables to `.env.template`
4. Update documentation
5. Add tests for new service integration

### Updating Base Images

1. Test with new image version locally
2. Update image tags in compose files
3. Test full build and deployment
4. Update documentation with version notes

## Support and Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **AetherOS Issues**: https://github.com/aetheros/aetheros/issues
- **AetherOS Discussions**: https://github.com/aetheros/aetheros/discussions

## License

The Docker configuration and related files are licensed under the same license as AetherOS. See the [LICENSE](../LICENSE) file for details.
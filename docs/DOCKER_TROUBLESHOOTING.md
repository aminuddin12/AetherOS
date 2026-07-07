# AetherOS Docker Troubleshooting Guide

This guide provides comprehensive troubleshooting for AetherOS Docker setup and common issues.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Service-Specific Troubleshooting](#service-specific-troubleshooting)
- [Networking Issues](#networking-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)
- [Log Analysis](#log-analysis)
- [Recovery Procedures](#recovery-procedures)

## Prerequisites

### Docker Requirements

- **Docker Engine**: Version 24.0+ recommended
- **Docker Compose**: Version 2.0+ required
- **Minimum Resources**:
  - 4GB RAM (8GB recommended)
  - 2 CPU cores
  - 10GB disk space

### Verify Docker Installation

```bash
# Check Docker version
docker --version
docker compose version

# Check Docker is running
docker info

# Check available resources
docker system df
```

## Common Issues and Solutions

### Issue: `docker compose up` fails with network errors

**Symptoms:**
- Services fail to start with network timeout errors
- Containers get stuck in "starting" state
- Network-related error messages

**Solutions:**

1. **Reset Docker network:**
   ```bash
   docker network prune
   docker system prune
   ```

2. **Restart Docker daemon:**
   ```bash
   # On Linux
   sudo systemctl restart docker
   
   # On macOS
   # Restart Docker Desktop
   ```

3. **Check port conflicts:**
   ```bash
   # Check which ports are in use
   lsof -i :5432  # PostgreSQL
   lsof -i :6379  # Redis
   lsof -i :6333  # Qdrant
   lsof -i :8000  # AetherOS
   lsof -i :8080  # Adminer
   ```

4. **Increase Docker resources:**
   - Open Docker Desktop settings
   - Increase memory allocation to at least 4GB
   - Increase CPU allocation to at least 2 cores

### Issue: Services fail health checks

**Symptoms:**
- Containers show "unhealthy" status
- Health check timeouts
- Services restart repeatedly

**Solutions:**

1. **Check individual service logs:**
   ```bash
   docker logs aetheros-postgres
   docker logs aetheros-redis
   docker logs aetheros-qdrant
   docker logs aetheros-app
   ```

2. **Increase health check timeouts:**
   - Edit `docker-compose.yml`
   - Increase `interval`, `timeout`, and `retries` values

3. **Manual health verification:**
   ```bash
   # Test PostgreSQL
   psql -h localhost -U aetheros -d aetheros -c "SELECT 1"
   
   # Test Redis
   redis-cli -h localhost ping
   
   # Test Qdrant
   curl http://localhost:6333/readyz
   ```

### Issue: Dependency failures

**Symptoms:**
- Services fail because dependencies aren't ready
- "depends_on" conditions not met
- Circular dependency warnings

**Solutions:**

1. **Start dependencies manually first:**
   ```bash
   docker compose up -d postgres redis qdrant
   # Wait for services to be healthy
   docker compose up -d aetheros adminer
   ```

2. **Add custom health check scripts:**
   - Create custom scripts that wait for dependencies
   - Use `wait-for-it.sh` or similar tools

3. **Increase dependency timeout:**
   ```yaml
   depends_on:
     postgres:
       condition: service_healthy
       # Add custom wait script
   ```

## Service-Specific Troubleshooting

### PostgreSQL Issues

**Common Problems:**
- Database initialization failures
- Authentication errors
- Connection limits reached

**Debugging:**

```bash
# Check PostgreSQL logs
docker logs aetheros-postgres

# Connect to database
docker exec -it aetheros-postgres psql -U aetheros -d aetheros

# Check connections
docker exec -it aetheros-postgres psql -U aetheros -c "SELECT * FROM pg_stat_activity;"

# Check database size
docker exec -it aetheros-postgres psql -U aetheros -c "SELECT pg_size_pretty(pg_database_size('aetheros'));"
```

**Solutions:**

1. **Reset database (caution: data loss):**
   ```bash
   docker compose down -v
   docker compose up -d postgres
   ```

2. **Increase connection limits:**
   - Edit `postgresql.conf` in container
   - Add to `docker-compose.yml`:
     ```yaml
     command: postgres -c max_connections=200
     ```

### Redis Issues

**Common Problems:**
- Memory limits exceeded
- Persistence issues
- Connection refused

**Debugging:**

```bash
# Check Redis logs
docker logs aetheros-redis

# Connect to Redis
docker exec -it aetheros-redis redis-cli

# Check memory usage
docker exec -it aetheros-redis redis-cli INFO memory

# Check clients
docker exec -it aetheros-redis redis-cli CLIENT LIST
```

**Solutions:**

1. **Increase memory limit:**
   ```yaml
   command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
   ```

2. **Disable persistence for development:**
   ```yaml
   command: redis-server --appendonly no
   ```

### Qdrant Issues

**Common Problems:**
- Vector database initialization failures
- Port conflicts
- Memory pressure

**Debugging:**

```bash
# Check Qdrant logs
docker logs aetheros-qdrant

# Check Qdrant health
curl http://localhost:6333/readyz

# Get Qdrant metrics
curl http://localhost:6333/metrics

# Check collections
curl http://localhost:6333/collections
```

**Solutions:**

1. **Reset Qdrant storage:**
   ```bash
   docker compose down -v
   docker compose up -d qdrant
   ```

2. **Increase resources:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 2G
   ```

### AetherOS Application Issues

**Common Problems:**
- Application crashes on startup
- Configuration errors
- Dependency resolution failures

**Debugging:**

```bash
# Check application logs
docker logs aetheros-app

# Get interactive shell
docker exec -it aetheros-app bash

# Check Python environment
docker exec -it aetheros-app python --version
docker exec -it aetheros-app pip list

# Check installed packages
docker exec -it aetheros-app pip show aether-cli
```

**Solutions:**

1. **Rebuild application:**
   ```bash
   docker compose build --no-cache aetheros
   docker compose up -d aetheros
   ```

2. **Check environment variables:**
   ```bash
   docker exec -it aetheros-app env
   ```

3. **Install missing dependencies:**
   ```bash
   docker exec -it aetheros-app pip install missing-package
   ```

## Networking Issues

### Issue: Containers can't communicate

**Symptoms:**
- Services can't connect to each other
- Connection refused errors between containers
- DNS resolution failures

**Debugging:**

```bash
# Check network connectivity
docker network inspect aetheros-network

# Test DNS resolution from container
docker exec -it aetheros-app ping postgres

# Test port connectivity
docker exec -it aetheros-app telnet postgres 5432

# Check container IPs
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' aetheros-postgres
```

**Solutions:**

1. **Recreate network:**
   ```bash
   docker network rm aetheros-network
   docker compose up -d
   ```

2. **Use container names for DNS:**
   - Always use service names (e.g., `postgres`, `redis`) not `localhost`

3. **Check firewall rules:**
   ```bash
   # On Linux
   sudo iptables -L -n
   
   # On macOS
   sudo pfctl -sr
   ```

### Issue: Port conflicts on host

**Symptoms:**
- Bind errors when starting containers
- Ports already in use messages

**Debugging:**

```bash
# Check which process is using a port
lsof -i :5432

# Check all listening ports
netstat -tuln
```

**Solutions:**

1. **Change host ports in docker-compose.yml:**
   ```yaml
   ports:
     - "5433:5432"  # Host:Container
   ```

2. **Kill conflicting process:**
   ```bash
   kill -9 $(lsof -t -i :5432)
   ```

## Performance Issues

### Issue: Slow container startup

**Symptoms:**
- Containers take a long time to start
- Health checks timeout during startup

**Solutions:**

1. **Increase health check intervals:**
   ```yaml
   healthcheck:
     interval: 10s
     timeout: 10s
     retries: 10
   ```

2. **Use lighter base images:**
   ```yaml
   image: postgres:16-alpine  # Instead of postgres:16
   ```

3. **Pre-pull images:**
   ```bash
   docker compose pull
   ```

### Issue: High memory usage

**Symptoms:**
- Docker desktop runs out of memory
- Containers get killed due to OOM
- System becomes unresponsive

**Debugging:**

```bash
# Check memory usage
docker stats

# Check system memory
top
free -h
```

**Solutions:**

1. **Increase Docker memory limit:**
   - Docker Desktop → Settings → Resources
   - Increase to at least 4GB

2. **Limit container memory:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G
   ```

3. **Clean up unused resources:**
   ```bash
   docker system prune -a
   docker volume prune
   ```

## Debugging Tools

### Built-in Docker Tools

```bash
# View all containers
docker ps -a

# View container logs
docker logs <container>

# Follow logs in real-time
docker logs -f <container>

# View container processes
docker top <container>

# View container resource usage
docker stats

# Inspect container details
docker inspect <container>

# Execute command in running container
docker exec -it <container> <command>
```

### AetherOS Specific Tools

```bash
# Run health checks
python tools/docker/test_docker_health.py

# Run full test suite
python tools/docker/docker_test_suite.py

# Check service dependencies
python tools/docker/docker_test_suite.py DockerDependencyTest
```

## Log Analysis

### PostgreSQL Logs

```bash
# View PostgreSQL logs
docker logs aetheros-postgres

# Common log patterns to look for:
# - "FATAL: database does not exist"
# - "FATAL: password authentication failed"
# - "LOG: database system was shut down"
# - "PANIC: could not write to file"
```

### Redis Logs

```bash
# View Redis logs
docker logs aetheros-redis

# Common log patterns:
# - "Ready to accept connections"
# - "OOM command not allowed when used memory"
# - "Background saving started"
```

### Qdrant Logs

```bash
# View Qdrant logs
docker logs aetheros-qdrant

# Common log patterns:
# - "Starting Qdrant"
# - "Storage initialized"
# - "Collection created"
```

### AetherOS Logs

```bash
# View AetherOS logs
docker logs aetheros-app

# Common log patterns:
# - "Starting AetherOS"
# - "Configuration loaded"
# - "Database connection established"
# - "Server listening on"
```

## Recovery Procedures

### Full Reset Procedure

```bash
# Step 1: Stop all containers
docker compose down

# Step 2: Remove all volumes (WARNING: data loss)
docker volume prune

# Step 3: Clean system
docker system prune -a

# Step 4: Restart Docker
sudo systemctl restart docker  # Linux
# Restart Docker Desktop      # macOS/Windows

# Step 5: Rebuild and start
docker compose build --no-cache
docker compose up -d
```

### Partial Recovery

**PostgreSQL only:**
```bash
docker compose stop postgres
docker volume rm aetheros-postgres-data
docker compose up -d postgres
```

**Redis only:**
```bash
docker compose stop redis
docker volume rm aetheros-redis-data
docker compose up -d redis
```

**Qdrant only:**
```bash
docker compose stop qdrant
docker volume rm aetheros-qdrant-data
docker compose up -d qdrant
```

### Backup and Restore

**Backup procedure:**
```bash
# Backup PostgreSQL
docker exec -it aetheros-postgres pg_dump -U aetheros -d aetheros > postgres_backup.sql

# Backup Redis (if persistence enabled)
docker cp aetheros-redis:/data/redis_backup.tar .

# Backup Qdrant data
docker cp aetheros-qdrant:/qdrant/storage qdrant_backup
```

**Restore procedure:**
```bash
# Restore PostgreSQL
docker exec -i aetheros-postgres psql -U aetheros -d aetheros < postgres_backup.sql

# Restore Redis
docker cp redis_backup.tar aetheros-redis:/data/
docker exec -it aetheros-redis tar -xvf /data/redis_backup.tar -C /

# Restore Qdrant
docker cp qdrant_backup/. aetheros-qdrant:/qdrant/storage/
docker compose restart qdrant
```

## Common Error Messages and Solutions

### "Cannot connect to the Docker daemon"

**Solution:**
```bash
# Start Docker service
sudo systemctl start docker  # Linux
# Start Docker Desktop       # macOS/Windows
```

### "Port is already allocated"

**Solution:**
```bash
# Find and kill process using port
lsof -i :<port>
kill -9 <PID>
```

### "No space left on device"

**Solution:**
```bash
# Clean Docker system
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk space
df -h
```

### "Image not found"

**Solution:**
```bash
# Pull images explicitly
docker compose pull

# Or build locally
docker compose build
```

### "Health check failed"

**Solution:**
```bash
# Increase health check timeouts
# Edit docker-compose.yml healthcheck section

# Or disable temporarily for debugging
healthcheck:
  disable: true
```

## Contact and Support

If you encounter issues not covered in this guide:

1. **Check GitHub Issues**: [AetherOS GitHub](https://github.com/aetheros)
2. **Review Documentation**: [AetherOS Docs](https://aetheros.com/docs)
3. **Community Support**: Join our Discord community
4. **Create Issue**: Provide detailed logs and reproduction steps

When reporting issues, please include:
- Docker version (`docker --version`)
- Docker Compose version (`docker compose version`)
- Operating system and version
- Full error messages and logs
- Steps to reproduce
- Expected vs actual behavior
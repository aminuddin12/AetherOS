# Testing AetherOS with Docker

## Overview

This guide provides comprehensive instructions for running AetherOS tests in Docker containers. The testing setup includes isolated environments, test databases, and CI/CD integration.

## Prerequisites

- Docker Engine (v24.0+)
- Docker Compose (v2.20+)
- Git

## Quick Start

### 1. Start Test Services

```bash
docker compose -f docker-compose.test.yml up -d
```

This starts:
- Test PostgreSQL database
- Test Redis instance
- Test Qdrant instance
- Test runner container

### 2. Run Tests

```bash
docker compose -f docker-compose.test.yml run test-runner
```

### 3. Stop Test Services

```bash
docker compose -f docker-compose.test.yml down -v
```

## Test Environment Structure

### Test Services

```yaml
services:
  test-runner:      # Runs pytest with test configuration
  test-postgres:    # Isolated PostgreSQL for tests
  test-redis:       # Isolated Redis for tests
  test-qdrant:      # Isolated Qdrant for tests
```

### Test Configuration

Environment variables for testing:

```bash
AETHEROS_ENV=test
PYTEST_ADDOPTS=--color=yes -v --tb=short
POSTGRES_HOST=test-postgres
POSTGRES_DB=aetheros_test
REDIS_HOST=test-redis
QDRANT_HOST=test-qdrant
```

## Running Different Test Types

### Unit Tests

```bash
# Run all unit tests
docker compose -f docker-compose.test.yml run test-runner pytest tests/unit/ -v

# Run specific unit test
docker compose -f docker-compose.test.yml run test-runner pytest tests/unit/test_kernel.py::test_execution_context -v
```

### Integration Tests

```bash
# Run all integration tests
docker compose -f docker-compose.test.yml run test-runner pytest tests/integration/ -v

# Run specific integration test
docker compose -f docker-compose.test.yml run test-runner pytest tests/integration/test_workspace.py -v
```

### Contract Tests

```bash
# Run all contract tests
docker compose -f docker-compose.test.yml run test-runner pytest tests/contracts/ -v

# Run specific contract test
docker compose -f docker-compose.test.yml run test-runner pytest tests/contracts/test_execution.py -v
```

### Architecture Tests

```bash
# Run architecture tests
docker compose -f docker-compose.test.yml run test-runner pytest tests/architecture/ -v
```

## Test Configuration Options

### Pytest Options

Common pytest flags:

```bash
# Verbose output
docker compose -f docker-compose.test.yml run test-runner pytest -v

# Show test durations
docker compose -f docker-compose.test.yml run test-runner pytest --durations=10

# Stop on first failure
docker compose -f docker-compose.test.yml run test-runner pytest -x

# Run failed tests first
docker compose -f docker-compose.test.yml run test-runner pytest --failed-first

# Run specific test by name
docker compose -f docker-compose.test.yml run test-runner pytest -k "test_execution"

# Run tests by marker
docker compose -f docker-compose.test.yml run test-runner pytest -m "integration"
```

### Test Coverage

```bash
# Run tests with coverage
docker compose -f docker-compose.test.yml run test-runner pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
docker compose -f docker-compose.test.yml run test-runner pytest --cov=src --cov-report=html:htmlcov

# View coverage report
# The HTML report will be in the htmlcov directory
```

## Test Data Management

### Database Setup

The test PostgreSQL is initialized with:

```sql
CREATE DATABASE aetheros_test;
CREATE USER aetheros WITH PASSWORD 'aetheros';
GRANT ALL PRIVILEGES ON DATABASE aetheros_test TO aetheros;
```

### Test Data Cleanup

```bash
# Clean test database between runs
docker compose -f docker-compose.test.yml down -v

# This removes all test data and starts fresh
```

## Debugging Tests

### View Test Logs

```bash
# View test runner logs
docker compose -f docker-compose.test.yml logs test-runner

# Follow logs in real-time
docker compose -f docker-compose.test.yml logs -f test-runner
```

### Interactive Debugging

```bash
# Access test container shell
docker compose -f docker-compose.test.yml run test-runner bash

# Then run tests manually
pytest tests/ -v
```

### Test Database Access

```bash
# Access test PostgreSQL
docker compose -f docker-compose.test.yml exec test-postgres psql -U aetheros -d aetheros_test

# Run SQL queries
SELECT * FROM information_schema.tables;
```

## Test Performance Optimization

### Selective Testing

```bash
# Run tests in specific directory
docker compose -f docker-compose.test.yml run test-runner pytest tests/kernel/ -v

# Run tests matching pattern
docker compose -f docker-compose.test.yml run test-runner pytest -k "execution" -v

# Skip slow tests
docker compose -f docker-compose.test.yml run test-runner pytest -m "not slow" -v
```

### Parallel Testing

```bash
# Run tests in parallel (requires pytest-xdist)
docker compose -f docker-compose.test.yml run test-runner pytest -n 4 -v

# Auto-detect CPU cores
docker compose -f docker-compose.test.yml run test-runner pytest -n auto -v
```

## CI/CD Testing

### GitHub Actions Workflow

The workflow includes:

1. **Build**: Development and production Docker images
2. **Security Scan**: Trivy vulnerability scanning
3. **Test Execution**: Run full test suite
4. **Push Images**: Push to container registries

### Local CI/CD Simulation

```bash
# Build images
docker build -t aetheros-dev -f Dockerfile.dev .
docker build -t aetheros-prod -f Dockerfile.prod .

# Run security scan
docker scan aetheros-dev

# Run tests
docker compose -f docker-compose.test.yml up -d
docker compose -f docker-compose.test.yml run test-runner
docker compose -f docker-compose.test.yml down -v
```

## Test Environment Customization

### Custom Test Configuration

Modify `docker-compose.test.yml`:

```yaml
services:
  test-runner:
    environment:
      PYTEST_ADDOPTS: "--color=yes -v --tb=short -m 'not slow'"
      AETHEROS_LOG_LEVEL: "debug"
```

### Adding Test Dependencies

Update `Dockerfile.dev` to include additional test tools:

```dockerfile
RUN pip install --no-cache-dir \
    pytest-cov \
    pytest-benchmark \
    pytest-xdist \
    hypothesis
```

## Test Data Generation

### Using Factories

```python
# Example test with factory
from tests.factories import WorkspaceFactory

def test_workspace_creation():
    workspace = WorkspaceFactory.create()
    assert workspace.id is not None
```

### Using Fixtures

```python
# Example pytest fixture
import pytest
from aether_workspace.models import Workspace

@pytest.fixture
def workspace():
    return Workspace(name="test-workspace", owner="test-user")

def test_workspace_properties(workspace):
    assert workspace.name == "test-workspace"
```

## Test Isolation Strategies

### Database Isolation

```python
# Use transactions for test isolation
@pytest.fixture(scope="function")
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()
```

### Temporary Directories

```python
# Use temp directories for file tests
import tempfile
import pytest

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
```

## Test Reporting

### JUnit XML Reports

```bash
# Generate JUnit XML reports
docker compose -f docker-compose.test.yml run test-runner pytest --junitxml=test-results.xml

# Reports will be in test-results.xml
```

### HTML Reports

```bash
# Generate HTML reports
docker compose -f docker-compose.test.yml run test-runner pytest --html=report.html

# View report in browser
```

## Test Maintenance

### Updating Test Dependencies

```bash
# Update pytest and plugins
docker compose -f docker-compose.test.yml run test-runner pip install --upgrade pytest pytest-cov pytest-asyncio
```

### Adding New Test Types

1. Create new test directory (e.g., `tests/performance/`)
2. Add test configuration to `docker-compose.test.yml`
3. Update CI/CD workflow
4. Add documentation

## Troubleshooting Tests

### Common Test Issues

**Issue: Database connection failed**
```bash
# Check test database logs
docker compose -f docker-compose.test.yml logs test-postgres

# Test connection manually
docker compose -f docker-compose.test.yml exec test-postgres psql -U aetheros -d aetheros_test
```

**Issue: Tests hanging**
```bash
# Check for deadlocks or timeouts
# Increase timeout in test configuration
```

**Issue: Test data pollution**
```bash
# Clean test database
docker compose -f docker-compose.test.yml down -v
docker compose -f docker-compose.test.yml up -d
```

### Debugging Test Failures

```bash
# Run failed test with more verbose output
docker compose -f docker-compose.test.yml run test-runner pytest tests/failing_test.py -vv -s

# Use pdb for interactive debugging
docker compose -f docker-compose.test.yml run test-runner pytest tests/failing_test.py --pdb
```

## Test Best Practices

### Test Organization

1. **Directory structure**: Organize tests by module/functionality
2. **Naming conventions**: Use `test_` prefix for test files and functions
3. **Test isolation**: Each test should be independent
4. **Test data**: Use factories or fixtures for test data

### Test Performance

1. **Selective testing**: Run only relevant tests during development
2. **Parallel execution**: Use pytest-xdist for parallel test runs
3. **Test marking**: Mark slow tests to skip during quick runs
4. **Test caching**: Use pytest caching for faster re-runs

### Test Reliability

1. **Deterministic tests**: Avoid randomness or use seeds
2. **Timeout handling**: Set reasonable timeouts for slow operations
3. **Resource cleanup**: Ensure resources are properly cleaned up
4. **Test retries**: Use pytest-rerunfailures for flaky tests

## Advanced Testing Techniques

### Property-Based Testing

```python
# Example using hypothesis
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(), st.integers())
def test_string_concatenation(text, number):
    result = text + str(number)
    assert isinstance(result, str)
```

### Benchmark Testing

```bash
# Run benchmark tests
docker compose -f docker-compose.test.yml run test-runner pytest --benchmark-autosave=true

# Compare benchmark results
docker compose -f docker-compose.test.yml run test-runner pytest --benchmark-compare
```

### Integration Testing

```python
# Example integration test
import pytest
from aether_workspace.service import WorkspaceService
from aether_storage.service import StorageService

@pytest.mark.integration
class TestWorkspaceStorageIntegration:
    def test_workspace_storage_integration(self):
        workspace_service = WorkspaceService()
        storage_service = StorageService()
        
        # Test integration between services
        workspace = workspace_service.create("test")
        storage = storage_service.create(workspace.id, "test-file")
        
        assert storage.workspace_id == workspace.id
```

## Test Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AETHEROS_ENV` | `test` | Test environment |
| `PYTEST_ADDOPTS` | `--color=yes -v` | Pytest options |
| `POSTGRES_HOST` | `test-postgres` | Test DB host |
| `POSTGRES_DB` | `aetheros_test` | Test DB name |

### Test Service Ports

| Service | Port | Description |
|---------|------|-------------|
| `test-postgres` | 5432 | Test PostgreSQL |
| `test-redis` | 6379 | Test Redis |
| `test-qdrant` | 6333 | Test Qdrant |

## Migration from Other Test Setups

### From Local Testing

1. Update connection strings to use Docker service names
2. Ensure test data is isolated per test run
3. Update CI/CD to use Docker test setup

### From Other CI Systems

1. Convert CI configuration to GitHub Actions format
2. Update test service definitions
3. Ensure test environment variables are properly set

## Contributing to Testing

### Adding New Tests

1. Create test file in appropriate directory
2. Follow existing test patterns
3. Add test to CI/CD workflow if needed
4. Update test documentation

### Improving Test Coverage

1. Identify uncovered code with coverage reports
2. Add tests for missing coverage
3. Ensure edge cases are tested
4. Add integration tests for critical paths

## Support and Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Docker Testing Guide**: https://docs.docker.com/language/python/test/
- **AetherOS Testing Issues**: https://github.com/aetheros/aetheros/issues

## License

The testing configuration and related files are licensed under the same license as AetherOS. See the [LICENSE](../LICENSE) file for details.
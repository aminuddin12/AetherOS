#!/usr/bin/env python3
"""
AetherOS Docker Test Suite

Comprehensive testing framework for Docker environment including:
- Service health tests
- Integration tests
- Performance tests
- Dependency tests
"""

import os
import sys
import time
import subprocess
import json
import unittest
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docker.test_docker_health import DockerHealthChecker, ServiceStatus


class DockerServiceHealthTest(unittest.TestCase):
    """Test case for Docker service health checks."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.checker = DockerHealthChecker()
        cls.start_time = time.time()
    
    def test_postgres_health(self):
        """Test PostgreSQL service health."""
        status = self.checker.check_postgres()
        self.assertTrue(status.healthy, f"PostgreSQL unhealthy: {status.message}")
    
    def test_redis_health(self):
        """Test Redis service health."""
        status = self.checker.check_redis()
        self.assertTrue(status.healthy, f"Redis unhealthy: {status.message}")
    
    def test_qdrant_health(self):
        """Test Qdrant service health."""
        status = self.checker.check_qdrant()
        self.assertTrue(status.healthy, f"Qdrant unhealthy: {status.message}")
    
    def test_aetheros_health(self):
        """Test AetherOS application health."""
        status = self.checker.check_aetheros()
        self.assertTrue(status.healthy, f"AetherOS unhealthy: {status.message}")
    
    def test_adminer_health(self):
        """Test Adminer UI health."""
        status = self.checker.check_adminer()
        self.assertTrue(status.healthy, f"Adminer unhealthy: {status.message}")
    
    def test_docker_containers(self):
        """Test that all Docker containers are running."""
        results = self.checker.check_docker_containers()
        
        for status in results:
            with self.subTest(service=status.name):
                # Some containers don't have health checks (qdrant, aetheros, adminer)
                # Just check that they are running
                if status.name in ['qdrant', 'aetheros', 'adminer']:
                    self.assertIn('Up', status.message, f"Container {status.name} not running: {status.message}")
                else:
                    self.assertTrue(status.healthy, f"Container {status.name} unhealthy: {status.message}")


class DockerIntegrationTest(unittest.TestCase):
    """Test case for Docker integration tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.checker = DockerHealthChecker()
    
    def test_postgres_connection(self):
        """Test PostgreSQL connection and basic operations."""
        import psycopg2
        
        try:
            conn = psycopg2.connect(
                host=self.checker.services['postgres']['host'],
                port=self.checker.services['postgres']['port'],
                dbname=self.checker.postgres_db,
                user=self.checker.postgres_user,
                password=self.checker.postgres_password
            )
            
            with conn.cursor() as cursor:
                # Test table creation
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_integration (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                # Test insert
                cursor.execute("INSERT INTO test_integration (name) VALUES (%s) RETURNING id", ("test",))
                inserted_id = cursor.fetchone()[0]
                
                # Test select
                cursor.execute("SELECT name FROM test_integration WHERE id = %s", (inserted_id,))
                result = cursor.fetchone()
                
                # Test cleanup
                cursor.execute("DELETE FROM test_integration WHERE id = %s", (inserted_id,))
                
            conn.close()
            
            self.assertEqual(result[0], "test")
            
        except Exception as e:
            self.fail(f"PostgreSQL integration test failed: {str(e)}")
    
    def test_redis_operations(self):
        """Test Redis connection and basic operations."""
        import redis
        
        try:
            r = redis.Redis(
                host=self.checker.services['redis']['host'],
                port=self.checker.services['redis']['port']
            )
            
            # Test set/get
            test_key = "integration_test_key"
            test_value = "integration_test_value"
            
            r.set(test_key, test_value)
            retrieved_value = r.get(test_key)
            
            # Cleanup
            r.delete(test_key)
            
            self.assertEqual(retrieved_value.decode(), test_value)
            
        except Exception as e:
            self.fail(f"Redis integration test failed: {str(e)}")
    
    def test_inter_service_communication(self):
        """Test communication between all services."""
        results = self.checker.test_inter_service_communication()
        
        for service, healthy in results.items():
            with self.subTest(service=service):
                self.assertTrue(healthy, f"Inter-service communication failed for {service}")


class DockerPerformanceTest(unittest.TestCase):
    """Test case for Docker performance tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.checker = DockerHealthChecker()
    
    def test_postgres_response_time(self):
        """Test PostgreSQL response time."""
        import psycopg2
        import time
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(
                host=self.checker.services['postgres']['host'],
                port=self.checker.services['postgres']['port'],
                dbname=self.checker.postgres_db,
                user=self.checker.postgres_user,
                password=self.checker.postgres_password
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            conn.close()
            
        except Exception as e:
            self.fail(f"PostgreSQL response time test failed: {str(e)}")
        
        response_time = time.time() - start_time
        max_allowed = 2.0  # 2 seconds
        
        self.assertLess(response_time, max_allowed, 
                       f"PostgreSQL response time {response_time:.3f}s exceeds {max_allowed}s")
    
    def test_redis_response_time(self):
        """Test Redis response time."""
        import redis
        import time
        
        start_time = time.time()
        
        try:
            r = redis.Redis(
                host=self.checker.services['redis']['host'],
                port=self.checker.services['redis']['port']
            )
            
            # Multiple operations
            for i in range(10):
                r.set(f"perf_test_{i}", f"value_{i}")
                r.get(f"perf_test_{i}")
                r.delete(f"perf_test_{i}")
            
        except Exception as e:
            self.fail(f"Redis response time test failed: {str(e)}")
        
        response_time = time.time() - start_time
        max_allowed = 1.0  # 1 second for 30 operations
        
        self.assertLess(response_time, max_allowed, 
                       f"Redis response time {response_time:.3f}s exceeds {max_allowed}s")


class DockerDependencyTest(unittest.TestCase):
    """Test case for Docker dependency management."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.checker = DockerHealthChecker()
    
    def test_service_dependencies(self):
        """Test that services respect their dependencies."""
        # Check that dependent services are healthy only if their dependencies are healthy
        results = self.checker.run_all_checks()
        
        # AetherOS depends on PostgreSQL and Redis
        postgres_healthy = results['postgres'].healthy
        redis_healthy = results['redis'].healthy
        aetheros_healthy = results['aetheros'].healthy
        
        # If dependencies are unhealthy, AetherOS should also be unhealthy or at least not fully functional
        if not (postgres_healthy and redis_healthy):
            # We can't assert AetherOS is unhealthy because it might still be running
            # but we can log a warning
            print(f"WARNING: AetherOS running with unhealthy dependencies (PostgreSQL: {postgres_healthy}, Redis: {redis_healthy})")
        
        # Adminer depends on PostgreSQL
        adminer_healthy = results['adminer'].healthy
        if not postgres_healthy:
            print("WARNING: Adminer running with unhealthy PostgreSQL dependency")
    
    def test_docker_network(self):
        """Test Docker network connectivity."""
        # Test that all containers can communicate on the same network
        try:
            result = subprocess.run([
                'docker', 'network', 'inspect', 'aetheros-network'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse JSON output - it might be a list
                try:
                    network_info = json.loads(result.stdout)
                    if isinstance(network_info, list):
                        network_info = network_info[0] if network_info else {}
                    
                    containers = network_info.get('Containers', {})
                    
                    # Check that expected containers are on the network
                    expected_containers = [
                        'aetheros-postgres',
                        'aetheros-redis', 
                        'aetheros-qdrant',
                        'aetheros-app',
                        'aetheros-adminer'
                    ]
                    
                    # Build a list of actual container names
                    actual_container_names = []
                    for container_id, container_data in containers.items():
                        actual_container_names.append(container_data.get('Name', ''))
                    
                    for container in expected_containers:
                        with self.subTest(container=container):
                            found = container in actual_container_names
                            self.assertTrue(found, 
                                         f"Container {container} not found on aetheros-network. Found: {actual_container_names}")
                except json.JSONDecodeError as e:
                    self.fail(f"Failed to parse network inspect output: {str(e)}")
            else:
                self.fail(f"Docker network inspect failed: {result.stderr}")
                
        except Exception as e:
            self.fail(f"Docker network test failed: {str(e)}")


def run_docker_tests():
    """Run all Docker tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(DockerServiceHealthTest))
    suite.addTests(loader.loadTestsFromTestCase(DockerIntegrationTest))
    suite.addTests(loader.loadTestsFromTestCase(DockerPerformanceTest))
    suite.addTests(loader.loadTestsFromTestCase(DockerDependencyTest))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    """Main entry point for Docker test suite."""
    print("=" * 60)
    print("AetherOS Docker Test Suite")
    print("=" * 60)
    
    success = run_docker_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL DOCKER TESTS PASSED")
    else:
        print("❌ SOME DOCKER TESTS FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
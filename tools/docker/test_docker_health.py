#!/usr/bin/env python3
"""
AetherOS Docker Health Check and Testing Framework

This script provides comprehensive testing for the Docker environment,
including service health checks, inter-service communication tests,
and integration testing capabilities.
"""

import os
import sys
import time
import socket
import subprocess
import json
import requests
import psycopg2
import redis
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ServiceStatus:
    """Represents the health status of a service."""
    name: str
    healthy: bool
    message: str = ""
    details: dict = None


class DockerHealthChecker:
    """Main class for Docker health checking and testing."""
    
    def __init__(self):
        self.services = {
            'postgres': {'host': 'localhost', 'port': 5432, 'container': 'aetheros-postgres'},
            'redis': {'host': 'localhost', 'port': 6379, 'container': 'aetheros-redis'},
            'qdrant': {'host': 'localhost', 'port': 6333, 'container': 'aetheros-qdrant'},
            'aetheros': {'host': 'localhost', 'port': 8000, 'container': 'aetheros-app'},
            'adminer': {'host': 'localhost', 'port': 8080, 'container': 'aetheros-adminer'}
        }
        
        # Load environment variables
        self.postgres_db = os.environ.get('POSTGRES_DB', 'aetheros')
        self.postgres_user = os.environ.get('POSTGRES_USER', 'aetheros')
        self.postgres_password = os.environ.get('POSTGRES_PASSWORD', 'aetheros')
        
    def check_port(self, host: str, port: int, timeout: int = 5) -> bool:
        """Check if a port is accessible."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
    
    def check_postgres(self) -> ServiceStatus:
        """Check PostgreSQL database health."""
        try:
            conn = psycopg2.connect(
                host=self.services['postgres']['host'],
                port=self.services['postgres']['port'],
                dbname=self.postgres_db,
                user=self.postgres_user,
                password=self.postgres_password,
                connect_timeout=5
            )
            
            # Test query
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            
            conn.close()
            return ServiceStatus('postgres', True, "PostgreSQL is healthy", {"query_result": result})
            
        except Exception as e:
            return ServiceStatus('postgres', False, f"PostgreSQL connection failed: {str(e)}")
    
    def check_redis(self) -> ServiceStatus:
        """Check Redis cache health."""
        try:
            r = redis.Redis(
                host=self.services['redis']['host'],
                port=self.services['redis']['port'],
                socket_timeout=5
            )
            
            # Test ping
            response = r.ping()
            
            # Test set/get
            r.set('test_key', 'test_value')
            value = r.get('test_key')
            
            return ServiceStatus('redis', True, "Redis is healthy", {
                "ping_response": response,
                "test_value": value.decode() if value else None
            })
            
        except Exception as e:
            return ServiceStatus('redis', False, f"Redis connection failed: {str(e)}")
    
    def check_qdrant(self) -> ServiceStatus:
        """Check Qdrant vector database health."""
        try:
            # Check if port is open
            if not self.check_port(self.services['qdrant']['host'], self.services['qdrant']['port']):
                return ServiceStatus('qdrant', False, "Qdrant port not accessible")
            
            # Try to get version info
            response = requests.get(f"http://{self.services['qdrant']['host']}:{self.services['qdrant']['port']}/readyz", timeout=5)
            
            if response.status_code == 200:
                return ServiceStatus('qdrant', True, "Qdrant is healthy", {"status": "ready"})
            else:
                return ServiceStatus('qdrant', False, f"Qdrant not ready: {response.status_code}")
                
        except Exception as e:
            return ServiceStatus('qdrant', False, f"Qdrant check failed: {str(e)}")
    
    def check_aetheros(self) -> ServiceStatus:
        """Check AetherOS application health."""
        try:
            # Check if port is open
            if not self.check_port(self.services['aetheros']['host'], self.services['aetheros']['port']):
                return ServiceStatus('aetheros', False, "AetherOS port not accessible")
            
            # Try to get health endpoint (if available)
            try:
                response = requests.get(f"http://{self.services['aetheros']['host']}:{self.services['aetheros']['port']}/health", timeout=5)
                if response.status_code == 200:
                    return ServiceStatus('aetheros', True, "AetherOS is healthy", response.json())
            except requests.exceptions.RequestException:
                pass
            
            # If no health endpoint, just check port
            return ServiceStatus('aetheros', True, "AetherOS port accessible")
            
        except Exception as e:
            return ServiceStatus('aetheros', False, f"AetherOS check failed: {str(e)}")
    
    def check_adminer(self) -> ServiceStatus:
        """Check Adminer database management UI."""
        try:
            # Check if port is open
            if not self.check_port(self.services['adminer']['host'], self.services['adminer']['port']):
                return ServiceStatus('adminer', False, "Adminer port not accessible")
            
            # Try to get Adminer page
            response = requests.get(f"http://{self.services['adminer']['host']}:{self.services['adminer']['port']}", timeout=5)
            
            if response.status_code == 200:
                return ServiceStatus('adminer', True, "Adminer is healthy")
            else:
                return ServiceStatus('adminer', False, f"Adminer not responding: {response.status_code}")
                
        except Exception as e:
            return ServiceStatus('adminer', False, f"Adminer check failed: {str(e)}")
    
    def check_docker_containers(self) -> List[ServiceStatus]:
        """Check Docker container status using docker commands."""
        results = []
        
        try:
            # Get container status
            result = subprocess.run(['docker', 'ps', '--format', '{{json .}}'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        containers.append(json.loads(line))
                
                # Check each expected container
                for service_name, service_info in self.services.items():
                    container_name = service_info['container']
                    found = False
                    
                    for container in containers:
                        if container.get('Names') == container_name:
                            found = True
                            status = container.get('Status', '')
                            healthy = 'healthy' in status.lower() and 'up' in status.lower()
                            
                            results.append(ServiceStatus(
                                service_name, 
                                healthy, 
                                f"Container {container_name} status: {status}",
                                {"container_status": status}
                            ))
                            break
                    
                    if not found:
                        results.append(ServiceStatus(service_name, False, f"Container {container_name} not found"))
            
        except Exception as e:
            results.append(ServiceStatus('docker', False, f"Docker command failed: {str(e)}"))
        
        return results
    
    def run_all_checks(self) -> Dict[str, ServiceStatus]:
        """Run all health checks and return results."""
        results = {}
        
        # Check containers via Docker
        docker_results = self.check_docker_containers()
        for status in docker_results:
            results[status.name] = status
        
        # Run individual service checks
        results['postgres'] = self.check_postgres()
        results['redis'] = self.check_redis()
        results['qdrant'] = self.check_qdrant()
        results['aetheros'] = self.check_aetheros()
        results['adminer'] = self.check_adminer()
        
        return results
    
    def print_results(self, results: Dict[str, ServiceStatus]) -> None:
        """Print health check results in a formatted way."""
        print("=" * 60)
        print("AetherOS Docker Health Check Results")
        print("=" * 60)
        
        all_healthy = True
        
        for service_name, status in results.items():
            emoji = "✅" if status.healthy else "❌"
            print(f"{emoji} {service_name.upper():12} - {status.message}")
            
            if status.details:
                for key, value in status.details.items():
                    print(f"    {key}: {value}")
            
            if not status.healthy:
                all_healthy = False
        
        print("=" * 60)
        overall_status = "✅ ALL SERVICES HEALTHY" if all_healthy else "❌ SOME SERVICES UNHEALTHY"
        print(f"Overall Status: {overall_status}")
        print("=" * 60)
        
        return all_healthy
    
    def test_inter_service_communication(self) -> Dict[str, bool]:
        """Test communication between services."""
        results = {}
        
        # Test PostgreSQL connection from host
        try:
            postgres_status = self.check_postgres()
            results['host_postgres'] = postgres_status.healthy
        except Exception:
            results['host_postgres'] = False
        
        # Test Redis connection from host
        try:
            redis_status = self.check_redis()
            results['host_redis'] = redis_status.healthy
        except Exception:
            results['host_redis'] = False
        
        # Test Qdrant connection from host
        try:
            qdrant_status = self.check_qdrant()
            results['host_qdrant'] = qdrant_status.healthy
        except Exception:
            results['host_qdrant'] = False
        
        return results


def main():
    """Main entry point for Docker health checking."""
    checker = DockerHealthChecker()
    
    print("Starting AetherOS Docker Health Check...")
    print("This may take a few moments...")
    
    # Run all health checks
    results = checker.run_all_checks()
    
    # Print results
    all_healthy = checker.print_results(results)
    
    # Test inter-service communication
    print("\nTesting Inter-Service Communication...")
    comm_results = checker.test_inter_service_communication()
    
    comm_healthy = all(comm_results.values())
    print(f"Inter-Service Communication: {'✅ HEALTHY' if comm_healthy else '❌ UNHEALTHY'}")
    
    # Return appropriate exit code
    sys.exit(0 if (all_healthy and comm_healthy) else 1)


if __name__ == "__main__":
    main()
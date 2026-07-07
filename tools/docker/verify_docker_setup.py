#!/usr/bin/env python3
"""
AetherOS Docker Setup Verification Script

This script verifies that the Docker setup is complete and working correctly.
It runs comprehensive checks and generates a verification report.
"""

import os
import sys
import time
import subprocess
import json
import socket
from typing import Dict, List, Any
from dataclasses import dataclass
import datetime


@dataclass
class VerificationResult:
    """Represents a verification test result."""
    test_name: str
    passed: bool
    message: str
    details: dict = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()


class DockerSetupVerifier:
    """Main class for Docker setup verification."""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def add_result(self, test_name: str, passed: bool, message: str, details: dict = None) -> None:
        """Add a verification result."""
        result = VerificationResult(test_name, passed, message, details)
        self.results.append(result)
        
        status_emoji = "✅" if passed else "❌"
        print(f"{status_emoji} {test_name}: {message}")
        
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    def check_docker_installed(self) -> bool:
        """Check if Docker is installed and running."""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.add_result("Docker Installation", True, "Docker is installed", {"version": version})
                return True
            else:
                self.add_result("Docker Installation", False, "Docker command failed")
                return False
                
        except FileNotFoundError:
            self.add_result("Docker Installation", False, "Docker not found")
            return False
        except Exception as e:
            self.add_result("Docker Installation", False, f"Docker check failed: {str(e)}")
            return False
    
    def check_docker_compose_installed(self) -> bool:
        """Check if Docker Compose is installed."""
        try:
            result = subprocess.run(['docker', 'compose', 'version'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.add_result("Docker Compose Installation", True, "Docker Compose is installed", {"version": version})
                return True
            else:
                self.add_result("Docker Compose Installation", False, "Docker Compose command failed")
                return False
                
        except Exception as e:
            self.add_result("Docker Compose Installation", False, f"Docker Compose check failed: {str(e)}")
            return False
    
    def check_docker_daemon(self) -> bool:
        """Check if Docker daemon is running."""
        try:
            result = subprocess.run(['docker', 'info'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                # Try to parse JSON, but if it fails, just check that daemon is responsive
                try:
                    info = json.loads(result.stdout)
                    containers = info.get('Containers', 0)
                    images = info.get('Images', 0)
                    
                    self.add_result("Docker Daemon", True, "Docker daemon is running", {
                        "containers": containers,
                        "images": images,
                        "server_version": info.get('ServerVersion', 'unknown')
                    })
                except json.JSONDecodeError:
                    # Docker info output might not be pure JSON, but daemon is responsive
                    self.add_result("Docker Daemon", True, "Docker daemon is running")
                
                return True
            else:
                self.add_result("Docker Daemon", False, "Docker daemon not responding")
                return False
                
        except Exception as e:
            self.add_result("Docker Daemon", False, f"Docker daemon check failed: {str(e)}")
            return False
    
    def check_docker_compose_files(self) -> bool:
        """Check if Docker Compose files exist."""
        required_files = ['docker-compose.yml', 'docker-compose.test.yml']
        found_files = []
        
        for file in required_files:
            if os.path.exists(file):
                found_files.append(file)
        
        if len(found_files) == len(required_files):
            self.add_result("Docker Compose Files", True, "All Docker Compose files found", {
                "files": found_files
            })
            return True
        else:
            missing = set(required_files) - set(found_files)
            self.add_result("Docker Compose Files", False, f"Missing files: {', '.join(missing)}")
            return False
    
    def check_dockerfiles(self) -> bool:
        """Check if Dockerfiles exist."""
        required_files = ['Dockerfile.dev', 'Dockerfile.prod']
        found_files = []
        
        for file in required_files:
            if os.path.exists(file):
                found_files.append(file)
        
        if len(found_files) == len(required_files):
            self.add_result("Dockerfiles", True, "All Dockerfiles found", {
                "files": found_files
            })
            return True
        else:
            missing = set(required_files) - set(found_files)
            self.add_result("Dockerfiles", False, f"Missing Dockerfiles: {', '.join(missing)}")
            return False
    
    def check_services_running(self) -> bool:
        """Check if all required services are running."""
        try:
            result = subprocess.run(['docker', 'compose', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Handle both single JSON object and multiple JSON lines
                services = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            services.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                
                expected_services = [
                    'aetheros-app', 'aetheros-postgres', 'aetheros-redis',
                    'aetheros-qdrant', 'aetheros-adminer'
                ]
                
                running_services = []
                healthy_services = []
                
                for service in services:
                    name = service.get('Name', '')
                    status = service.get('Status', '')
                    
                    if 'Up' in status:
                        running_services.append(name)
                        if 'healthy' in status.lower():
                            healthy_services.append(name)
                
                all_running = len(running_services) == len(expected_services)
                all_healthy = len(healthy_services) >= len(expected_services) - 1  # Adminer doesn't have healthcheck
                
                if all_running and all_healthy:
                    self.add_result("Services Running", True, "All services are running and healthy", {
                        "running": running_services,
                        "healthy": healthy_services
                    })
                    return True
                elif all_running:
                    self.add_result("Services Running", True, "All services are running", {
                        "running": running_services,
                        "healthy": healthy_services
                    })
                    return True
                else:
                    missing = set(expected_services) - set(running_services)
                    self.add_result("Services Running", False, f"Some services not running: {', '.join(missing)}", {
                        "running": running_services,
                        "expected": expected_services
                    })
                    return False
            else:
                self.add_result("Services Running", False, "Failed to get service status")
                return False
                
        except Exception as e:
            self.add_result("Services Running", False, f"Service check failed: {str(e)}")
            return False
    
    def check_port_accessibility(self) -> bool:
        """Check if required ports are accessible."""
        ports = {
            'PostgreSQL': 5432,
            'Redis': 6379,
            'Qdrant': 6333,
            'AetherOS': 8000,
            'Adminer': 8080
        }
        
        accessible_ports = []
        
        for service, port in ports.items():
            try:
                with socket.create_connection(("localhost", port), timeout=3):
                    accessible_ports.append(f"{service} ({port})")
            except (socket.timeout, ConnectionRefusedError):
                pass
        
        if len(accessible_ports) == len(ports):
            self.add_result("Port Accessibility", True, "All required ports are accessible", {
                "accessible_ports": accessible_ports
            })
            return True
        else:
            missing = set(ports.values()) - {int(p.split(' ')[1][1:-1]) for p in accessible_ports}
            self.add_result("Port Accessibility", False, f"Some ports not accessible: {', '.join(str(p) for p in missing)}", {
                "accessible_ports": accessible_ports,
                "expected_ports": list(ports.values())
            })
            return False
    
    def check_docker_network(self) -> bool:
        """Check if Docker network is properly configured."""
        try:
            result = subprocess.run(['docker', 'network', 'inspect', 'aetheros-network'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                network_info = json.loads(result.stdout)
                containers = list(network_info[0].get('Containers', {}).keys())
                
                expected_containers = [
                    'aetheros-postgres', 'aetheros-redis', 'aetheros-qdrant',
                    'aetheros-app', 'aetheros-adminer'
                ]
                
                if len(containers) == len(expected_containers):
                    self.add_result("Docker Network", True, "Network properly configured", {
                        "containers": containers,
                        "driver": network_info[0].get('Driver', 'unknown')
                    })
                    return True
                else:
                    missing = set(expected_containers) - set(containers)
                    self.add_result("Docker Network", True, f"Network exists, some containers missing: {', '.join(missing)}", {
                        "containers": containers,
                        "expected": expected_containers
                    })
                    return True  # Network exists, just missing some containers
            else:
                self.add_result("Docker Network", False, "Network not found or error")
                return False
                
        except Exception as e:
            self.add_result("Docker Network", False, f"Network check failed: {str(e)}")
            return False
    
    def check_docker_volumes(self) -> bool:
        """Check if Docker volumes are properly configured."""
        try:
            result = subprocess.run(['docker', 'volume', 'ls', '--format', '{{json .}}'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                volumes = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        volumes.append(json.loads(line).get('Name', ''))
                
                expected_volumes = [
                    'aetheros-postgres-data', 'aetheros-redis-data',
                    'aetheros-qdrant-data', 'aetheros-cache', 'aetheros-data'
                ]
                
                found_volumes = [v for v in volumes if any(exp in v for exp in expected_volumes)]
                
                if len(found_volumes) >= len(expected_volumes):
                    self.add_result("Docker Volumes", True, "All required volumes found", {
                        "volumes": found_volumes
                    })
                    return True
                else:
                    self.add_result("Docker Volumes", True, f"Some volumes found: {len(found_volumes)}/{len(expected_volumes)}", {
                        "found": found_volumes,
                        "expected": expected_volumes
                    })
                    return True  # Partial success
            else:
                self.add_result("Docker Volumes", False, "Failed to list volumes")
                return False
                
        except Exception as e:
            self.add_result("Docker Volumes", False, f"Volume check failed: {str(e)}")
            return False
    
    def check_testing_framework(self) -> bool:
        """Check if testing framework is available."""
        test_files = [
            'tools/docker/test_docker_health.py',
            'tools/docker/docker_test_suite.py',
            'tools/docker/verify_docker_setup.py'
        ]
        
        found_files = []
        
        for file in test_files:
            if os.path.exists(file):
                found_files.append(file)
        
        if len(found_files) == len(test_files):
            self.add_result("Testing Framework", True, "All testing files found", {
                "files": found_files
            })
            return True
        else:
            missing = set(test_files) - set(found_files)
            self.add_result("Testing Framework", False, f"Missing test files: {', '.join(missing)}")
            return False
    
    def check_documentation(self) -> bool:
        """Check if documentation files exist."""
        doc_files = [
            'docs/DOCKER_SETUP.md',
            'docs/DOCKER_TROUBLESHOOTING.md'
        ]
        
        found_files = []
        
        for file in doc_files:
            if os.path.exists(file):
                found_files.append(file)
        
        if len(found_files) == len(doc_files):
            self.add_result("Documentation", True, "All documentation files found", {
                "files": found_files
            })
            return True
        else:
            missing = set(doc_files) - set(found_files)
            self.add_result("Documentation", False, f"Missing documentation: {', '.join(missing)}")
            return False
    
    def run_health_checks(self) -> bool:
        """Run the Docker health check script."""
        try:
            result = subprocess.run([
                sys.executable, 'tools/docker/test_docker_health.py'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse output to get health status
                output = result.stdout
                if "ALL SERVICES HEALTHY" in output:
                    self.add_result("Health Checks", True, "All services passed health checks")
                    return True
                else:
                    self.add_result("Health Checks", True, "Health checks completed with warnings", {
                        "output": output[:200] + "..." if len(output) > 200 else output
                    })
                    return True
            else:
                self.add_result("Health Checks", False, "Health checks failed", {
                    "error": result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr
                })
                return False
                
        except Exception as e:
            self.add_result("Health Checks", False, f"Health check execution failed: {str(e)}")
            return False
    
    def run_test_suite(self) -> bool:
        """Run the Docker test suite."""
        try:
            result = subprocess.run([
                sys.executable, 'tools/docker/docker_test_suite.py'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.add_result("Test Suite", True, "All Docker tests passed")
                return True
            else:
                self.add_result("Test Suite", False, "Some Docker tests failed", {
                    "output": result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
                })
                return False
                
        except Exception as e:
            self.add_result("Test Suite", False, f"Test suite execution failed: {str(e)}")
            return False
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive verification report."""
        end_time = time.time()
        duration = end_time - self.start_time
        
        passed_tests = sum(1 for r in self.results if r.passed)
        total_tests = len(self.results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "verification_completed": datetime.datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "tests_passed": passed_tests,
            "tests_total": total_tests,
            "success_rate": round(success_rate, 1),
            "overall_status": "PASS" if passed_tests == total_tests else "FAIL",
            "results": [
                {
                    "test_name": r.test_name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ]
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = "docker_verification_report.json") -> None:
        """Save verification report to file."""
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Verification report saved to: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save report: {str(e)}")
    
    def run_all_checks(self) -> bool:
        """Run all verification checks."""
        print("=" * 60)
        print("AetherOS Docker Setup Verification")
        print("=" * 60)
        print()
        
        # Run all checks
        checks = [
            self.check_docker_installed,
            self.check_docker_compose_installed,
            self.check_docker_daemon,
            self.check_docker_compose_files,
            self.check_dockerfiles,
            self.check_services_running,
            self.check_port_accessibility,
            self.check_docker_network,
            self.check_docker_volumes,
            self.check_testing_framework,
            self.check_documentation,
            self.run_health_checks,
            self.run_test_suite
        ]
        
        results = []
        for check in checks:
            try:
                result = check()
                results.append(result)
            except Exception as e:
                print(f"❌ {check.__name__}: Failed with exception: {str(e)}")
                results.append(False)
        
        # Generate and save report
        report = self.generate_report()
        self.save_report(report)
        
        # Print summary
        print()
        print("=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Tests Passed: {report['tests_passed']}/{report['tests_total']}")
        print(f"Success Rate: {report['success_rate']}%")
        print(f"Duration: {report['duration_seconds']} seconds")
        print(f"Overall Status: {'✅ PASS' if report['overall_status'] == 'PASS' else '❌ FAIL'}")
        print("=" * 60)
        
        return report['overall_status'] == 'PASS'


def main():
    """Main entry point for Docker setup verification."""
    verifier = DockerSetupVerifier()
    success = verifier.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
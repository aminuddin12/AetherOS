#!/usr/bin/env python3
"""
Demonstration of the new Company Brain runtime resource resolution feature.

This script shows how the KnowledgeFacade.index_resource() method now uses
the full runtime services stack to resolve and aggregate resource information.
"""

import asyncio
from aether_runtime import RuntimeBuilder


async def main():
    print("=== AetherOS Company Brain Runtime Resource Resolution Demo ===\n")
    
    # Initialize the runtime
    runtime = RuntimeBuilder().build()
    print("✓ Runtime initialized with all services\n")
    
    # Test 1: Artifact resource resolution
    print("1. Testing artifact resource resolution:")
    artifact_uri = "artifact://company/schema/employee/v1"
    artifact_resource = await runtime.knowledge.index_resource(
        uri=artifact_uri,
        tags=["schema", "employee", "hr"]
    )
    
    print(f"   URI: {artifact_resource.uri}")
    print(f"   Identifier: {artifact_resource.identifier}")
    print(f"   Title: {artifact_resource.title}")
    print(f"   Summary: {artifact_resource.summary}")
    print(f"   Artifact Info: {artifact_resource.artifact_info}")
    print(f"   Repository Graph: {len(artifact_resource.repository_graph)} entries")
    print(f"   Workspace Context: {artifact_resource.workspace_context.get('name', 'N/A')}")
    print(f"   Storage Metadata: {artifact_resource.storage_metadata.get('uri', 'N/A')}")
    print(f"   Organization Info: {artifact_resource.organization_info.get('status', 'N/A')}")
    print()
    
    # Test 2: Workspace resource resolution
    print("2. Testing workspace resource resolution:")
    workspace_uri = "workspace://engineering/ai-team"
    workspace_resource = await runtime.knowledge.index_resource(
        uri=workspace_uri,
        tags=["team", "engineering"]
    )
    
    print(f"   URI: {workspace_resource.uri}")
    print(f"   Title: {workspace_resource.title}")
    print(f"   Summary: {workspace_resource.summary}")
    print()
    
    # Test 3: Query the indexed resources
    print("3. Querying indexed resources:")
    results = await runtime.knowledge.query("engineering")
    print(f"   Found {results.total} resources matching 'engineering'")
    for result in results.results:
        print(f"   - {result.title}: {result.summary}")
    print()
    
    # Test 4: Verify backward compatibility
    print("4. Testing backward compatibility with direct indexing:")
    direct_uri = "document://manual/onboarding"
    await runtime.knowledge.index(
        uri=direct_uri,
        title="Employee Onboarding Manual",
        summary="Comprehensive guide for new employee onboarding process",
        tags=["hr", "onboarding"]
    )
    
    direct_results = await runtime.knowledge.query("onboarding")
    print(f"   Direct indexing still works: {direct_results.total} results found")
    print()
    
    print("✓ Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("• Runtime service orchestration (artifact, repository, workspace, storage, organization)")
    print("• Aggregated resource information in KnowledgeResource model")
    print("• Backward compatibility with existing index() method")
    print("• Graceful degradation when services return minimal data")


if __name__ == "__main__":
    asyncio.run(main())
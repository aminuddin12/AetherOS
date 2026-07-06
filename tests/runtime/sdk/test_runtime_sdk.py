import pytest
from aether_runtime import AetherRuntime, RuntimeBuilder
from aether_runtime.context.context import RuntimeContext


@pytest.mark.asyncio
async def test_runtime_sdk_initialization():
    context = RuntimeContext(user_id="tester", workspace_id="w-001")
    runtime = RuntimeBuilder().with_context(context).build()

    assert runtime.context.user_id == "tester"
    assert runtime.context.workspace_id == "w-001"
    assert runtime.kernel is not None
    assert runtime.execution is not None
    assert runtime.workspace is not None
    assert runtime.storage is not None
    assert runtime.repository is not None
    assert runtime.artifact is not None
    assert runtime.organization is not None
    assert runtime.knowledge is not None
    assert runtime.provider_router is not None
    assert runtime.workflow is not None


@pytest.mark.asyncio
async def test_knowledge_facade_index_and_query():
    runtime = RuntimeBuilder().build()

    uri = "artifact://test/item"
    await runtime.knowledge.index(
        uri=uri,
        title="Test Item",
        summary="A test artifact for Company Brain indexing.",
        tags=["test", "artifact"],
    )

    results = await runtime.knowledge.query("test")
    assert results.total == 1
    assert results.results[0].uri == uri
    assert results.scored[uri] > 0

    description = await runtime.knowledge.describe(uri)
    assert description["uri"] == uri
    assert description["title"] == "Test Item"


@pytest.mark.asyncio
async def test_provider_router_selection():
    runtime = RuntimeBuilder().build()
    provider = await runtime.provider_router.select(capability="llm", preference="speed")
    assert provider["provider_id"] == "openai-gpt-4o"

    provider = await runtime.provider_router.select(capability="llm", preference="cost")
    assert provider["provider_id"] == "anthropic-claude-3-5" or provider["provider_id"] == "openai-gpt-4o"


@pytest.mark.asyncio
async def test_workflow_facade_lifecycle():
    runtime = RuntimeBuilder().build()
    workflow_id = await runtime.workflow.submit({"name": "test-workflow", "created_at": "2026-07-07"})

    status = await runtime.workflow.status(workflow_id)
    assert status["status"] == "submitted"

    assert await runtime.workflow.cancel(workflow_id)
    status = await runtime.workflow.status(workflow_id)
    assert status["status"] == "canceled"


@pytest.mark.asyncio
async def test_knowledge_runtime_resource_resolution():
    """Test the new runtime resource resolution flow using all runtime services."""
    runtime = RuntimeBuilder().build()
    
    # Test with artifact URI
    artifact_uri = "artifact://test/schema/v1"
    resource = await runtime.knowledge.index_resource(uri=artifact_uri, tags=["test", "artifact"])
    
    # Verify the resource structure
    assert resource.uri == artifact_uri
    assert resource.identifier == artifact_uri  # Should be resolved by artifact service
    # Title includes workspace name from mock workspace service
    assert "Default Workspace" in resource.title
    # Summary includes workspace, storage, and organization info from mock services
    assert "Workspace:" in resource.summary
    assert "Storage:" in resource.summary
    assert "Organization:" in resource.summary
    assert isinstance(resource.artifact_info, dict)
    assert isinstance(resource.repository_graph, dict)
    assert isinstance(resource.workspace_context, dict)
    assert isinstance(resource.storage_metadata, dict)
    assert isinstance(resource.organization_info, dict)
    
    # Test that it was also indexed as a document (backward compatibility)
    results = await runtime.knowledge.query("artifact")
    assert results.total >= 1
    
    # Test with different URI types
    workspace_uri = "workspace://test-workspace"
    workspace_resource = await runtime.knowledge.index_resource(uri=workspace_uri)
    
    assert workspace_resource.uri == workspace_uri
    assert workspace_resource.identifier == workspace_uri
    
    # Test with storage URI - should work fine with mock services
    storage_uri = "storage://invalid/path"
    storage_resource = await runtime.knowledge.index_resource(uri=storage_uri)
    
    assert storage_resource.uri == storage_uri
    assert "Storage:" in storage_resource.summary
    assert "Workspace:" in storage_resource.summary

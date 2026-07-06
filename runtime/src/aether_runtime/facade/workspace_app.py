class WorkspaceAppFacade:
    """Public interface for Workspace Application Runtime (Milestone 3.4)."""
    
    def __init__(self, engine):
        self.engine = engine
        
    async def execute(self, command) -> any:
        return await self.engine.execute_command(command)
        
    async def query(self, query) -> any:
        return await self.engine.execute_query(query)

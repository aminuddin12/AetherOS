from typing import Callable
from .context import CommandContext
from .events import event_manager

class CommandPipeline:
    @staticmethod
    def execute(command: Callable, ctx: CommandContext, **kwargs):
        # 1. Validate
        
        # 2. Load Config (assume attached to ctx)
        
        # 3. Permission Check
        
        # 4. Trigger Before Event
        event_manager.dispatch("BeforeCommand", command=command.__name__, ctx=ctx)
        
        # 5. Execute
        result = command(ctx, **kwargs)
        
        # 6. Trigger After Event
        event_manager.dispatch("AfterCommand", command=command.__name__, result=result)
        
        # 7. Output Handling is usually done within command via Formatter
        return result

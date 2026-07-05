from enum import Enum

class SupervisorPolicy(Enum):
    IGNORE = "ignore"
    RETRY = "retry"
    DEAD_LETTER = "dead_letter"
    TELEMETRY = "telemetry"
    RAISE = "raise"

class DispatcherPolicy:
    def __init__(self, policy: SupervisorPolicy = SupervisorPolicy.TELEMETRY):
        self.supervisor_policy = policy

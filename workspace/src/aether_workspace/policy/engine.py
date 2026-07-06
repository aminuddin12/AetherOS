from typing import Dict, Any

class PolicyEngine:
    def evaluate(self, policies: Dict[str, Any], context: dict, action: str) -> bool:
        # Stub implementation for policy evaluation
        policy = policies.get(action)
        if policy is None:
            return True # Default allow for stub
        return policy.get("allow", True)

policy_engine = PolicyEngine()

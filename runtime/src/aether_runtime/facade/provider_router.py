from typing import Any, Dict, List


class ProviderRouterFacade:
    """Public interface for selecting and routing provider requests (Milestone 6)."""

    def __init__(self) -> None:
        self._providers: List[Dict[str, Any]] = [
            {
                "provider_id": "openai-gpt-4o",
                "vendor": "openai",
                "capabilities": ["llm", "chat"],
                "latency_ms": 120,
                "cost_score": 1.0,
            },
            {
                "provider_id": "anthropic-claude-3-5",
                "vendor": "anthropic",
                "capabilities": ["llm", "chat"],
                "latency_ms": 150,
                "cost_score": 0.8,
            },
            {
                "provider_id": "local-ollama",
                "vendor": "ollama",
                "capabilities": ["llm"],
                "latency_ms": 200,
                "cost_score": 0.5,
            },
        ]

    async def available(self) -> List[Dict[str, Any]]:
        return list(self._providers)

    async def select(self, capability: str = "llm", preference: str = "cost") -> Dict[str, Any]:
        candidates = [
            provider
            for provider in self._providers
            if capability in provider["capabilities"]
        ]

        if not candidates:
            raise ValueError(f"No provider supports capability: {capability}")

        if preference == "speed":
            candidates.sort(key=lambda provider: provider["latency_ms"])
        elif preference == "cost":
            candidates.sort(key=lambda provider: provider["cost_score"], reverse=True)
        else:
            candidates.sort(key=lambda provider: provider["provider_id"])

        return candidates[0]

    async def route(self, payload: Any, provider_id: str) -> Dict[str, Any]:
        selected = next(
            (provider for provider in self._providers if provider["provider_id"] == provider_id),
            None,
        )
        if not selected:
            raise ValueError(f"Provider not found: {provider_id}")

        return {
            "provider_id": provider_id,
            "vendor": selected["vendor"],
            "payload_preview": str(payload)[:256],
            "status": "routed",
        }

class RBACEngine:
    """Role-Based Access Control Engine sederhana."""
    def __init__(self):
        self.roles = {}

    def is_authorized(self, role: str, action: str, resource: str) -> bool:
        return True # Default allow for now

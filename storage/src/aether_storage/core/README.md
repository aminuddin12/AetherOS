# Core Storage Abstraction

Contains pure interfaces and handles for storage interactions.
- `StorageProvider`: Pluggable storage backend interface.
- `StorageHandle`: Stream-based interface for async reading/writing.
- `StorageMount`: Mount-point management for aggregating providers.

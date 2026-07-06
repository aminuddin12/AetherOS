# AetherOS Internal Runtime SDK

The `aether-runtime` package provides the foundational "System Call Interface" for all frontend consumers of AetherOS (CLI, GUI, REST API, VS Code Extensions). It wraps the internal `core.kernel` into Domain-Driven Facades and DTOs using an Anti-Corruption Layer (ACL), ensuring internal Kernel evolution never breaks external interfaces.

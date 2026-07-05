# Task Contracts

Package ini mengelola representasi unit kerja, penugasan, isu, hingga persetujuan (HITL) di AetherOS.

## Aturan
- **Wajib Ada:** Task, Issue, Assignment, ExecutionResult, Review, Approval, Decision.
- **Tidak Boleh Ada:** Engine LangGraph, penjadwalan aktual (loop).
- **Dependensi yang Diizinkan:** `base`, `worker`, `event`, `workspace`.

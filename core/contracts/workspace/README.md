# Workspace Contracts

Package ini mendefinisikan isolasi lingkungan (Workspace), Code Repository, Manajemen Artifact (seperti gambar/diagram), dan lingkungan deployment.

## Aturan
- **Wajib Ada:** Workspace, ArtifactStore, Repository, Branch, Commit, PullRequest, Deployment, Environment.
- **Tidak Boleh Ada:** Git client implementation (e.g., PyGit2), AWS S3 Boto3 API.
- **Dependensi yang Diizinkan:** `base`, `common`.

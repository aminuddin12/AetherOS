# ADR-0013: Workspace Resource Tree

## Status
Accepted

## Context
Sebuah Workspace perlu menyimpan berbagai tipe data: kode sumber, dokumen, model AI (knowledge embeddings), rahasia, serta *event logs*. Menggunakan istilah *Virtual File System (VFS)* menciptakan asumsi bahwa semua hal harus disimpan sebagai file teks atau biner standar.

## Decision
Kita beralih dari terminologi *VFS* ke **Workspace Resource Tree**.
- Entitas dasarnya adalah `WorkspaceNode`.
- Sebuah `WorkspaceNode` bisa berupa Artifact (file fisik), Knowledge Reference (embedding index), Workflow Definition, atau Asset lainnya.
- Node ini di-manage oleh `ResourceProvider`. Pada Milestone awal, kita akan menggunakan **Memory Provider**, lalu menyusul dengan **Local Filesystem Adapter**, **Cloud Object Storage Adapter**, dan sebagainya.

## Consequences
- **Keuntungan**: Model arsitektur ini mendukung penyimpanan *hybrid* (sebagian di RAM, sebagian di disk, sebagian di cloud) dan tidak membatasi AI agent hanya berinteraksi melalui fungsi *filesystem* konvensional.
- **Kerugian**: Kompleksitas implementasi *Resource Provider* yang tidak bisa langsung diterjemahkan ke *I/O syscall* sistem operasi bawaan.

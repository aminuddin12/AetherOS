# ADR-0024: Resource Ownership Matrix

## Status
Accepted

## Context
AetherOS adalah *Knowledge Platform*. Kekacauan data rentan terjadi bila beberapa runtime merasa memiliki wewenang untuk menyimpan atau memodifikasi objek yang sama (misalnya, *Repository* dan *Artifact* sama-sama menyimpan konten *file*).

## Decision
Disahkan prinsip kepemilikan tunggal (*Single Responsibility*) yang didefinisikan dalam **Resource Ownership Matrix**:

| Runtime       | Owns (Kepemilikan Mutlak)                                 | Never Owns (Haram Disimpan)           |
| ------------- | --------------------------------------------------------- | ------------------------------------- |
| Storage       | Blob, Streams, Binary Data                                | Metadata, Revision History            |
| Repository    | Revision, Branch, Changeset, Graph History                | Blob / File Content                   |
| Artifact      | Identity, Metadata, Semantic Lineage, Classification      | Blob, Revision Graph                  |
| Workspace     | Context, Lifecycle State, Runtime Policy                  | Blob, Knowledge Graph                 |
| Company Brain | Knowledge Graph, Embeddings, Reasoning Index              | Blob, Revision, Raw Artifact Metadata |

**Aturan Emas:**
*Company Brain* sama sekali tidak "menyimpan" pengetahuan fisik. Ia murni berfungsi sebagai **Knowledge Orchestrator** yang merajut kepingan informasi dari `storage://`, `repository://`, dan `artifact://`.

## Consequences
- **Positive**: Jika *Company Brain* di-reset atau algoritma *embedding* diubah, tidak ada satu pun *source data* atau metadata yang hilang, karena data tersimpan di runtime aslinya.
- **Negative**: Penggabungan informasi yang kompleks (misal: "tampilkan kode dari *prompt* terbaru") menuntut orkestrasi *query* lintas-domain yang rumit.

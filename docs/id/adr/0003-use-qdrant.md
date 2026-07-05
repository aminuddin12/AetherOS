# ADR-0003: Penggunaan Qdrant untuk Vector Database

## Konteks
AetherOS membutuhkan "Company Brain" untuk menyimpan dan melakukan pencarian semantik (Semantic Search) terhadap *Global Knowledge*, *Patterns*, dan histori percakapan agen yang jumlahnya terus membesar (mencapai jutaan embedding vektor seiring berjalannya perusahaan).

## Keputusan
Kita menggunakan **Qdrant** sebagai mesin Vector Database utama (tersedia juga opsi in-memory untuk pengujian lokal, dan Docker image untuk produksi).

## Konsekuensi Positif
- Qdrant ditulis dalam bahasa Rust, yang menawarkan performa dan efisiensi memori yang sangat tinggi.
- Fitur *Metadata Filtering* di Qdrant sangat kaya, memungkinkan kita memfilter hasil pencarian vektor berdasarkan *Workspace ID* atau *Project ID* (krusial untuk privasi Multi-Workspace).
- Mendukung mode *hybrid search* secara native.

## Konsekuensi Negatif
- Ekosistem tidak sebesar ChromaDB atau Pinecone (namun cukup stabil dan matang untuk produksi).

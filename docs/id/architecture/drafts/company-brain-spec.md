# Company Brain Specification (Draft M4)

## 1. Konsep Utama
*Company Brain* BUKAN sekadar Large Language Model (LLM). Ia bukanlah OpenAI, Claude, ataupun model lokal. *Company Brain* adalah **Knowledge Orchestrator**. 

Ia tidak menyimpan *knowledge database* statisnya sendiri. Ia merakit pengetahuan secara dinamis dari ekosistem *AetherOS Runtime*.

## 2. Paradigma Resource Reference
Sesuai arahan spesifikasi arsitektur OS, seluruh *reasoning* (proses nalar) dilakukan terhadap `ResourceReference`.
Company Brain tidak pernah memindai *file system* langsung (`/path/file.py`). Ia akan bekerja mengandalkan URI:
- `artifact://...`
- `repository://...`
- `workspace://...`
- `storage://...`

## 3. Graf Pengetahuan (Knowledge Triple)
Company Brain bertugas membangkitkan relasi kontekstual dengan format **Subject-Predicate-Object** (*Knowledge Triple*).

Contoh representasi:
- `[Artifact A] implements [Contract B]`
- `[Repository X] contains [Artifact Y]`
- `[Workspace Z] belongs_to [Organization A]`

Graf ini terbentuk dengan cara mengorkestrasi lapisan *Artifact*, *Repository*, dan *Organization Runtime*.

## 4. Aliran Dependensi Knowledge
Pengetahuan dibangun dan didistribusikan secara bottom-up:
```text
Storage 
  ↓ 
Repository 
  ↓ 
Artifact 
  ↓ 
Organization 
  ↓ 
Company Brain
```

Brain = Orchestrator, Brain ≠ Database. 

Dengan draf ini, pada Milestone 4, pengembangan tidak akan terjebak merakit *chatbot*, melainkan menciptakan mesin analitik spasial terhadap organisasi itu sendiri.

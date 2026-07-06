# ADR-0023: Runtime Communication

## Status
Accepted

## Context
Dengan puluhan package yang berjalan berdampingan, diperlukan cara standar untuk runtime berkomunikasi satu sama lain. Jika runtime memanggil *internal function* runtime lain secara langsung, akan timbul ketergantungan erat (tight coupling) yang merusak konsep arsitektur OS.

## Decision
Alur komunikasi lintas runtime dibakukan sebagai berikut:

**Runtime -> Reference -> URI -> SDK -> Facade -> Protocol**

1. Runtime pemanggil membuat sebuah **Reference Object** yang menyimpan **URI**.
2. Reference Object diserahkan ke **Runtime SDK**.
3. SDK mengarahkan panggilan ke **Facade** dari runtime tujuan.
4. Facade menerjemahkan permintaan dan memanggil **Protocol/Backend** internalnya.

Contoh: *Artifact Runtime* tidak pernah meng-import *Storage Backend*. Ia hanya meneruskan `storage://...` ke Facade milik *Storage Runtime* melalui SDK terpusat.

## Consequences
- **Positive**: Isolasi total. Facade dapat dimodifikasi tanpa merusak runtime lain.
- **Negative**: Ada lapisan abstraksi ekstra untuk setiap operasi lintas-runtime.

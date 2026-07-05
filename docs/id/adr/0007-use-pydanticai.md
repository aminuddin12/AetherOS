# ADR-0007: Penggunaan PydanticAI untuk Agent Runtime & Validation

## Konteks
LLM sering menghasilkan output yang tidak terstruktur atau salah format (halusinasi format). Untuk sebuah Sistem Operasi, output semacam ini akan menyebabkan sistem *crash*. Kita membutuhkan *Agent Runtime* yang secara agresif memaksa LLM mengembalikan data sesuai skema yang diizinkan (Structured Outputs).

## Keputusan
Kita menggunakan **PydanticAI** (dari pengembang Pydantic) sebagai fondasi *Agent Runtime* (Agent SDK).

## Konsekuensi Positif
- Dukungan *Structured Outputs* kelas satu (First-class support) berbasis Pydantic.
- Mendukung fitur *Dependency Injection* (DI) asli yang sangat cocok untuk mengalirkan memori (Company Brain) secara dinamis ke agen.
- *Type-safety* yang ketat membuat pengembangan agen baru (melalui Plugin SDK) jauh lebih aman dari error *runtime*.

## Konsekuensi Negatif
- Relatif baru dibandingkan dengan arsitektur agen tradisional (seperti AutoGPT core), sehingga mungkin ada batasan pada beberapa *edge case*.

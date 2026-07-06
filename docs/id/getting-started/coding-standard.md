# Coding Standard

1. **Python Version**: Wajib menggunakan Python 3.12+.
2. **Type Hinting**: Wajib 100% menggunakan Type Hints yang ketat (`mypy` compliant).
3. **Pydantic**: Gunakan Pydantic V2 untuk model, validasi, dan serialisasi data. Model bisnis (Contract) harus selalu `frozen=True`.
4. **Clean Architecture**: Pisahkan Interface (Protocol) dari Implementation.
5. **Naming Convention**: 
   - Class: `PascalCase`
   - Method/Function: `snake_case`
   - File/Module: `snake_case`
   - Interface/Protocol: Akhiri dengan `Protocol` atau nama yang mencerminkan kapabilitas (misal `Dispatcher`).

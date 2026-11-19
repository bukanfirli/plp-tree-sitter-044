# CLI Pemeriksa Kode Python (`cek.py`)

Tool berbasis `tree-sitter-python` untuk memeriksa kualitas dan validitas sintaks file Python di dalam suatu folder secara rekursif.

## Fitur
1. **Deteksi TODO / FIXME:** Mencari semua komentar yang mengandung `TODO` atau `FIXME` beserta nomor barisnya.
2. **Deteksi Fungsi Panjang:** Melaporkan setiap fungsi (`function_definition`, termasuk method di dalam kelas atau fungsi bersarang) yang panjangnya lebih dari 30 baris.
3. **Deteksi Syntax Error:** Melaporkan file yang pohon sintaksnya memiliki `has_error == True` beserta baris pertama node `ERROR`/`MISSING`.

## Cara Memasang Dependensi
```bash
pip install tree-sitter tree-sitter-python
# Laporan Praktikum Tree-sitter
- **Nama:** Firliana Febrina
- **NIM:** 251524044
- **Kelas:** 1B D4 Teknik Informatika

---

## Tugas 1: Membaca Pohon Sintaks

### 1. Perkiraan S-Expression vs Hasil Sebenarnya

#### a. Potongan Fungsi (`def sapa(nama): return "Halo " + nama`)
* **Perkiraan Awal:**
  ```lisp
  (module
    (function_definition
      name: (identifier)
      parameters: (parameters (identifier))
      body: (block
        (return_statement
          (binary_operator left: (string) right: (identifier))))))
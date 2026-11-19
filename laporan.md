# Laporan Praktikum Tree-sitter
- **Nama:** Firliana Febrina
- **NIM:** 251524044
- **Kelas:** 1B D4 Teknik Informatika

---

## Tugas 1: Membaca Pohon Sintaks

### 1. Perkiraan Pohon (Tulisan Tangan) vs Hasil Sebenarnya
![Perkiraan Pohon Tulisan Tangan](ss/t1_tulisan_tangan_perkiraan.jpeg)
![Output Terminal Tugas 1](ss/t1_output.png)

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

---

## Tugas 2: Penjelajah Node (`jelajah.py`)

### 1. Hasil Penelusuran Pohon
Program `jelajah.py` menelusuri node bernama secara rekursif (*preorder DFS*) menggunakan `enumerate(node.children)` untuk mengambil label `field_name_for_child(i)` serta posisi `start_point` (`baris + 1 : kolom`).

![Output Jelajah File Kecil](bukti ss/t2_kecil.png)
![Output Jelajah File Besar >=100 Baris](bukti ss/t2_besar.png)

### 2. Kendala 
* **Kendala:** Jika melakukan perulangan langsung pada `node.named_children`, indeks yang dihasilkan tidak cocok dengan `node.field_name_for_child(i)` karena metode tersebut menghitung indeks dari `node.children` (termasuk node anonim). 
* **Solusi:** Melakukan iterasi pada `enumerate(node.children)` lalu memfilter dengan `if child.is_named:`.

---

## Tugas 3: Query & Pattern Matching (`.scm`)

### 1. Hasil Query & Verifikasi Manual
Pengujian dilakukan pada file `contoh_t3.py` menggunakan 3 pola query:
1. **Query Fungsi & Parameter (`fungsi.scm`):** Menggunakan `matches()` pada `QueryCursor` untuk memasangkan `@nama` dan `named_child_count` dari `@params`. Hasil: `sapa` (1), `hitung_luas` (3), dan `tanpa_param` (0) — cocok 100% dengan hitungan manual.
2. **Query Pemanggilan `print` (`print.scm`):** Menggunakan predikat `(#eq? @fn "print")`. Berhasil menangkap 3 pemanggilan `print(...)` pada baris 7, 12, dan 16 tanpa menangkap panggilan fungsi `sapa("Budi")` pada baris 18.
3. **Query Import Modul (`import.scm`):** Menangkap `(import_statement)` (termasuk `aliased_import` seperti `import sys as system`) dan `(import_from_statement)` dengan `module_name:`. Berhasil menangkap 4 modul (`os`, `sys`, `pathlib`, `typing`).

![Output Query Tugas 3](bukti ss/t3_hasil_query.png)

---

## Tugas 4: Grammar DSL Filter (`tree-sitter-filter`)

### 1. Rancangan Grammar & Uji Kasus
Grammar `filter` dibangun bertahap di `tree-sitter-filter/grammar.js` untuk mendukung ekspresi logika (`and`, `or`, `not`), tanda kurung, perbandingan (`=`, `!=`, `>`, `<`, `>=`, `<=`), operator `contains`, serta operator `in` dengan daftar nilai (`in_expression`). Sebanyak **6 kasus uji** ditulis di `test/corpus/dasar.txt` dan seluruhnya lulus pada pengujian `tree-sitter test`.

![Conflict Operator Tanpa Prec](bukti ss/t4_conflict.png)
![Hasil Tree-sitter Test](bukti ss/t4_test.png)
![Hasil Tree-sitter Parse](bukti ss/t4_parse.png)

### 2. Kendala 
* **Kendala 1 (`Unresolved conflict`):** Saat menambahkan `or_expression` dan `and_expression` tanpa `prec.left`, `tree-sitter generate` menolak karena ambiguitas pengelompokan `a = 1 or b = 2 and c = 3`. **Solusi:** Memberikan `prec.left(1, ...)` untuk `or_expression` dan `prec.left(2, ...)` untuk `and_expression` agar `and` mengikat lebih kuat daripada `or`.
* **Kendala 2 (Keyword terbaca sebagai `identifier`):** Kata kunci `and` dan `or` sempat tertangkap sebagai `identifier`. **Solusi:** Menambahkan properti `word: $ => $.identifier` pada konfigurasi grammar.

---

## Tugas 5: Syntax Highlighting (`queries/highlights.scm`)

### 1. Pemetaan Capture Highlight
Aturan pewarnaan sintaks ditulis di `tree-sitter-filter/queries/highlights.scm` dengan memetakan token ke standar capture tree-sitter: kata kunci (`and`, `or`, `not`, `in`, `contains`) ke `@keyword`, operator perbandingan ke `@operator`, literal ke `@string`/`@number`/`@constant.builtin`, serta nama kolom pada `comparison` dan `in_expression` ke `@property`.

![Hasil Highlight DSL Filter](bukti ss/t5_highlight.png)

### 2. Kendala 
* **Kendala:** Saat pertama kali menjalankan `tree-sitter parse`/`highlight`, CLI menampilkan peringatan bahwa `parser-directories` belum dikonfigurasi, dan penulisan `config.json` dengan `Out-File -Encoding utf8` di PowerShell sempat menyisipkan UTF-8 BOM sehingga JSON gagal dibaca. **Solusi:** Menulis ulang `config.json` menggunakan `[System.IO.File]::WriteAllText` tanpa BOM dan mendaftarkan folder induk `plp-tree-sitter-044`.

---

## Tugas 6: Mini Proyek CLI Pemeriksa Kode (`cek/cek.py`)

### 1. Hasil Pengujian Lokal & Repositori Nyata
Tool `cek.py` menggabungkan `QueryCursor` (untuk mencari komentar `TODO|FIXME` dan mengukur rentang baris `function_definition`) serta penelusuran rekursif untuk menemukan baris pertama `is_error`/`is_missing` saat `tree.root_node.has_error` bernilai `True`.

* **Uji Folder `uji/`:** Berhasil mendeteksi 2 komentar TODO/FIXME pada `todo.py`, 1 fungsi panjang (`proses_data_panjang`, 32 baris) pada `panjang.py`, dan 1 error sintaks pada `rusak.py` baris 1.
* **Uji Repositori Nyata (`psf/requests`):** Berhasil memindai seluruh file `.py` di repositori open source dan mencocokkan temuan komentar `TODO` serta fungsi panjang secara manual pada 2 file acak (`src/requests/models.py` dan `src/requests/sessions.py`).

![Hasil Uji Lokal cek.py](bukti ss/t6_uji.png)
![Hasil Uji Repo Nyata](bukti ss/t6_repo_nyata.png)

### 2. Kendala & Catatan Penggunaan AI
* **Kendala:** Saat memindai folder proyek yang memiliki virtual environment (`venv/`) atau `.git/`, skrip ikut memeriksa ribuan file library pihak ketiga sehingga proses berjalan lambat. **Solusi:** Menambahkan filter `ABAIKAN_FOLDER` untuk melewati direktori `venv`, `.venv`, `.git`, dan `__pycache__`.

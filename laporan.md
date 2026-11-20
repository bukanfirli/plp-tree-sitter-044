# Laporan Praktikum Tree-sitter
- **Nama:** Firliana Febrina
- **NIM:** 251524044
- **Kelas:** 2B D4 Teknik Informatika

---

## Tugas 1: Membaca Pohon Sintaks

### 1. Perkiraan Pohon (Tulisan Tangan) vs Hasil Sebenarnya
Perbandingan perkiraan tulisan tangan dengan S-expression asli dari parser Python pada fungsi `def sapa(nama): return "Halo " + nama` dan `if x > 0: print("positif")` menunjukkan struktur blok (`function_definition`, `if_statement`) sudah tepat, namun pohon asli membungkus argumen ke dalam node `parameter_list`, `argument_list`, dan `block`.

![Perkiraan Pohon Tulisan Tangan](bukti%20ss/t1_tulisan_tangan_perkiraan.jpeg)
![Output Terminal Tugas 1](bukti%20ss/t1_terminal.png)
---

## Tugas 2: Penjelajah Node (`jelajah.py`)
Program `jelajah.py` menelusuri node bernama secara rekursif (*preorder DFS*) menggunakan `enumerate(node.children)` untuk mengambil label `field_name_for_child(i)` serta posisi `start_point` (`baris + 1 : kolom`).
* **Kendala & Solusi:** Perulangan langsung pada `node.named_children` membuat indeks tidak cocok dengan `field_name_for_child(i)` karena metode tersebut menghitung indeks dari `node.children` (termasuk node anonim). Diatasi dengan melakukan iterasi pada `enumerate(node.children)` lalu memfilter `if child.is_named:`.

![Output Jelajah File Kecil](bukti%20ss/t2_kecil.png)
![Output Jelajah File Besar >=100 Baris](bukti%20ss/t2_besar.png)
---

## Tugas 3: Query & Pattern Matching (`.scm`)
Pengujian pada `contoh_t3.py` menggunakan 3 pola query:
1. **`fungsi.scm`:** Menggunakan `matches()` untuk memasangkan `@nama` dan `named_child_count` dari `@params`. Hasil: `sapa` (1), `hitung_luas` (3), dan `tanpa_param` (0) — cocok 100% dengan hitungan manual.
2. **`print.scm`:** Menggunakan predikat `(#eq? @fn "print")`, menangkap 3 pemanggilan `print(...)` tanpa menangkap `sapa("Budi")`.
3. **`import.scm`:** Menangkap `(import_statement)` (termasuk `aliased_import`) dan `(import_from_statement)`, berhasil mendeteksi 4 modul (`os`, `sys`, `pathlib`, `typing`).

![Output Query Tugas 3](bukti%20ss/t3_hasil_query.png)
---

## Tugas 4: Grammar DSL Filter (`tree-sitter-filter`)
Grammar `filter` dibangun di `tree-sitter-filter/grammar.js` untuk mendukung operator logika (`and`, `or`, `not`), tanda kurung, perbandingan (`=`, `!=`, `>`, `<`, `>=`, `<=`), `contains`, dan `in_expression`. Seluruh **6 kasus uji** pada `test/corpus/dasar.txt` lulus pengujian `tree-sitter test`.
* **Kendala & Solusi:** Muncul `Unresolved conflict` saat menambahkan `or_expression` dan `and_expression` tanpa prioritas; diselesaikan dengan `prec.left(1, ...)` untuk `or` dan `prec.left(2, ...)` untuk `and`. Selain itu, properti `word: $ => $.identifier` ditambahkan agar kata kunci `and`/`or` tidak terbaca sebagai `identifier`.

![Conflict Operator Tanpa Prec](bukti%20ss/t4_conflict.png)
![Hasil Tree-sitter Test](bukti%20ss/t4_test.png)
![Hasil Tree-sitter Parse](bukti%20ss/t4_parse.png)
---

## Tugas 5: Syntax Highlighting (`queries/highlights.scm`)
Aturan pewarnaan sintaks memetakan kata kunci (`and`, `or`, `not`, `in`, `contains`) ke `@keyword`, operator ke `@operator`, literal ke `@string`/`@number`/`@constant.builtin`, serta nama kolom pada `comparison` dan `in_expression` ke `@property`.
* **Kendala & Solusi:** Penulisan `config.json` menggunakan `Out-File -Encoding utf8` di PowerShell menyisipkan UTF-8 BOM sehingga memicu error JSON. Diatasi dengan menulis ulang menggunakan `[System.IO.File]::WriteAllText` tanpa BOM dan mendaftarkan `parser-directories`.

![Hasil Highlight DSL Filter](bukti%20ss/t5_highlight.png)
---

## Tugas 6: Mini Proyek CLI Pemeriksa Kode (`cek/cek.py`)
Tool `cek.py` mendeteksi komentar `TODO|FIXME`, fungsi > 30 baris, serta file dengan `has_error == True` (menelusuri baris pertama `is_error`/`is_missing`). Diuji pada folder `uji/` (terdeteksi 2 TODO/FIXME, 1 fungsi 32 baris, 1 syntax error) dan repositori `psf/requests` (diverifikasi manual pada `models.py` dan `sessions.py`).
* **Kendala & Solusi:** Pemindaian ikut masuk ke folder `venv/` dan `.git/` sehingga eksekusi lambat. Diatasi dengan menambahkan filter `ABAIKAN_FOLDER` untuk melewati direktori lingkungan virtual dan cache.

![Hasil Uji Lokal cek.py](bukti%20ss/t6_uji.png)
![Hasil Uji Repo Nyata](bukti%20ss/t6_repo_nyata.png)
---

# Catatan Penggunaan AI

| Tugas | Yang diminta | Kesalahan AI | Bukti verifikasi |
| :--- | :--- | :--- | :--- |
| **Tugas 1** | Cara inisialisasi `tree_sitter_python` versi terbaru (`0.25+`). | Menyarankan `Language.build_library()` yang sudah *deprecated* dan memicu `AttributeError`. | Diubah ke `Language(tspython.language())` dan diuji lewat `python t1.py` (`bukti ss/t1_terminal.png`). |
| **Tugas 2** | Algoritma DFS rekursif untuk mencetak node bernama beserta label *field name*. | Memakai `enumerate(node.named_children)` sehingga indeks tidak sinkron dengan `field_name_for_child(i)`. | Diubah ke `enumerate(node.children)` dengan filter `is_named` (`bukti ss/t2_kecil.png`, `t2_besar.png`). |
| **Tugas 3** | Pola query `.scm` untuk fungsi + parameter, `print()`, dan `import`. | Query `import.scm` awalnya melewatkan `(import_from_statement)` (`from ... import ...`). | Menambahkan `(import_from_statement)` dan mencocokkan hasil dengan hitungan manual (`bukti ss/t3_hasil_query.png`). |
| **Tugas 4** | Perancangan `grammar.js` DSL `filter` (`and`, `or`, `not`, `in`, `contains`). | Tidak menambahkan `prec.left` pada `or`/`and` sehingga muncul `Unresolved conflict`. | Menambahkan `prec.left(1)` untuk `or` dan `prec.left(2)` untuk `and`; 6/6 tes lulus (`bukti ss/t4_test.png`). |
| **Tugas 5** | Pemetaan capture `highlights.scm` dan pembuatan `config.json`. | `Out-File -Encoding utf8` menyisipkan UTF-8 BOM sehingga memicu error `Bad JSON config`. | Menulis ulang `config.json` tanpa BOM dan menguji `tree-sitter highlight` (`bukti ss/t5_highlight.png`). |
| **Tugas 6** | Kerangka CLI `cek.py` untuk deteksi `TODO`, fungsi > 30 baris, dan error sintaks. | Ikut memindai ribuan file di dalam `venv/` dan `.git/` sehingga eksekusi lambat. | Menambahkan `ABAIKAN_FOLDER` dan memverifikasi hasil pada `uji/` serta `psf/requests` (`bukti ss/t6_uji.png`, `t6_repo_nyata.png`). |
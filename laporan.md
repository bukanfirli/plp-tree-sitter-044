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

### 2. Kendala & Catatan Penggunaan AI
* **Kendala:** Jika melakukan perulangan langsung pada `node.named_children`, indeks yang dihasilkan tidak cocok dengan `node.field_name_for_child(i)` karena metode tersebut menghitung indeks dari `node.children` (termasuk node anonim)[cite: 2]. **Solusi:** Melakukan iterasi pada `enumerate(node.children)` lalu memfilter dengan `if child.is_named:`[cite: 2].
* **Catatan AI:** Meminta AI menyusun kerangka fungsi rekursif `jelajah()`[cite: 2]. Diverifikasi dengan membandingkan output `kecil.py` (`x = 1`) dan file `file_besar.py` (>100 baris) terhadap struktur tree-sitter yang diharapkan[cite: 2].
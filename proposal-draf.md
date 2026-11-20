# Draf Proposal Proyek Tree-sitter
- **Nama:** Firliana Febrina
- **NIM:** 251524044
- **Kelas:** 2B D4 Teknik Informatika

---

### 1. Judul
**SQLGuard-TS: Tool Analisis Statis Berbasis Tree-sitter untuk Mendeteksi Potensi SQL Injection pada Backend Web TypeScript/JavaScript**

### 2. Masalah
Dalam pengembangan aplikasi web enterprise berbasis Node.js/TypeScript (Express atau NestJS), developer sering membangun query database secara dinamis menggunakan *template literal* (`SELECT * FROM users WHERE id = ${req.params.id}`) atau penggabungan string (`+`) alih-alih *parameterized query*. Celah SQL injection ini sering lolos saat *code review* manual ketika basis kode sudah mencapai ratusan file. Pendekatan pencarian teks biasa (`grep`/regex) tidak efektif karena menghasilkan banyak *false positive* pada template string biasa yang bukan pemanggilan query database.

### 3. Kenapa Tidak Cukup dengan AI Saja
Meminta AI coding agent memeriksa setiap file atau pull request secara berulang membutuhkan biaya token yang besar pada proyek enterprise, berisiko tidak konsisten (probabilistik) antar-eksekusi, dan terlalu lambat untuk dijalankan di setiap `git commit` atau pipeline CI/CD. Tool berbasis tree-sitter bersifat deterministik, memproses ribuan file dalam hitungan detik tanpa biaya API, dan menjamin aturan keamanan tim selalu ditegakkan secara konsisten sebelum kode di-merge.

### 4. Bahasa dan Framework Target
- **Bahasa & Framework:** TypeScript / JavaScript (Node.js, Express, NestJS, Prisma/raw `pg`/`mysql2`).
- **Grammar Tree-sitter:** `tree-sitter-typescript` (untuk file `.ts`/`.tsx`) dan `tree-sitter-javascript` (untuk file `.js`).

### 5. Contoh Kode Target
- **Harus Terdeteksi (Rentan SQL Injection):**
  ```typescript
  const user = await db.query(`SELECT * FROM users WHERE email = '${req.body.email}'`);
  const orders = await pool.query("SELECT * FROM orders WHERE status = " + status);
  ```
- **Tidak Boleh Terdeteksi (Aman / Parameterized Query & Non-SQL):**
  ```typescript
  const user = await db.query("SELECT * FROM users WHERE email = $1", [req.body.email]);
  const msg = `Halo ${user.name}, selamat datang!`;
  ```

### 6. Rancangan Query (S-Expression)
```scheme
(call_expression
  function: (member_expression
    property: (property_identifier) @method
    (#match? @method "^(query|execute)$"))
  arguments: (arguments
    [
      (template_string
        (template_substitution)) @unsafe_query
      (binary_expression
        operator: "+") @unsafe_query
    ]))
```

### 7. Bentuk Output
Laporan CLI di terminal dan file JSON (`sqlguard-report.json`) berisi path file, nomor baris, nama method pemanggil, serta cuplikan ekspresi query berisiko, dengan exit code `1` jika ditemukan pelanggaran agar dapat memblokir pipeline CI.

### 8. Cara Evaluasi
Pengujian dilakukan pada minimal 2 repositori backend Express/TypeScript open source di GitHub serta 1 dataset kasus uji sintetis (berisi 15 kasus rentan dan 15 kasus aman). Hasil deteksi tool akan diverifikasi secara manual pada 20 sampel temuan untuk menghitung *precision* dan memastikan nol *false positive* pada parameterized query.

### 9. Rencana Kerja & Risiko
- **Minggu 1:** Finalisasi desain arsitektur, penyusunan dataset kasus uji (`.ts`/`.js`), dan eksplorasi struktur node `template_string` & `binary_expression` dengan tree-sitter.
- **Minggu 2:** Implementasi parser dan query deteksi SQL injection serta dukungan *parameterized query* whitelist.
- **Minggu 3:** Penambahan fitur output JSON, integrasi CLI, dan pengujian pada repositori backend open source nyata.
- **Minggu 4:** Evaluasi akurasi manual, perbaikan edge-case (query multi-baris/variabel terpisah), dan penyusunan laporan akhir.
- **Risiko & Mitigasi:** Query SQL yang dirakit di variabel terpisah sebelum masuk ke `db.query(sql)` mungkin terlewat oleh query AST tunggal; dimitigasi dengan melacak assignment variabel string SQL dalam lingkup fungsi yang sama.
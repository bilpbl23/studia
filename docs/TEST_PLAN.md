# Rencana dan Hasil Pengujian

Status: **revisi status kalender, agenda, aksesibilitas, dan label UI diuji lokal
pada 2026-10-14.**

## Otomatis

`python -m unittest discover -s tests -v` — **12 tes lulus**.

| Skenario | Hasil |
|---|---|
| Route Flask, aset lokal, dan referensi output GitHub Pages | Lulus |
| Penyimpanan lokal, riwayat aktual, dan payload cadangan | Lulus |
| Intro, checklist, tur panduan, dan Tutorial permanen | Lulus |
| Navigasi Classroom tidak ada; Pengingat tetap ada | Lulus |
| Pemisahan Data Demo dan perlindungan tugas pribadi | Lulus |
| Kalender Senin–Minggu, tanggal lokal, dan pemformatan tanggal | Lulus |
| Penanda deadline mendatang, hari ini, terlambat, dan selesai | Lulus |
| Agenda kosong, tanggal terpilih, aksesibilitas label, dan aksi tambah | Lulus |
| Label Indonesia dan cakupan CSV/cadangan/pemulihan | Lulus |
| Kontrol suara mandiri dihapus | Lulus |

Kompilasi `py_compile` untuk aplikasi dan tes serta `git diff --check` lulus.
Analisis editor tidak melaporkan masalah pada `studia.py` maupun `studia.js`.

## Smoke test browser lokal

Pengujian dilakukan pada instance lokal terisolasi di port 5004 menggunakan
penyimpanan browser khusus untuk data QA.

- Dashboard menggabungkan lima tugas pribadi dan satu Data Demo dengan benar:
  5 aktif, 1 selesai, 1 terlambat, dan 17% selesai. Data demo memiliki banner
  serta key penyimpanan terpisah; pemuatan ulang tidak menggandakan tugas.
- Kelas kalender serta label pembaca layar membedakan status mendatang, hari ini,
  terlambat, dan selesai. Keempat warna penanda terhitung berbeda.
- Pemilihan tanggal menampilkan dua tugas pada hari yang sama, nama hari dan
  tanggal lengkap, waktu setempat, kepentingan, serta status.
- Menandai tugas selesai memperbarui statistik dan agenda. Mengubah tenggat
  memindahkan tugas ke tanggal baru; menghapus tugas menghapus hanya tugas itu.
  Setelah muat ulang, data tersimpan konsisten.
- Agenda kosong menyediakan tombol tambah tugas; formulir memakai tanggal
  terpilih pukul 09.00 sebagai nilai awal.
- Dialog tugas mengunci fokus keyboard, mendukung Escape, dan mengembalikan fokus.
  Menu mobile mengumumkan statusnya melalui `aria-expanded`.
- Kalender sesuai untuk Februari 2028 (29 hari), Februari 2027 (28), April 2026
  (30), Mei 2026 (31), dan Desember 2026; setiap tanggal 1 berada pada kolom
  hari yang tepat. Navigasi Desember 2026 ke Januari 2027 berfungsi.
- Pada lebar 390px (dokumen 375px) dan 1440px (dokumen 1425px), tidak ada
  overflow horizontal. Classroom tidak muncul. Tidak ada error JavaScript
  ketika halaman dimuat ulang dan skenario utama dijalankan.
- Menghapus Data Demo mempertahankan seluruh tugas pribadi dalam penyimpanan.
  Data pengujian lokal dibersihkan setelah smoke test; data situs live tidak
  disentuh.

## Deployment

Workflow `.github/workflows/pages.yml` menjalankan suite Python sebelum menyusun
`_site/index.html` dari `studia.py` dan menyalin aset `static/`. Status publish
untuk perubahan baru harus diverifikasi setelah push dan workflow selesai.

Repository tidak menunjukkan konfigurasi Vercel yang membuktikan bahwa project
production terkait dengan repository ini; deployment Vercel tidak diubah.

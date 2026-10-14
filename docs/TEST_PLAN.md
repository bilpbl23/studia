# Rencana dan Hasil Pengujian

Status: **revisi navigasi, Data Demo, dan kalender diuji lokal pada 2026-10-14.**

## Otomatis (Python `unittest`)

`python -m unittest discover -s tests -v` — **10 tes lulus**.

| Skenario | Hasil |
|---|---|
| Route Flask, aset lokal, dan struktur output GitHub Pages | Lulus |
| Penyimpanan lokal, riwayat aktual, dan payload cadangan | Lulus |
| Intro, checklist, tur panduan, dan Tutorial permanen | Lulus |
| Navigasi Classroom tidak ada; Pengingat tetap ada | Lulus |
| Demo memakai key terpisah dan mekanisme muat/hapus yang mempertahankan tugas pribadi | Lulus |
| Kalender berorientasi Senin, memakai tanggal lokal, dan format tanggal lengkap | Lulus |
| Kontrol suara mandiri dihapus | Lulus |

`py_compile` untuk aplikasi dan tes serta `git diff --check` juga lulus.

## Smoke test browser lokal

- Tidak ada teks, tautan, atau navigasi Classroom pada UI; Pengingat tersedia.
- Data uji tugas pribadi tetap di `studia_tasks_v1`. Memuat enam tugas demo
  menyimpan data tersebut terpisah di `studia_demo_tasks_v1`; dashboard dan
  Monitoring menghitung 7 total, 6 aktif, 1 selesai, 1 terlambat, 14% selesai.
- Reload mempertahankan enam demo tanpa duplikasi. Migrasi satu contoh lama dari
  penyimpanan utama memindahkannya ke key demo dan mempertahankan tugas pribadi.
- Menghapus Data Demo menyisakan tugas pribadi identik, mengosongkan key demo,
  dan tetap demikian setelah reload.
- Statistik cocok dengan status dan deadline aktual; agenda yang dipilih
  menampilkan tugas, nama hari/tanggal penuh, mata kuliah, prioritas, status,
  keterangan, dan jam setempat.
- Kalender diuji untuk Februari 2028 (29 hari), Februari 2027 (28), April 2026
  (30), dan Mei 2026 (31); hari pertama berada di kolom yang benar dengan
  pekan Senin–Minggu.
- Tombol bulan maju/mundur memperbarui bulan dan tanggal pilihan. Penanda
  deadline, tanggal hari ini, agenda kosong, serta detail agenda diuji.
- Viewport 390px tidak mengalami horizontal overflow (dokumen 375px). CSS/JS v7
  dimuat tanpa page error atau request gagal.

Data smoke test dibuat hanya pada origin lokal port 5003 dan dihapus setelah
pengujian; tidak ada perubahan pada data browser live.

## Deployment

Status publish diverifikasi setelah push, bukan sebagai bagian dari pengujian
lokal. Workflow GitHub Pages dan versi production perlu diperiksa untuk setiap
commit baru. Repository tidak menunjukkan konfigurasi Vercel yang membuktikan
deployment production terkait dengan proyek ini.

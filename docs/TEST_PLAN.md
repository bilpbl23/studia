# Rencana dan Hasil Pengujian

Status: **validasi onboarding lokal dijalankan pada 2026-10-14.**

## Otomatis (Python `unittest`)

| Skenario | Hasil |
|---|---|
| Route `/` mengirim HTML dengan referensi aset lokal | Lulus |
| Route Flask melayani stylesheet dan JavaScript | Lulus |
| Semua aset yang direferensikan ada pada struktur output Pages | Lulus |
| Source memakai penyimpanan lokal dan event historis, tanpa grafik progres sintetis | Lulus |
| Fixture pemulihan memiliki payload backup berversi | Lulus |
| Intro, checklist, tur, dan halaman Tutorial disediakan | Lulus |
| Kontrol suara mandiri dihapus dari UI dan runtime | Lulus |

Perintah: `python -m unittest discover -s tests -v` — **7 tes lulus**.
`py_compile`, build struktur Pages lokal, dan `git diff --check` juga lulus.
Node.js tidak tersedia untuk `node --check`; browser Chromium berhasil memuat dan
menjalankan JavaScript tanpa page error.

## Smoke test browser

- First run kosong menampilkan intro dan empat checklist belum selesai; melewati
  intro membuka dashboard, dan intro tidak muncul lagi setelah state tersimpan —
  **lulus**.
- Tombol Mulai Perjalanan membuka tur enam langkah. Setiap langkah membuka view
  yang sesuai, menyorot target, dan menyediakan navigasi; Finish menandai tour
  selesai — **lulus**.
- Tutorial permanen memuat tujuh panduan fitur; intro dapat diputar ulang lalu
  dilewati tanpa menghapus tugas — **lulus**.
- Finish tur dari intro dan mulai/lewati tur dari Tutorial mengakhiri overlay
  tanpa error; fokus kembali ke heading dashboard yang terlihat — **lulus**.
- Membuat tugas melalui checklist menyimpan judul dan deadline, memperbarui jumlah
  tugas, serta menandai langkah tugas/deadline selesai — **lulus**.
- Tugas smoke test tampil di My Tasks dan agenda tanggal deadline, tetap tersimpan
  setelah reload, lalu dihapus melalui UI agar tidak meninggalkan data uji —
  **lulus**.
- Data contoh tidak menandai pembuatan tugas pengguna sebagai selesai — **lulus**.
- Checklist dapat diciutkan; membuka Schedule menandai langkah kalender selesai.
  Navigasi bulan maju/mundur juga menampilkan bulan yang benar — **lulus**.
- Aplikasi berhasil memakai SessionStorage saat akses LocalStorage onboarding
  disimulasikan gagal — **lulus**; warning console pada simulasi ini diharapkan.
- Navigasi Tasks, Schedule, Monitoring, Classroom, Pengingat, Tutorial, dan
  Dashboard berfungsi — **lulus**.
- Focus Timer dapat dikaitkan dengan tugas, mulai, jeda, dan reset — **lulus**.
- Viewport mobile 390px memiliki lebar dokumen 375px tanpa horizontal overflow;
  aset v6 berhasil dimuat, tanpa request gagal atau page error — **lulus**.
- Ekspor CSV dan pemeriksaan console untuk seluruh alur aplikasi — **belum diuji**.

GitHub Pages untuk perubahan onboarding, Vercel, dan smoke test pada production
versi baru menunggu commit/push berikutnya. Pemeriksaan repo tidak menemukan
konfigurasi atau deployment record Vercel untuk project ini.

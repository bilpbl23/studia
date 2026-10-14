# Rencana dan Hasil Pengujian

Status: **tes otomatis dan smoke test lokal dijalankan pada 2026-10-14.**

## Otomatis (Python `unittest`)

| Skenario | Hasil |
|---|---|
| Route `/` mengirim HTML dengan referensi aset lokal | Lulus |
| Route Flask melayani stylesheet dan JavaScript | Lulus |
| Semua aset yang direferensikan ada pada struktur output Pages | Lulus |
| Source memakai penyimpanan lokal dan event historis, tanpa grafik progres sintetis | Lulus |
| Fixture pemulihan memiliki payload backup berversi | Lulus |

Perintah: `python -m unittest discover -s tests -v` — **5 tes lulus**.
`py_compile`, build struktur Pages lokal, dan `git diff --check` juga lulus.

## Smoke test browser

- First run tanpa data menunjukkan empty state, bukan data demo otomatis — **lulus**.
- Tambah, edit, filter, selesaikan, buka kembali, dan hapus tugas; data tetap ada setelah reload — **lulus**.
- Ringkasan dashboard/kalender dan grafik mengikuti data tugas dan event penyelesaian — **lulus**.
- Timer start, pause, resume, reset; sesi yang berakhir saat reload hanya tercatat sekali — **lulus**.
- Ekspor JSON dan impor backup dengan konfirmasi; fixture memulihkan tugas, sesi, dan pengaturan — **lulus**.
- Layout mobile pada viewport 390px tidak memiliki horizontal overflow; menu navigasi diuji — **lulus**.
- Simulasi kegagalan penulisan storage: peringatan dan tombol pemulihan muncul, data tersimpan sebelumnya tetap utuh setelah reload — **lulus**.
- Migrasi data tugas legacy — **lulus**.
- Ekspor CSV dan pemeriksaan console untuk alur utama — **belum diuji**. Simulasi quota sengaja menghasilkan log error rollback yang diharapkan.

Workflow GitHub Actions, publikasi, dan URL live tetap **belum diverifikasi**;
build lokal tidak membuktikan deployment berhasil.

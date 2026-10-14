# Changelog

## 2026-10-14 — Data demo aman dan kalender deadline

- Menghapus Classroom dari navigasi, halaman, dan tutorial tanpa mengubah fitur
  Pengingat.
- Memisahkan Data Demo dari tugas pribadi, memberi penanda pada demo, dan
  menyediakan aksi muat/hapus tanpa mengganti data pribadi.
- Mengonversi contoh demo lama dari daftar tugas utama ke penyimpanan demo
  terpisah, serta mengecualikan demo dari cadangan JSON.
- Menyelaraskan kalender agar dimulai Senin, menyorot tenggat dan status selesai,
  serta menampilkan tanggal lengkap berbahasa Indonesia di agenda dan detail.
- Menghitung kalender menurut tanggal lokal dan memperbarui pilihan agenda saat
  pengguna berpindah bulan.

## 2026-10-14 — Guided onboarding

- Menambahkan intro first-run singkat yang dapat dilewati, diputar ulang, dan
  mengikuti preferensi reduced motion tanpa menunda akses ke aplikasi.
- Menambahkan tur enam langkah dengan highlight pada halaman dan kontrol nyata,
  dukungan keyboard, serta aksi untuk melewati atau menyelesaikannya.
- Menambahkan checklist dashboard yang memakai tugas pengguna, kunjungan Schedule,
  dan penyelesaian tur sebagai kriteria aktual.
- Menambahkan Tutorial permanen yang menjelaskan Pengingat deadline secara
  akurat; label Messages yang menyerupai chat diganti menjadi Pengingat.
- Menghapus kontrol dan efek suara mandiri tanpa mengubah tugas, timer, maupun
  riwayat tersimpan; backup lama dengan field suara tetap dapat diimpor.

## 2026-10-14

- Memisahkan stylesheet dan JavaScript ke aset statis, serta menyertakannya dalam
  artefak GitHub Pages.
- Memulai instalasi baru dengan dashboard kosong; data contoh hanya dimuat atas
  permintaan dan diberi label.
- Menambahkan ringkasan tugas hari ini dan prioritas terdekat.
- Mengganti grafik progres sintetis dengan hitungan penyelesaian berdasarkan
  riwayat status yang tercatat sejak fitur ini tersedia.
- Mencatat waktu pembuatan/perubahan/penyelesaian tugas dan mencegah sesi fokus
  yang sama dicatat lebih dari sekali.
- Menambahkan ekspor/impor cadangan JSON dan peringatan eksplisit saat data lokal
  tidak dapat dibaca atau disimpan.
- Memperjelas bahwa pengingat hanya aktif saat halaman Studia dibuka dan
  memperhatikan preferensi reduced motion.
- Menambahkan pemeriksaan Python untuk route Flask, aset statis, dan referensi
  artefak Pages.

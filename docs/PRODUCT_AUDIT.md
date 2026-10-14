# Audit Produk Studia

## Kondisi awal

- Source of truth berada di `studia.py` pada repository `studia`; route Flask
  mengirim satu dokumen HTML dan CSS/JavaScript masih inline.
- Workflow GitHub Pages mengimpor konstanta `HTML` dari `studia.py` dan menulis
  `_site/index.html`. Folder `_site` diabaikan Git.
- Fitur utama menggunakan `localStorage`; tidak ditemukan database, API produk,
  akun, atau sinkronisasi antarperangkat.
- First run sebelumnya memasukkan empat tugas contoh secara otomatis.
- Grafik Academic Performance membentuk titik berdasarkan persentase selesai saat
  ini, sehingga tampak historis walau tidak ada rekaman historis.
- Timer menyimpan deadline sesi absolut dan menghitung sisa waktu dari jam sistem,
  tetapi riwayat fokus tidak menampilkan beberapa sesi terakhir.
- Notifikasi merupakan indikator dan dialog di dalam halaman, bukan browser atau
  notifikasi latar belakang.
- Tidak ada test suite pada repository sebelum perubahan ini.

## Risiko dan keputusan

- Data rusak sebelumnya dapat berubah menjadi daftar kosong di memori tanpa pesan
  yang jelas; perubahan berikutnya berisiko menimpa data tersimpan.
- Penyimpanan hanya berupa data browser, sehingga tidak otomatis tersedia di
  perangkat/browser lain.
- Aset inline mempersulit pemeliharaan dan pengujian; CSS dan JavaScript kini
  dipisah di `static/`, dan workflow menyalin aset yang sama ke artefak Pages.
- Data tugas legacy dimuat dengan metadata waktu kosong; tanggal pembuatan atau
  penyelesaian masa lalu tidak direka ulang.
- Grafik baru menghitung event penyelesaian tersimpan selama 28 hari. Riwayat
  dimulai saat event baru dicatat; tugas lama tidak menyumbang titik historis.
- Perubahan atau kegagalan localStorage menampilkan peringatan serta jalur untuk
  mengunduh data mentah/memulai ulang setelah konfirmasi.

## Implementasi prioritas

1. Pertahankan data lama dengan normalisasi kompatibel dan versi skema lokal.
2. Jadikan first run kosong; muat data contoh hanya atas permintaan dengan label.
3. Tampilkan tugas jatuh tempo hari ini dan prioritas aktif berikutnya.
4. Rekam event pembuatan/penyelesaian/pembukaan kembali serta timestamp tugas.
5. Beri ID sesi timer yang stabil agar penyelesaian yang sama bersifat idempoten.
6. Sediakan ekspor/impor JSON yang divalidasi dan konfirmasi sebelum mengganti data.
7. Uji route, asset statis, dan build Pages; lakukan smoke test browser terpisah.

## Batas audit

Audit deployment live memerlukan status GitHub Actions dan pemeriksaan URL yang
berhasil. Build lokal atau commit/push saja tidak membuktikan website produksi
telah diperbarui.

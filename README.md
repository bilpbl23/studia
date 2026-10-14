# Studia

Dashboard akademik untuk mengatur tugas kuliah, tenggat waktu, agenda, dan sesi
belajar. Studia berjalan seluruhnya di browser; data tugas dan preferensi disimpan
di penyimpanan lokal browser dan tidak tersinkron otomatis antarperangkat.

## Buka Studia

Website publik: **https://bilpbl23.github.io/studia/**

GitHub Pages diperbarui otomatis setiap ada perubahan pada branch `main`. Jika
website baru saja diaktifkan, tunggu workflow **Deploy Studia to GitHub Pages**
selesai di tab **Actions**.

## Fitur

- Dashboard progres dengan ringkasan tugas, aktivitas tenggat, dan grafik.
- Kalender tenggat Senin–Minggu dengan penanda tugas mendatang, hari ini,
  terlambat, dan selesai; agenda memuat nama hari, tanggal, waktu, status, serta
  prioritas tugas. Agenda kosong menyediakan aksi untuk menambah tugas pada
  tanggal pilihan.
- Tambah, edit, hapus, cari, filter, urutkan, dan ekspor tugas ke CSV.
- Cadangan dan pemulihan data lokal dalam format JSON.
- Timer Fokus dengan sesi istirahat, riwayat, dan atribusi tugas.
- Grafik penyelesaian berbasis riwayat perubahan status yang benar-benar tercatat.
- Intro kunjungan pertama yang dapat dilewati, tur interaktif, daftar langkah awal, dan
  Tutorial permanen.
- Pengingat tenggat di dalam aplikasi saat halaman dibuka dan pemberitahuan status.
- Tampilan responsif untuk layar komputer dan ponsel.
- Data Demo akademik yang ditandai jelas, tersimpan terpisah, dan dapat dihapus
  tanpa mengubah tugas pribadi.

Riwayat aktivitas baru mulai direkam setelah versi yang mendukungnya digunakan.
Tugas lama tetap dimuat, tetapi tidak dipakai untuk merekonstruksi grafik historis.
Pengingat bukan notifikasi peramban dan tidak berjalan saat website ditutup.
Tugas demo tidak dicampur ke penyimpanan tugas pribadi; ekspor cadangan hanya
memuat data pribadi, sementara CSV menandai sumber setiap tugas.
Untuk presentasi, pilih **Muat Data Demo** dari sidebar atau Tutorial; saat aktif,
banner Data Demo menyediakan **Hapus Data Demo** tanpa mengubah tugas pribadi.
Data kalender, statistik, prioritas, agenda, dan tugas demo memakai sumber yang
sama. **Unduh Daftar Tugas** membuat CSV dari seluruh daftar (dengan kolom sumber),
sedangkan **Simpan Salinan Data** hanya memuat tugas pribadi. **Pulihkan dari File
Cadangan** mengganti tugas pribadi dan riwayat, tetapi mempertahankan Data Demo;
aplikasi meminta konfirmasi sebelum mengganti data.
Efek suara yang berdiri sendiri telah dihapus. Intro berlangsung setelah pengguna
membuka Studia, tanpa memutar audio secara otomatis.

## Pengembangan dan pemeriksaan

Source frontend berada di `static/studia.css` dan `static/studia.js`; Flask
menyajikan file tersebut untuk penggunaan lokal maupun Vercel melalui entrypoint
`app.py`. Workflow Pages tetap menyalin HTML yang sama bersama aset ke `_site/`.

Jalankan pemeriksaan:

```powershell
python -m unittest discover -s tests -v
```

## Jalankan secara lokal (opsional)

Python 3.10 atau lebih baru:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python studia.py
```

Buka URL lokal yang ditampilkan di terminal. Website GitHub Pages tidak
memerlukan Python, instalasi, atau akun GitHub untuk digunakan.

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
- Kalender, agenda per tanggal, dan daftar mata kuliah.
- Tambah, edit, hapus, cari, filter, urutkan, dan ekspor tugas ke CSV.
- Cadangan dan pemulihan data lokal dalam format JSON.
- Focus Timer Pomodoro dengan sesi istirahat, riwayat, dan atribusi tugas.
- Grafik penyelesaian berbasis riwayat perubahan status yang benar-benar tercatat.
- Pengingat di dalam aplikasi saat halaman dibuka, toast, dan efek suara opsional.
- Layout responsif untuk layar komputer dan ponsel.

Riwayat aktivitas baru mulai direkam setelah versi yang mendukungnya digunakan.
Tugas lama tetap dimuat, tetapi tidak dipakai untuk merekonstruksi grafik historis.
Pengingat bukan browser notification dan tidak berjalan saat website ditutup.

## Pengembangan dan pemeriksaan

Source frontend berada di `static/studia.css` dan `static/studia.js`; Flask
menyajikan file tersebut untuk penggunaan lokal. Workflow Pages menyalin aset yang
sama bersama `index.html` ke `_site/`.

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

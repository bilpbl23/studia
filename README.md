# Studia

Dashboard akademik untuk mengatur tugas kuliah, tenggat waktu, agenda, dan sesi
belajar. Studia berjalan seluruhnya di browser; data tugas dan preferensi disimpan
di local storage masing-masing pengguna.

## Buka Studia

Website publik: **https://bilpbl23.github.io/studia/**

GitHub Pages diperbarui otomatis setiap ada perubahan pada branch `main`. Jika
website baru saja diaktifkan, tunggu workflow **Deploy Studia to GitHub Pages**
selesai di tab **Actions**.

## Fitur

- Dashboard progres dengan ringkasan tugas, aktivitas tenggat, dan grafik.
- Kalender, agenda per tanggal, dan daftar mata kuliah.
- Tambah, edit, hapus, cari, filter, urutkan, dan ekspor tugas ke CSV.
- Focus Timer Pomodoro dengan sesi istirahat dan riwayat waktu fokus.
- Pengingat popup, toast, serta efek suara yang bisa dinyalakan atau dimatikan.
- Layout responsif untuk layar komputer dan ponsel.

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

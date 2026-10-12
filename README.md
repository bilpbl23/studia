# Studia

Studia adalah dashboard akademik berbasis Flask untuk mengelola tugas kuliah,
deadline, agenda, waktu fokus, dan panduan belajar dengan Gemini AI.

## Fitur

- Dashboard progres, kalender, agenda deadline, dan mata kuliah.
- Pengelolaan tugas dengan prioritas, filter, pengurutan, dan ekspor CSV.
- Focus Timer Pomodoro dengan jeda dan riwayat sesi lokal.
- Notifikasi popup, toast, dan efek suara yang dapat diatur.
- Studia AI Guide menggunakan Gemini; API key disimpan di environment server,
  bukan di source code atau browser.

## Menjalankan di Windows

Python 3.10 atau lebih baru disarankan.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Gemini AI bersifat opsional. Untuk mengaktifkannya, buat API key melalui
[Google AI Studio](https://aistudio.google.com/app/apikey), lalu atur key hanya
di terminal yang akan menjalankan aplikasi:

```powershell
$env:GEMINI_API_KEY="API_KEY_KAMU"
```

Jangan masukkan API key ke source code atau commit ke GitHub.

Jalankan aplikasi:

```powershell
$env:STUDIA_PORT="5001"
python studia.py
```

Buka `http://127.0.0.1:5001` di browser. Jika `STUDIA_PORT` tidak diatur,
aplikasi memakai port `5001`.

## Catatan

Data tugas dan pengaturan browser disimpan di local storage browser pengguna.
Endpoint Gemini berjalan melalui server Flask. Jangan publikasikan API key,
data tugas pribadi, file `.env`, atau kredensial lain.

Repository GitHub publik membagikan **kode sumber**, bukan menjalankan aplikasi
sebagai website publik. GitHub Pages tidak menjalankan aplikasi Flask; untuk
membuka Studia sebagai website, deploy ke layanan hosting yang mendukung Flask
dan atur `GEMINI_API_KEY` sebagai secret/environment variable di layanan itu.

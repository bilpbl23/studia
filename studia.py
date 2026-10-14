
import os

from flask import Flask

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studia | Ruang Kerja Akademik</title>
<link rel="stylesheet" href="static/studia.css?v=8">
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar">
 <div class="brand">Studia<span>.</span><small>RUANG KERJA AKADEMIK</small></div>
 <div class="nav-label">MENU UTAMA</div>
 <button class="nav active" data-view="dashboard" aria-current="page"><span class="ico">⌂</span>Dashboard</button>
 <button class="nav" data-view="tasks"><span class="ico">▤</span>Tugas Saya<span class="count" id="navPending">0</span></button>
 <button class="nav" data-view="schedule"><span class="ico">▦</span>Jadwal</button>
 <button class="nav" data-view="monitoring"><span class="ico">◉</span>Progres</button>
 <button class="nav" data-view="tutorial"><span class="ico">?</span>Tutorial</button>
 <button class="nav" data-view="messages"><span class="ico">✉</span>Pengingat</button>
 <div class="sidebar-bottom">
  <button class="nav" id="sampleBtn"><span class="ico">✦</span>Muat Data Demo</button>
  <button class="nav" id="removeDemoBtn" hidden><span class="ico">×</span>Hapus Data Demo</button>
  <div class="upgrade"><strong>Belajar lebih terarah.</strong>
   <p>Atur tugas, tenggat, dan waktu belajarmu di satu tempat.</p>
   <span class="pill">UNTUK MAHASISWA</span>
  </div>
 </div>
</aside>

<main class="main">
 <div class="storage-notice" id="storageNotice" role="alert">
  <p id="storageNoticeText"></p>
  <div class="task-row-actions">
   <button class="btn small" id="downloadRecoveryBtn" hidden>Unduh salinan</button>
   <button class="btn small" id="resetStorageBtn" hidden>Mulai baru</button>
  </div>
 </div>
 <div class="topbar">
  <button class="icon-btn mobile-menu" id="menuBtn" aria-label="Menu" aria-controls="sidebar" aria-expanded="false">☰</button>
  <div class="search"><input id="globalSearch" placeholder="Cari tugas atau mata kuliah..." aria-label="Cari tugas"></div>
  <div class="top-actions">
   <button class="icon-btn" title="Buka jadwal" aria-label="Buka jadwal" onclick="navigate('schedule')">♧</button>
   <button class="icon-btn notification-trigger" id="notificationBtn" title="Buka notifikasi" aria-label="Buka notifikasi" aria-haspopup="dialog" aria-expanded="false" aria-controls="notificationModal">♢<span class="notification-dot" id="notificationDot"></span></button>
   <div class="avatar" title="Mahasiswa">S</div>
  </div>
 </div>

 <section class="view active" id="view-dashboard">
  <header class="heading">
   <div><div class="eyebrow">STUDIA · RUANG KERJA AKADEMIK</div>
    <h1 tabindex="-1">Selamat datang di Studia.</h1>
    <div class="muted" style="font-size:12px">Satu tempat untuk mengatur perkembangan dan aktivitas kuliahmu.</div>
    <div class="sub" id="today"></div>
   </div>
   <button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button>
  </header>

  <section class="demo-banner" id="demoBanner" aria-label="Mode data demo" hidden>
   <span class="pill gray">DATA DEMO</span>
   <span>Contoh tugas terpisah dari data pribadimu dan hanya tersimpan di browser ini.</span>
   <button class="btn small" id="removeDemoBannerBtn">Hapus Data Demo</button>
  </section>

  <section class="card onboarding-card" id="onboardingChecklist" aria-labelledby="onboardingTitle" hidden>
   <div class="card-head">
    <div><div class="eyebrow">MULAI DENGAN LANGKAH SEDERHANA</div><h2 id="onboardingTitle">Mulai dari Sini</h2><div class="sub" id="onboardingSummary">Kenali ruang kerja dan siapkan rencana kuliahmu.</div></div>
    <div class="onboarding-actions"><button class="btn small" id="checklistCollapseBtn" aria-expanded="true" aria-controls="onboardingSteps">Ciutkan</button><button class="icon-btn" id="checklistDismissBtn" aria-label="Sembunyikan checklist" title="Sembunyikan checklist">×</button></div>
   </div>
   <ol class="onboarding-steps" id="onboardingSteps"></ol>
  </section>

  <div class="stats">
   <div class="card"><div class="stat-top"><span class="stat-icon">◉</span><span class="trend">AKADEMIK</span></div><div class="stat-label">Tugas Selesai</div><div class="stat-number" id="completionStat">0%</div><div class="stat-foot">Persentase tugas yang selesai</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">▤</span><span class="trend">TUGAS</span></div><div class="stat-label">Tugas Aktif</div><div class="stat-number" id="activeStat">0</div><div class="stat-foot">Tugas yang belum selesai</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">✓</span><span class="trend">PROGRES</span></div><div class="stat-label">Selesai</div><div class="stat-number" id="doneStat">0</div><div class="stat-foot">Tugas yang sudah kamu selesaikan</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">◷</span><span class="trend">TENGGAT</span></div><div class="stat-label">Tugas Terlambat</div><div class="stat-number" id="lateStat">0</div><div class="stat-foot">Tugas belum selesai dengan tenggat terlewat</div></div>
  </div>

  <section class="today-brief" aria-label="Ringkasan hari ini">
   <article class="today-panel"><h2>Tenggat hari ini <span class="pill" id="todayCount">0</span></h2><div class="sub" id="todayTasksIntro">Belum ada tugas dengan tenggat hari ini.</div><div class="today-list" id="todayTasksList"></div></article>
   <article class="today-panel"><h2>Prioritas berikutnya</h2><div class="sub" id="nextDeadlineIntro">Tambahkan tugas untuk melihat tenggat terdekat.</div><div class="today-list" id="nextDeadlineList"></div></article>
  </section>

  <div class="dashboard-grid">
   <div class="left-stack">
    <section class="card activity-card">
     <div class="card-head"><div><h2>Aktivitas tenggat</h2><div class="sub">Jumlah tenggat tugas · 28 hari terakhir</div></div><span class="pill">28 HARI</span></div>
     <div class="activity-grid" id="activityGrid" aria-label="Aktivitas tenggat selama empat minggu terakhir"></div>
     <div class="heat-legend"><span>4 minggu lalu</span><span id="activitySummary">0 tenggat tercatat</span><span>Hari ini</span><span class="heat-legend-scale"><span>Sedikit</span><i class="heat-cell"></i><i class="heat-cell level-1"></i><i class="heat-cell level-2"></i><i class="heat-cell level-3"></i><i class="heat-cell level-4"></i><span>Banyak</span></span></div>
    </section>
    <section class="card">
     <div class="card-head"><div><h2>Riwayat penyelesaian</h2><div class="sub">Tugas yang ditandai selesai · 28 hari terakhir</div></div><span class="pill">RIWAYAT</span></div>
     <div class="chart-wrap is-empty" id="completionChart">
      <svg viewBox="0 0 600 180" preserveAspectRatio="none" role="img" aria-label="Grafik penyelesaian tugas">
       <g stroke="#403c50" stroke-width="1">
        <line x1="35" y1="20" x2="590" y2="20"/><line x1="35" y1="60" x2="590" y2="60"/>
        <line x1="35" y1="100" x2="590" y2="100"/><line x1="35" y1="140" x2="590" y2="140"/>
       </g>
       <g fill="#a9a2bb" font-size="10">
        <text id="chartMax" x="2" y="23">0</text><text id="chartMid" x="9" y="83">0</text>
        <text x="15" y="143">0</text>
       </g>
       <path id="chartArea" d="" fill="#b38aff" opacity=".10"/>
       <path id="chartLine" d="" fill="none" stroke="#b38aff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
       <g id="chartDots"></g>
      </svg>
      <div class="chart-empty">Riwayat mulai tercatat sejak fitur ini tersedia.<br>Tugas lama tidak dihitung sebagai aktivitas historis.</div>
     </div>
     <div class="chart-labels"><span>28 hari lalu</span><span>14 hari lalu</span><span>Hari ini</span></div>
     <div class="metric-row"><span class="muted">Tingkat penyelesaian saat ini</span><strong id="chartRate">0%</strong></div>
     <div class="progress"><div id="chartProgress" style="width:0%"></div></div>
    </section>

    <section class="card">
     <div class="card-head"><div><h2>Tugas yang perlu diperhatikan</h2><div class="sub">Tugas aktif dengan prioritas tertinggi</div></div><button class="btn small" onclick="navigate('tasks')">Lihat semua →</button></div>
     <div id="assignmentList" class="assignments"></div>
    </section>

    <section class="card focus-card">
     <div class="eyebrow">SARAN BELAJAR</div>
     <h2 style="margin-top:10px">Langkah berikutnya</h2>
     <div class="sub">Studia membantu menentukan tugas yang layak diprioritaskan.</div>
     <div id="focusContent"></div>
    </section>
   </div>

   <div class="right-stack">
    <section class="card calendar">
     <div class="cal-head"><button class="icon-btn" id="prevMonth" aria-label="Bulan sebelumnya">‹</button><strong id="monthLabel"></strong><button class="icon-btn" id="nextMonth" aria-label="Bulan berikutnya">›</button></div>
     <div class="weekdays"><div>Sen</div><div>Sel</div><div>Rab</div><div>Kam</div><div>Jum</div><div>Sab</div><div>Min</div></div>
     <div class="days" id="calendarDays"></div>
     <div class="calendar-legend" aria-label="Keterangan status tenggat"><span><i class="calendar-dot upcoming"></i>Mendatang</span><span><i class="calendar-dot due-today"></i>Hari ini</span><span><i class="calendar-dot overdue"></i>Terlambat</span><span><i class="calendar-dot completed"></i>Selesai</span></div>
     <div class="agenda">
      <div class="card-head"><div><h2 id="agendaTitle">Agenda</h2><div class="sub" id="agendaSub">Pilih tanggal untuk melihat tugas.</div></div><button class="btn small" onclick="navigate('schedule')">Lihat jadwal →</button></div>
      <div id="agendaList"></div>
     </div>
    </section>
    <section class="card">
     <div class="card-head"><div><h2>Ringkasan Belajar</h2><div class="sub">Gambaran tugas dan waktu belajarmu</div></div></div>
     <div class="metric-row"><span class="muted">Tugas aktif</span><strong id="overviewActive">0</strong></div>
     <div class="progress"><div id="activeProgress" style="width:0%"></div></div>
     <div class="metric-row"><span class="muted">Tugas selesai</span><strong id="overviewDone">0</strong></div>
     <div class="progress"><div id="doneProgress" style="width:0%"></div></div>
     <div class="metric-row"><span class="muted">Total estimasi tugas aktif</span><strong id="totalTime">0 jam</strong></div>
     <div class="sub" id="studyInsight"></div>
    </section>
    <section class="card focus-timer" id="focusTimerCard">
     <div class="card-head"><div><h2>Timer Fokus</h2><div class="sub">Fokus dalam sesi singkat, lalu istirahat sejenak.</div></div><span class="pill">WAKTU FOKUS</span></div>
     <div class="timer-layout">
      <div class="timer-ring" id="timerRing" role="timer" aria-label="Timer fokus">
       <div class="timer-face"><div class="timer-time" id="timerDisplay">25:00</div><div class="timer-caption" id="timerCaption">SIAP FOKUS</div></div>
      </div>
      <div class="timer-options">
       <label class="field" style="margin:0"><span class="muted" style="font-size:10px">Durasi fokus</span><select id="timerDuration" aria-label="Durasi fokus"><option value="15">15 menit</option><option value="25" selected>25 menit</option><option value="45">45 menit</option><option value="60">60 menit</option></select></label>
       <label class="field" style="margin:0"><span class="muted" style="font-size:10px">Fokus pada tugas</span><select id="timerTask" aria-label="Pilih tugas untuk sesi fokus"><option value="">Sesi belajar bebas</option></select></label>
       <div class="timer-controls"><button class="btn primary" id="timerStartBtn">Mulai fokus</button><button class="btn" id="timerResetBtn">Atur ulang</button></div>
      </div>
     </div>
     <div class="timer-summary"><span>Total waktu fokus</span><strong id="focusTotal">0 menit · 0 sesi</strong></div>
     <div class="focus-history" id="focusHistory" aria-label="Sesi fokus terbaru"></div>
    </section>
   </div>
  </div>
 </section>

 <section class="view" id="view-tasks">
  <header class="heading"><div><div class="eyebrow">DAFTAR TUGAS</div><h1>Tugas Saya</h1><div class="muted">Atur tugas kuliah, tenggat, dan prioritasmu.</div></div><button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button></header>
  <section class="card">
   <div class="section-tools"><input id="taskSearch" placeholder="Cari tugas atau mata kuliah..." aria-label="Cari di daftar tugas" oninput="renderTasks()"><select id="taskFilter" onchange="renderTasks()" aria-label="Saring tugas"><option value="all">Semua status</option><option value="pending">Belum selesai</option><option value="completed">Selesai</option><option value="overdue">Terlambat</option></select><select id="taskSort" onchange="renderTasks()" aria-label="Urutkan tugas"><option value="priority">Prioritas tertinggi</option><option value="deadline">Tenggat terdekat</option><option value="title">Nama tugas</option></select><button class="btn small export-btn" id="exportTasksBtn" title="Unduh semua tugas yang tampil, termasuk Data Demo dengan penanda sumbernya.">↓ Unduh Daftar Tugas</button><button class="btn small export-btn" id="exportBackupBtn" title="Simpan salinan tugas pribadi dan riwayat; Data Demo tidak disertakan.">↓ Simpan Salinan Data</button><button class="btn small export-btn" id="importBackupBtn" title="Ganti tugas pribadi dari file cadangan. Data Demo tetap dipertahankan.">↑ Pulihkan dari File Cadangan</button><input id="backupFile" type="file" accept="application/json,.json" aria-label="Pilih file cadangan Studia" hidden></div>
   <div id="fullTaskList"></div>
  </section>
 </section>

 <section class="view" id="view-schedule">
  <header class="heading"><div><div class="eyebrow">JADWAL KULIAH</div><h1>Jadwal & Agenda</h1><div class="muted">Pilih tanggal untuk melihat tugas dan tenggatnya.</div></div><button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button></header>
  <div class="dashboard-grid">
   <section class="card calendar"><div class="cal-head"><button class="icon-btn" id="prevMonth2" aria-label="Bulan sebelumnya">‹</button><strong id="monthLabel2"></strong><button class="icon-btn" id="nextMonth2" aria-label="Bulan berikutnya">›</button></div><div class="weekdays"><div>Sen</div><div>Sel</div><div>Rab</div><div>Kam</div><div>Jum</div><div>Sab</div><div>Min</div></div><div class="days" id="calendarDays2"></div><div class="calendar-legend" aria-label="Keterangan status tenggat"><span><i class="calendar-dot upcoming"></i>Mendatang</span><span><i class="calendar-dot due-today"></i>Hari ini</span><span><i class="calendar-dot overdue"></i>Terlambat</span><span><i class="calendar-dot completed"></i>Selesai</span></div></section>
   <section class="card"><h2 id="scheduleDateTitle">Agenda</h2><div class="sub">Agenda pada tanggal yang dipilih.</div><div id="scheduleList" style="margin-top:15px"></div></section>
  </div>
 </section>

 <section class="view" id="view-monitoring">
  <header class="heading"><div><div class="eyebrow">PROGRES AKADEMIK</div><h1>Progres</h1><div class="muted">Pantau perkembangan tugas dan beban belajarmu.</div></div></header>
  <div class="stats">
   <div class="card"><div class="stat-label">Total Tugas</div><div class="stat-number" id="mTotal">0</div></div>
   <div class="card"><div class="stat-label">Tugas Selesai</div><div class="stat-number" id="mRate">0%</div></div>
   <div class="card"><div class="stat-label">Terlambat</div><div class="stat-number" id="mLate">0</div></div>
   <div class="card"><div class="stat-label">Estimasi Tugas Aktif</div><div class="stat-number" id="mHours">0 jam</div></div>
  </div>
  <section class="card" style="margin-top:15px"><h2>Ringkasan Progres</h2><div class="sub">Persentase dihitung dari status tugas yang tersimpan.</div><div id="monitorBars" style="margin-top:20px"></div></section>
 </section>

 <section class="view" id="view-messages">
  <header class="heading"><div><div class="eyebrow">PENGINGAT TENGGAT</div><h1>Pengingat</h1><div class="muted">Pengingat berdasarkan tenggat tugas yang tersimpan di browser ini.</div></div></header>
  <section class="card"><div id="messageList"></div></section>
 </section>

 <section class="view" id="view-tutorial">
  <header class="heading"><div><div class="eyebrow">PANDUAN STUDIA</div><h1>Tutorial</h1><div class="muted">Panduan singkat untuk fitur yang tersedia saat ini.</div></div><button class="btn" onclick="navigate('dashboard')">Kembali ke dashboard</button></header>
  <section class="card tutorial-welcome">
   <div><h2>Mulai dengan lebih percaya diri</h2><div class="sub">Tur interaktif menyorot bagian aplikasi yang sedang dijelaskan. Kamu bisa berhenti kapan saja.</div></div>
   <div class="task-row-actions"><button class="btn primary" id="restartTourBtn">Mulai tur panduan</button><button class="btn" id="replayIntroBtn">Putar intro lagi</button></div>
  </section>
  <div class="tutorial-grid">
   <article class="card tutorial-guide"><span class="pill">DASHBOARD</span><h2>Kenali ringkasan</h2><p class="sub">Dashboard merangkum jumlah dan status tugas, tenggat terdekat, aktivitas tenggat, serta agenda pada tanggal pilihan. Statistik dihitung dari tugas yang tersimpan di browser ini.</p><button class="btn small" onclick="navigate('dashboard')">Buka dashboard</button></article>
   <article class="card tutorial-guide"><span class="pill">TUGAS</span><h2>Buat tugas dan tenggat</h2><ol><li>Buka Tugas Saya atau tekan Tambah Tugas.</li><li>Isi nama tugas, mata kuliah, dan tenggat.</li><li>Pilih kepentingan dan estimasi, lalu simpan.</li></ol><p class="sub">Prioritas diurutkan dari tenggat, kepentingan, dan estimasi. Tugas tersimpan lokal pada browser ini.</p><button class="btn small" onclick="navigate('tasks');openTask()">Buat tugas</button></article>
   <article class="card tutorial-guide"><span class="pill">JADWAL</span><h2>Periksa kalender</h2><p class="sub">Jadwal menampilkan kalender dan tugas menurut tanggal tenggat. Pilih hari untuk melihat agenda; kalender dashboard memakai data tugas yang sama.</p><button class="btn small" onclick="navigate('schedule')">Buka jadwal</button></article>
   <article class="card tutorial-guide"><span class="pill">PROGRES</span><h2>Pantau progres</h2><p class="sub">Progres merangkum status aktual tugas. Tandai tugas selesai dari daftar atau agenda; grafik aktivitas hanya mencatat penyelesaian yang terjadi setelah riwayat mulai direkam.</p><button class="btn small" onclick="navigate('monitoring')">Buka progres</button></article>
   <article class="card tutorial-guide"><span class="pill">DATA DEMO</span><h2>Mode presentasi</h2><p class="sub">Muat Data Demo untuk menampilkan tugas contoh yang ditandai jelas dan disimpan terpisah dari tugas pribadimu. Hapus Data Demo kapan saja tanpa menghapus tugas pribadi.</p><button class="btn small" onclick="loadDemoData()">Muat Data Demo</button></article>
   <article class="card tutorial-guide"><span class="pill">PENGINGAT</span><h2>Pengingat tenggat</h2><p class="sub">Halaman Pengingat menampilkan pemberitahuan dari tenggat tugas yang tersimpan. Ini bukan chat, tidak mengirim pesan, dan tidak berjalan saat aplikasi ditutup.</p><button class="btn small" onclick="navigate('messages')">Buka Pengingat</button></article>
   <article class="card tutorial-guide"><span class="pill">FOKUS & DATA</span><h2>Belajar dan simpan data</h2><p class="sub">Timer Fokus dapat dikaitkan dengan tugas dan menyimpan sesi di browser. Daftar Tugas menyediakan unduhan CSV serta cadangan/pemulihan JSON agar data bisa kamu pindahkan secara manual.</p><button class="btn small" onclick="navigate('dashboard');document.getElementById('focusTimerCard').scrollIntoView({behavior:'smooth',block:'center'})">Lihat Timer Fokus</button></article>
  </div>
 </section>

 <footer>STUDIA © 2026 · KEHIDUPAN KULIAH LEBIH TERATUR</footer>
</main>
</div>

<section class="intro-overlay" id="introOverlay" aria-labelledby="introTitle" hidden>
 <div class="intro-card" role="dialog" aria-modal="true" aria-labelledby="introTitle" aria-describedby="introDescription">
  <div class="intro-orbit" aria-hidden="true"><span class="intro-mark">S<span>.</span></span></div>
  <div class="eyebrow">STUDIA · RUANG KERJA AKADEMIK</div>
  <h1 id="introTitle">Mulai perjalanan akademikmu.</h1>
  <p id="introDescription">Kelola tugas, atur tenggat, dan pantau progres akademikmu dalam satu ruang kerja yang terorganisasi.</p>
  <div class="intro-actions"><button class="btn primary" id="startJourneyBtn">Mulai Perjalanan</button><button class="btn" id="skipIntroBtn">Lewati Intro</button></div>
  <span class="intro-note">Data tugas tersimpan secara lokal di browser ini.</span>
 </div>
</section>

<div class="tour-scrim" id="tourScrim" hidden></div>
<section class="tour-card" id="tourCard" role="dialog" aria-labelledby="tourTitle" aria-describedby="tourDescription" aria-modal="false" hidden>
 <div class="tour-topline"><span class="pill" id="tourProgress" aria-live="polite" aria-atomic="true">1 dari 6</span><button class="tour-close" id="tourSkipBtn" aria-label="Lewati tur">Lewati tur ×</button></div>
 <h2 id="tourTitle" tabindex="-1"></h2><p class="sub" id="tourDescription"></p>
 <div class="tour-controls"><button class="btn" id="tourPreviousBtn">Sebelumnya</button><div><button class="btn" id="tourSkipBottomBtn">Lewati</button> <button class="btn primary" id="tourNextBtn">Berikutnya</button></div></div>
</section>

<div class="modal" id="taskModal" onclick="if(event.target===this)closeTask()">
 <div class="modal-box" role="dialog" aria-modal="true" aria-labelledby="formTitle">
  <h2 id="formTitle">Tambah Tugas</h2><div class="sub" style="margin-bottom:18px">Isi detail akademik agar prioritas dapat dihitung.</div>
  <form id="taskForm">
   <input type="hidden" id="taskId">
   <div class="form-grid">
    <div class="field full"><label for="title">Nama tugas *</label><input id="title" maxlength="100" required placeholder="Contoh: Laporan praktikum"></div>
    <div class="field full"><label for="subject">Mata kuliah *</label><input id="subject" maxlength="80" required placeholder="Contoh: Algoritma dan Pemrograman"></div>
    <div class="field"><label for="deadline">Tenggat *</label><input type="datetime-local" id="deadline" required></div>
    <div class="field"><label for="importance">Kepentingan</label><select id="importance"><option value="low">Rendah</option><option value="medium" selected>Sedang</option><option value="high">Tinggi</option></select></div>
    <div class="field"><label for="duration">Estimasi (menit) *</label><input id="duration" type="number" min="1" max="10080" value="60" required></div>
    <div class="field"><label for="description">Catatan</label><input id="description" maxlength="250" placeholder="Opsional"></div>
   </div>
   <div class="error" id="formError" role="alert" aria-live="polite"></div>
   <div class="form-actions"><button type="button" class="btn" onclick="closeTask()">Batal</button><button type="submit" class="btn primary">Simpan Tugas</button></div>
  </form>
 </div>
</div>

<div class="modal" id="notificationModal" onclick="if(event.target===this)closeNotifications()">
 <section class="modal-box popup-box" role="dialog" aria-modal="true" aria-labelledby="notificationTitle">
  <div class="popup-head"><div>  <div class="eyebrow">PENGINGAT STUDIA</div><h2 id="notificationTitle" style="margin-top:7px">Notifikasi</h2></div><button class="icon-btn" id="closeNotificationsBtn" aria-label="Tutup notifikasi">×</button></div>
  <div class="sub">Pengingat hanya ditampilkan saat Studia dibuka; tidak ada notifikasi latar belakang.</div>
  <div class="popup-list" id="notificationList"></div>
  <div class="popup-actions"><button class="btn" onclick="closeNotifications()">Tutup</button><button class="btn primary" id="allMessagesBtn">Lihat semua pengingat</button></div>
 </section>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"><span class="toast-mark" id="toastMark">✓</span><span id="toastMessage"></span></div>


<script src="static/studia.js?v=8" defer></script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML


if __name__ == "__main__":
    # Keep Studia separate from other local apps that may already use port 5000.
    # Set STUDIA_PORT to override the default while keeping debug disabled.
    app.run(host="0.0.0.0", port=int(os.environ.get("STUDIA_PORT", "5001")), debug=False)

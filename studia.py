
import os

from flask import Flask

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studia | Academic Workspace</title>
<link rel="stylesheet" href="static/studia.css?v=2">
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar">
 <div class="brand">Studia<span>.</span><small>ACADEMIC WORKSPACE</small></div>
 <div class="nav-label">GENERAL</div>
 <button class="nav active" data-view="dashboard"><span class="ico">⌂</span>Dashboard</button>
 <button class="nav" data-view="tasks"><span class="ico">▤</span>My Tasks<span class="count" id="navPending">0</span></button>
 <button class="nav" data-view="schedule"><span class="ico">▦</span>Schedule</button>
 <button class="nav" data-view="monitoring"><span class="ico">◉</span>Monitoring</button>
 <div class="nav-label">WORKSPACE</div>
 <button class="nav" data-view="classroom"><span class="ico">▣</span>Classroom</button>
 <button class="nav" data-view="messages"><span class="ico">✉</span>Messages</button>
 <div class="sidebar-bottom">
  <button class="nav" id="sampleBtn"><span class="ico">✦</span>Muat data contoh</button>
  <div class="upgrade"><strong>Study smarter.</strong>
   <p>Rencanakan pekerjaan akademikmu dengan lebih terarah bersama Studia.</p>
   <span class="pill">STUDENT EDITION</span>
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
  <button class="icon-btn mobile-menu" id="menuBtn" aria-label="Menu">☰</button>
  <div class="search"><input id="globalSearch" placeholder="Cari tugas atau mata kuliah..." aria-label="Cari tugas"></div>
  <div class="top-actions">
   <button class="icon-btn" title="Agenda" onclick="navigate('schedule')">♧</button>
   <button class="icon-btn notification-trigger" id="notificationBtn" title="Buka notifikasi" aria-label="Buka notifikasi" aria-haspopup="dialog" aria-controls="notificationModal">♢<span class="notification-dot" id="notificationDot"></span></button>
   <button class="icon-btn sound-toggle" id="soundToggle" title="Matikan efek suara" aria-label="Matikan efek suara">♫</button>
   <div class="avatar" title="Student">S</div>
  </div>
 </div>

 <section class="view active" id="view-dashboard">
  <header class="heading">
   <div><div class="eyebrow">STUDIA · YOUR ACADEMIC SPACE</div>
    <h1>Selamat datang di Studia.</h1>
    <div class="muted" style="font-size:12px">Satu tempat untuk mengatur progres dan aktivitas kuliahmu.</div>
    <div class="sub" id="today"></div>
   </div>
   <button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button>
  </header>

  <div class="stats">
   <div class="card"><div class="stat-top"><span class="stat-icon">◉</span><span class="trend">ACADEMIC</span></div><div class="stat-label">Task Completion</div><div class="stat-number" id="completionStat">0%</div><div class="stat-foot">Persentase tugas selesai</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">▤</span><span class="trend">TASKS</span></div><div class="stat-label">Active Tasks</div><div class="stat-number" id="activeStat">0</div><div class="stat-foot">Tugas belum selesai</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">✓</span><span class="trend">PROGRESS</span></div><div class="stat-label">Completed</div><div class="stat-number" id="doneStat">0</div><div class="stat-foot">Tugas yang diselesaikan</div></div>
   <div class="card"><div class="stat-top"><span class="stat-icon">◷</span><span class="trend">DEADLINE</span></div><div class="stat-label">Overdue Tasks</div><div class="stat-number" id="lateStat">0</div><div class="stat-foot">Melewati batas waktu</div></div>
  </div>

  <section class="today-brief" aria-label="Ringkasan hari ini">
   <article class="today-panel"><h2>Tenggat hari ini <span class="pill" id="todayCount">0</span></h2><div class="sub" id="todayTasksIntro">Belum ada tugas dengan tenggat hari ini.</div><div class="today-list" id="todayTasksList"></div></article>
   <article class="today-panel"><h2>Prioritas berikutnya</h2><div class="sub" id="nextDeadlineIntro">Tambahkan tugas untuk melihat tenggat terdekat.</div><div class="today-list" id="nextDeadlineList"></div></article>
  </section>

  <div class="dashboard-grid">
   <div class="left-stack">
    <section class="card activity-card">
     <div class="card-head"><div><h2>Kalender tenggat</h2><div class="sub">Jumlah deadline terjadwal · 28 hari terakhir</div></div><span class="pill">JADWAL</span></div>
     <div class="activity-grid" id="activityGrid" aria-label="Aktivitas deadline selama empat minggu terakhir"></div>
     <div class="heat-legend"><span>4 minggu lalu</span><span id="activitySummary">0 deadline tercatat</span><span>Hari ini</span><span class="heat-legend-scale"><span>Rendah</span><i class="heat-cell"></i><i class="heat-cell level-1"></i><i class="heat-cell level-2"></i><i class="heat-cell level-3"></i><i class="heat-cell level-4"></i><span>Tinggi</span></span></div>
    </section>
    <section class="card">
     <div class="card-head"><div><h2>Aktivitas penyelesaian</h2><div class="sub">Tugas yang ditandai selesai · 28 hari terakhir</div></div><span class="pill">RIWAYAT</span></div>
     <div class="chart-wrap is-empty" id="completionChart">
      <svg viewBox="0 0 600 180" preserveAspectRatio="none" role="img" aria-label="Grafik progres tugas">
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
      <div class="chart-empty">Riwayat penyelesaian mulai tercatat setelah perubahan ini.<br>Tugas lama tidak digunakan untuk membuat data historis palsu.</div>
     </div>
     <div class="chart-labels"><span>28 hari lalu</span><span>14 hari lalu</span><span>Hari ini</span></div>
     <div class="metric-row"><span class="muted">Tingkat penyelesaian saat ini</span><strong id="chartRate">0%</strong></div>
     <div class="progress"><div id="chartProgress" style="width:0%"></div></div>
    </section>

    <section class="card">
     <div class="card-head"><div><h2>Assignments</h2><div class="sub">Tugas yang perlu kamu perhatikan</div></div><button class="btn small" onclick="navigate('tasks')">View all →</button></div>
     <div id="assignmentList" class="assignments"></div>
    </section>

    <section class="card focus-card">
     <div class="eyebrow">SMART RECOMMENDATION</div>
     <h2 style="margin-top:10px">Your next move</h2>
     <div class="sub">Studia membantu menentukan tugas yang layak diprioritaskan.</div>
     <div id="focusContent"></div>
    </section>
   </div>

   <div class="right-stack">
    <section class="card calendar">
     <div class="cal-head"><button class="icon-btn" id="prevMonth" aria-label="Bulan sebelumnya">‹</button><strong id="monthLabel"></strong><button class="icon-btn" id="nextMonth" aria-label="Bulan berikutnya">›</button></div>
     <div class="weekdays"><div>Min</div><div>Sen</div><div>Sel</div><div>Rab</div><div>Kam</div><div>Jum</div><div>Sab</div></div>
     <div class="days" id="calendarDays"></div>
     <div class="agenda">
      <div class="card-head"><div><h2 id="agendaTitle">Agenda</h2><div class="sub" id="agendaSub">Pilih tanggal untuk melihat tugas.</div></div><button class="btn small" onclick="navigate('schedule')">View all</button></div>
      <div id="agendaList"></div>
     </div>
    </section>
    <section class="card">
     <div class="card-head"><div><h2>Study Overview</h2><div class="sub">Ringkasan beban akademik</div></div></div>
     <div class="metric-row"><span class="muted">Tugas aktif</span><strong id="overviewActive">0</strong></div>
     <div class="progress"><div id="activeProgress" style="width:0%"></div></div>
     <div class="metric-row"><span class="muted">Tugas selesai</span><strong id="overviewDone">0</strong></div>
     <div class="progress"><div id="doneProgress" style="width:0%"></div></div>
     <div class="metric-row"><span class="muted">Total estimasi tugas aktif</span><strong id="totalTime">0 jam</strong></div>
     <div class="sub" id="studyInsight"></div>
    </section>
    <section class="card focus-timer" id="focusTimerCard">
     <div class="card-head"><div><h2>Focus Timer</h2><div class="sub">Fokus dalam sesi singkat, istirahat dengan teratur.</div></div><span class="pill">DEEP WORK</span></div>
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
  <header class="heading"><div><div class="eyebrow">TASK MANAGEMENT</div><h1>My Tasks</h1><div class="muted">Kelola tugas, deadline, dan prioritas.</div></div><button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button></header>
  <section class="card">
   <div class="section-tools"><input id="taskSearch" placeholder="Cari tugas..." oninput="renderTasks()"><select id="taskFilter" onchange="renderTasks()" aria-label="Filter status tugas"><option value="all">Semua status</option><option value="pending">Pending</option><option value="completed">Selesai</option><option value="overdue">Terlambat</option></select><select id="taskSort" onchange="renderTasks()" aria-label="Urutkan tugas"><option value="priority">Prioritas</option><option value="deadline">Deadline terdekat</option><option value="title">Nama tugas</option></select><button class="btn small export-btn" id="exportTasksBtn">↓ Ekspor CSV</button><button class="btn small export-btn" id="exportBackupBtn">↓ Cadangkan JSON</button><button class="btn small export-btn" id="importBackupBtn">↑ Pulihkan JSON</button><input id="backupFile" type="file" accept="application/json,.json" hidden></div>
   <div id="fullTaskList"></div>
  </section>
 </section>

 <section class="view" id="view-schedule">
  <header class="heading"><div><div class="eyebrow">TIME MANAGEMENT</div><h1>Schedule & Agenda</h1><div class="muted">Lihat tugas berdasarkan tanggal deadline.</div></div><button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button></header>
  <div class="dashboard-grid">
   <section class="card calendar"><div class="cal-head"><button class="icon-btn" id="prevMonth2">‹</button><strong id="monthLabel2"></strong><button class="icon-btn" id="nextMonth2">›</button></div><div class="weekdays"><div>Min</div><div>Sen</div><div>Sel</div><div>Rab</div><div>Kam</div><div>Jum</div><div>Sab</div></div><div class="days" id="calendarDays2"></div></section>
   <section class="card"><h2 id="scheduleDateTitle">Agenda</h2><div class="sub">Agenda pada tanggal yang dipilih.</div><div id="scheduleList" style="margin-top:15px"></div></section>
  </div>
 </section>

 <section class="view" id="view-monitoring">
  <header class="heading"><div><div class="eyebrow">PERFORMANCE CENTER</div><h1>Monitoring</h1><div class="muted">Pantau progres nyata berdasarkan data tugasmu.</div></div></header>
  <div class="stats">
   <div class="card"><div class="stat-label">Total Tugas</div><div class="stat-number" id="mTotal">0</div></div>
   <div class="card"><div class="stat-label">Completion</div><div class="stat-number" id="mRate">0%</div></div>
   <div class="card"><div class="stat-label">Terlambat</div><div class="stat-number" id="mLate">0</div></div>
   <div class="card"><div class="stat-label">Estimasi Aktif</div><div class="stat-number" id="mHours">0h</div></div>
  </div>
  <section class="card" style="margin-top:15px"><h2>Progress Summary</h2><div class="sub">Persentase dihitung otomatis dari status tugas.</div><div id="monitorBars" style="margin-top:20px"></div></section>
 </section>

 <section class="view" id="view-classroom">
  <header class="heading"><div><div class="eyebrow">COURSE MANAGEMENT</div><h1>Classroom</h1><div class="muted">Daftar mata kuliah dari tugas yang sudah kamu masukkan.</div></div><button class="btn primary" onclick="openTask()">＋ Tambah Tugas</button></header>
  <div id="classroomList" class="stats"></div>
 </section>

 <section class="view" id="view-messages">
  <header class="heading"><div><div class="eyebrow">NOTIFICATIONS</div><h1>Messages</h1><div class="muted">Pengingat berdasarkan kondisi tugasmu.</div></div></header>
  <section class="card"><div id="messageList"></div></section>
 </section>

 <footer>STUDIA © 2026 · YOUR ACADEMIC LIFE, ORGANIZED.</footer>
</main>
</div>

<div class="modal" id="taskModal" onclick="if(event.target===this)closeTask()">
 <div class="modal-box" role="dialog" aria-modal="true" aria-labelledby="formTitle">
  <h2 id="formTitle">Tambah Tugas</h2><div class="sub" style="margin-bottom:18px">Isi detail akademik agar prioritas dapat dihitung.</div>
  <form id="taskForm">
   <input type="hidden" id="taskId">
   <div class="form-grid">
    <div class="field full"><label for="title">Nama tugas *</label><input id="title" maxlength="100" required placeholder="Contoh: Laporan praktikum"></div>
    <div class="field full"><label for="subject">Mata kuliah *</label><input id="subject" maxlength="80" required placeholder="Contoh: Algoritma dan Pemrograman"></div>
    <div class="field"><label for="deadline">Deadline *</label><input type="datetime-local" id="deadline" required></div>
    <div class="field"><label for="importance">Kepentingan</label><select id="importance"><option value="low">Rendah</option><option value="medium" selected>Sedang</option><option value="high">Tinggi</option></select></div>
    <div class="field"><label for="duration">Estimasi (menit) *</label><input id="duration" type="number" min="1" max="10080" value="60" required></div>
    <div class="field"><label for="description">Catatan</label><input id="description" maxlength="250" placeholder="Opsional"></div>
   </div>
   <div class="error" id="formError"></div>
   <div class="form-actions"><button type="button" class="btn" onclick="closeTask()">Batal</button><button type="submit" class="btn primary">Simpan Tugas</button></div>
  </form>
 </div>
</div>

<div class="modal" id="notificationModal" onclick="if(event.target===this)closeNotifications()">
 <section class="modal-box popup-box" role="dialog" aria-modal="true" aria-labelledby="notificationTitle">
  <div class="popup-head"><div><div class="eyebrow">STUDIA INBOX</div><h2 id="notificationTitle" style="margin-top:7px">Notifikasi</h2></div><button class="icon-btn" id="closeNotificationsBtn" aria-label="Tutup notifikasi">×</button></div>
  <div class="sub">Pengingat hanya ditampilkan saat Studia dibuka; tidak ada notifikasi latar belakang.</div>
  <div class="popup-list" id="notificationList"></div>
  <div class="popup-actions"><button class="btn" onclick="closeNotifications()">Tutup</button><button class="btn primary" id="allMessagesBtn">Lihat semua pesan</button></div>
 </section>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"><span class="toast-mark" id="toastMark">✓</span><span id="toastMessage"></span></div>


<script src="static/studia.js?v=2" defer></script>
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

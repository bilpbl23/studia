const KEY="studia_tasks_v1";
const DATA_VERSION_KEY="studia_data_version";
const DATA_VERSION=2;
const SOUND_KEY="studia_sound_enabled_v1";
const TIMER_KEY="studia_focus_timer_v1";
const STUDY_KEY="studia_focus_sessions_v1";
const ACTIVITY_KEY="studia_activity_v1";
const BACKUP_FORMAT="studia-backup";
const BACKUP_VERSION=1;
let tasks=[];
let activityEvents=[];
let soundEnabled=true;
let storageBlocked=false;
let storageRawData=null;
let storageWarning="";
try{soundEnabled=localStorage.getItem(SOUND_KEY)!=="false"}catch(e){storageBlocked=true;storageWarning="Penyimpanan browser tidak dapat dibaca. Perubahan tidak akan tersimpan.";console.error("Sound preference unavailable",e)}
let audioContext=null;
let toastTimer=null;
let focusTimer={duration:25*60,remaining:25*60,endAt:null,taskId:"",mode:"focus",sessionId:null};
let focusSessions=[];
let timerInterval=null;
let selectedDate=new Date();
let shownMonth=new Date(new Date().getFullYear(),new Date().getMonth(),1);
const $=id=>document.getElementById(id);
const months=["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"];

function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2)}
function localDate(d){return new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,16)}
function dayKey(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function esc(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function validTimestamp(value){return typeof value==="string"&&Number.isFinite(Date.parse(value))}
function normalizeTask(task){
 if(!task||typeof task!=="object"||Array.isArray(task)||typeof task.id!=="string"||!/^[A-Za-z0-9_-]{1,100}$/.test(task.id)||
  typeof task.title!=="string"||!task.title.trim()||typeof task.subject!=="string"||!task.subject.trim()||
  typeof task.deadline!=="string"||!Number.isFinite(Date.parse(task.deadline)))return null;
 const duration=Number(task.duration),importance=["low","medium","high"].includes(task.importance)?task.importance:"medium";
 if(!Number.isFinite(duration)||duration<1||duration>10080)return null;
 return {...task,title:task.title.trim(),subject:task.subject.trim(),duration,
  importance,description:typeof task.description==="string"?task.description:"",
  done:task.done===true,createdAt:validTimestamp(task.createdAt)?task.createdAt:null,
  updatedAt:validTimestamp(task.updatedAt)?task.updatedAt:null,
  completedAt:validTimestamp(task.completedAt)?task.completedAt:null,
  isSample:task.isSample===true};
}
function setStorageNotice(message,raw=null){
 storageWarning=message;storageRawData=raw;
 const notice=$("storageNotice");
 if(!notice)return;
 $("storageNoticeText").textContent=message;
 $("downloadRecoveryBtn").hidden=raw===null;
 $("resetStorageBtn").hidden=!storageBlocked;
 notice.classList.toggle("show",Boolean(message));
}
function persistLocalStorage(values,label){
 const keys=Object.keys(values),previous={};
 try{keys.forEach(key=>previous[key]=localStorage.getItem(key))}
 catch(error){
  storageBlocked=true;
  setStorageNotice("Penyimpanan browser tidak dapat dibaca. Muat ulang atau pulihkan data sebelum melanjutkan.",null);
  console.error("Could not read "+label+" before saving",error);return false;
 }
 try{
  keys.forEach(key=>localStorage.setItem(key,values[key]));
  return true;
 }catch(error){
  let rollbackFailed=false;
  keys.slice().reverse().forEach(key=>{
   try{if(previous[key]===null)localStorage.removeItem(key);else localStorage.setItem(key,previous[key])}
   catch(rollbackError){rollbackFailed=true;console.error("Could not roll back storage key "+key,rollbackError)}
  });
  storageBlocked=true;
  setStorageNotice(rollbackFailed?
   "Penyimpanan gagal dan pemulihan otomatis tidak tuntas. Unduh salinan yang tersedia sebelum memulai ulang.":
   "Penyimpanan gagal. Data sebelumnya dipertahankan; muat ulang atau pulihkan data sebelum melanjutkan.",
   rollbackFailed?JSON.stringify(previous):null);
  console.error("Could not save "+label,error);return false;
 }
}
function save(){
 if(storageBlocked)return false;
 const saved=persistLocalStorage({
  [KEY]:JSON.stringify(tasks),[ACTIVITY_KEY]:JSON.stringify(activityEvents.slice(-2000)),
  [DATA_VERSION_KEY]:String(DATA_VERSION)
 },"Studia data");
 if(saved)setStorageNotice("");
 return saved;
}
function recordActivity(type,task){
 activityEvents.push({id:uid(),type,at:new Date().toISOString(),taskId:task.id,taskTitle:task.title});
 activityEvents=activityEvents.slice(-2000);
}
function showToast(message,type="success"){
 const toast=$("toast");
 toast.className="toast show "+type;
 $("toastMessage").textContent=message;
 $("toastMark").textContent=type==="warning"?"!":"✓";
 window.clearTimeout(toastTimer);
 toastTimer=window.setTimeout(()=>toast.classList.remove("show"),3200);
}
function playSound(kind="tap"){
 if(!soundEnabled)return;
 try{
  const AudioContextClass=window.AudioContext||window.webkitAudioContext;
  if(!AudioContextClass){console.warn("Web Audio is not supported in this browser");return}
  audioContext=audioContext||new AudioContextClass();
  if(audioContext.state==="suspended")audioContext.resume().catch(e=>console.error("Audio playback unavailable",e));
  const notes=kind==="success"?[660,880]:kind==="warning"?[440,330]:[520];
  notes.forEach((frequency,index)=>{
   const start=audioContext.currentTime+index*.11;
   const oscillator=audioContext.createOscillator(),gain=audioContext.createGain();
   oscillator.type="sine";oscillator.frequency.setValueAtTime(frequency,start);
   gain.gain.setValueAtTime(.0001,start);gain.gain.exponentialRampToValueAtTime(.07,start+.015);
   gain.gain.exponentialRampToValueAtTime(.0001,start+.13);
   oscillator.connect(gain);gain.connect(audioContext.destination);
   oscillator.start(start);oscillator.stop(start+.14);
  });
 }catch(e){console.error("Could not play sound effect",e)}
}
function syncSoundButton(){
 const button=$("soundToggle");
 button.classList.toggle("muted",!soundEnabled);
 button.textContent=soundEnabled?"♫":"♪";
 button.title=soundEnabled?"Matikan efek suara":"Aktifkan efek suara";
 button.setAttribute("aria-label",button.title);
 button.setAttribute("aria-pressed",String(soundEnabled));
}
function loadFocusData(){
 try{
  const savedTimer=localStorage.getItem(TIMER_KEY);
  if(savedTimer){
   const parsed=JSON.parse(savedTimer);
   const duration=Number(parsed.duration),remaining=Number(parsed.remaining),mode=parsed.mode==="break"?"break":"focus";
   if(([15,25,45,60].includes(duration/60)||(mode==="break"&&duration===300))&&Number.isFinite(remaining)&&remaining>=0){
    focusTimer={duration,remaining,endAt:Number.isFinite(Number(parsed.endAt))&&parsed.endAt?Number(parsed.endAt):null,
     taskId:typeof parsed.taskId==="string"?parsed.taskId:"",mode,
     sessionId:typeof parsed.sessionId==="string"&&/^[A-Za-z0-9_-]{1,100}$/.test(parsed.sessionId)?parsed.sessionId:null};
    if(focusTimer.endAt)focusTimer.remaining=Math.max(0,Math.ceil((focusTimer.endAt-Date.now())/1000));
   }
  }
 }catch(e){
  if(!storageBlocked){
   storageBlocked=true;let raw=null;try{raw=localStorage.getItem(TIMER_KEY)}catch{}
   setStorageNotice("Pengaturan Focus Timer tidak dapat dibaca. Unduh salinan sebelum memilih mulai baru.",raw);
  }
  console.error("Could not restore focus timer",e);
 }
 try{
  const raw=localStorage.getItem(STUDY_KEY),parsed=raw?JSON.parse(raw):[];
  if(!Array.isArray(parsed))throw new Error("Focus history must be an array");
  focusSessions=parsed.filter(s=>s&&Number.isFinite(Number(s.minutes))&&Number(s.minutes)>0&&validTimestamp(s.at))
   .slice(-500).map((s,index)=>({...s,id:typeof s.id==="string"?s.id:"legacy-"+index,
    task:typeof s.task==="string"?s.task:"",taskId:typeof s.taskId==="string"?s.taskId:""}));
 }catch(e){
  if(!storageBlocked){
   storageBlocked=true;let raw=null;try{raw=localStorage.getItem(STUDY_KEY)}catch{}
   setStorageNotice("Riwayat Focus Timer tidak dapat dibaca. Unduh salinan sebelum memilih mulai baru.",raw);
  }
  console.error("Could not restore focus history",e);
 }
}
function saveFocusData(){
 if(storageBlocked)return false;
 return persistLocalStorage({
  [TIMER_KEY]:JSON.stringify(focusTimer),[STUDY_KEY]:JSON.stringify(focusSessions.slice(-500))
 },"Focus Timer data");
}
function renderFocusTimer(){
 const total=focusTimer.duration,remaining=Math.max(0,focusTimer.remaining);
 const minutes=String(Math.floor(remaining/60)).padStart(2,"0"),seconds=String(remaining%60).padStart(2,"0");
 $("timerDisplay").textContent=minutes+":"+seconds;
 $("timerRing").style.setProperty("--timer-progress",(total?Math.min(1,(total-remaining)/total):0)*360+"deg");
 $("focusTimerCard").classList.toggle("break-mode",focusTimer.mode==="break");
 $("timerCaption").textContent=focusTimer.endAt?(focusTimer.mode==="break"?"ISTIRAHAT BERJALAN":"SEDANG FOKUS"):focusTimer.mode==="break"?"SIAP ISTIRAHAT":remaining===0?"SESI SELESAI":"SIAP FOKUS";
 $("timerStartBtn").textContent=focusTimer.endAt?"Jeda":focusTimer.mode==="break"?"Mulai istirahat":"Mulai fokus";
 $("timerResetBtn").textContent=focusTimer.mode==="break"?"Kembali ke fokus":"Atur ulang";
 $("timerDuration").disabled=Boolean(focusTimer.endAt)||focusTimer.mode==="break";
 $("timerTask").disabled=Boolean(focusTimer.endAt)||focusTimer.mode==="break";
 const previousTask=focusTimer.taskId;
 $("timerTask").innerHTML='<option value="">Sesi belajar bebas</option>'+sorted().filter(task=>!task.done).map(task=>`<option value="${esc(task.id)}">${esc(task.title)} · ${esc(task.subject)}</option>`).join("");
 const sessionCount=focusSessions.length,totalMinutes=focusSessions.reduce((sum,session)=>sum+Number(session.minutes),0);
 $("focusTotal").textContent=totalMinutes.toLocaleString("id-ID")+" menit · "+sessionCount+" sesi";
 $("focusHistory").innerHTML=focusSessions.slice(-3).reverse().map(session=>
  `<div class="focus-history-item"><span>${esc(session.task||"Sesi belajar bebas")} · ${esc(fmt(session.at))}</span><strong>${esc(session.minutes)} mnt</strong></div>`
 ).join("");
 $("timerTask").value=previousTask&&tasks.some(task=>task.id===previousTask&&!task.done)?previousTask:"";
}
function updateFocusTick(){
 if(!focusTimer.endAt)return;
 focusTimer.remaining=Math.max(0,Math.ceil((focusTimer.endAt-Date.now())/1000));
 renderFocusTimer();
 if(focusTimer.remaining===0)completeFocusSession();
}
function startOrPauseFocus(){
 if(storageBlocked){showToast("Penyimpanan tidak tersedia; timer tidak dapat dipulihkan setelah halaman ditutup.","warning");return}
 if(focusTimer.endAt){
  focusTimer.remaining=Math.max(0,Math.ceil((focusTimer.endAt-Date.now())/1000));
  focusTimer.endAt=null;
  window.clearInterval(timerInterval);timerInterval=null;
  saveFocusData();renderFocusTimer();playSound("tap");return;
 }
 if(focusTimer.remaining===0)focusTimer.remaining=focusTimer.duration;
 focusTimer.taskId=$("timerTask").value;
 if(focusTimer.mode==="focus"&&!focusTimer.sessionId)focusTimer.sessionId=uid();
 focusTimer.endAt=Date.now()+focusTimer.remaining*1000;
 saveFocusData();renderFocusTimer();playSound("tap");
 timerInterval=window.setInterval(updateFocusTick,250);
}
function resetFocusTimer(){
 window.clearInterval(timerInterval);timerInterval=null;
 focusTimer.mode="focus";
 focusTimer.duration=Number($("timerDuration").value)*60;
 focusTimer.remaining=focusTimer.duration;focusTimer.endAt=null;focusTimer.sessionId=null;
 focusTimer.taskId=$("timerTask").value;
 saveFocusData();renderFocusTimer();playSound("tap");
}
function completeFocusSession(){
 window.clearInterval(timerInterval);timerInterval=null;
 focusTimer.endAt=null;
 if(focusTimer.mode==="break"){
  focusTimer.mode="focus";focusTimer.duration=Number($("timerDuration").value)*60;
  focusTimer.remaining=focusTimer.duration;focusTimer.sessionId=null;
  saveFocusData();renderFocusTimer();
  showToast("Waktu istirahat selesai. Siap fokus lagi?");playSound("success");
  return;
 }
 const task=tasks.find(item=>item.id===focusTimer.taskId);
 const sessionId=focusTimer.sessionId||uid();
 if(!focusSessions.some(session=>session.id===sessionId)){
  focusSessions.push({id:sessionId,at:new Date().toISOString(),minutes:focusTimer.duration/60,
   task:task?task.title:"",taskId:task?task.id:""});
  focusSessions=focusSessions.slice(-500);
 }
 focusTimer.mode="break";focusTimer.duration=5*60;focusTimer.remaining=focusTimer.duration;
 focusTimer.endAt=null;focusTimer.sessionId=null;
 saveFocusData();renderFocusTimer();renderDashboard();
 showToast(task?"Sesi fokus selesai untuk "+task.title+". Mulai istirahat 5 menit?":"Sesi fokus selesai. Mulai istirahat 5 menit?","success");
 playSound("success");
}
function load(){
 try{
  const storedVersion=localStorage.getItem(DATA_VERSION_KEY);
  if(storedVersion!==null&&![1,DATA_VERSION].includes(Number(storedVersion)))
   throw new Error("Unsupported Studia data version");
  const raw=localStorage.getItem(KEY);
  if(raw!==null){
   const data=JSON.parse(raw);
   if(!Array.isArray(data))throw new Error("Task data must be an array");
   const normalized=data.map(normalizeTask);
   if(normalized.some(task=>task===null)||new Set(normalized.map(task=>task.id)).size!==normalized.length)
    throw new Error("One or more saved tasks are invalid or duplicated");
   tasks=normalized;
  }
 }catch(e){
  tasks=[];storageBlocked=true;
  let raw=null;try{raw=localStorage.getItem(KEY)}catch{}
  setStorageNotice("Data tugas tersimpan tidak dapat dibaca dan belum dihapus. Unduh salinan aslinya sebelum memilih mulai baru.",raw);
  console.error("Could not restore saved tasks",e);
 }
 try{
  const raw=localStorage.getItem(ACTIVITY_KEY),data=raw?JSON.parse(raw):[];
  if(!Array.isArray(data)||data.some(event=>!event||!validTimestamp(event.at)||!["created","completed","reopened"].includes(event.type)))throw new Error("Activity history is invalid");
  activityEvents=data.slice(-2000);
 }catch(e){
  if(!storageBlocked){
   storageBlocked=true;
   let raw=null;try{raw=localStorage.getItem(ACTIVITY_KEY)}catch{}
   setStorageNotice("Riwayat aktivitas tersimpan tidak dapat dibaca. Unduh salinan sebelum memilih mulai baru.",raw);
  }
  console.error("Could not restore activity history",e);
 }
 if(storageWarning)setStorageNotice(storageWarning,storageRawData);
}
function resetSamples(){
 if(storageBlocked){showToast("Penyimpanan terkunci sampai data yang tidak terbaca dipulihkan atau dibersihkan.","warning");return}
 if(tasks.length&&!confirm("Data tugas saat ini akan diganti dengan data contoh. Lanjutkan?"))return;
 const now=new Date();
 const plus=(n)=>new Date(now.getTime()+n*86400000);
 tasks=[
  {id:uid(),title:"Menyelesaikan latihan Python",subject:"Algoritma dan Pemrograman",deadline:localDate(plus(1)),importance:"high",duration:90,description:"Latihan dasar pemrograman",done:false,isSample:true,createdAt:now.toISOString()},
  {id:uid(),title:"Review materi perkuliahan",subject:"Bahasa Inggris",deadline:localDate(plus(2)),importance:"medium",duration:45,description:"Persiapan kelas",done:false,isSample:true,createdAt:now.toISOString()},
  {id:uid(),title:"Membuat laporan praktikum",subject:"Teknologi Rekayasa Otomasi",deadline:localDate(plus(4)),importance:"high",duration:120,description:"Susun laporan dan kesimpulan",done:false,isSample:true,createdAt:now.toISOString()},
  {id:uid(),title:"Membaca modul minggu ini",subject:"Matematika Teknik",deadline:localDate(plus(6)),importance:"low",duration:30,description:"Review konsep dasar",done:false,isSample:true,createdAt:now.toISOString()}
 ];
 activityEvents=[];
 if(!save())return;
 renderAll();showToast("Data contoh dimuat. Tugas contoh ditandai agar berbeda dari tugasmu.","success");playSound("success");
}
function isLate(t){return !t.done&&new Date(t.deadline).getTime()<Date.now()}
function score(t){
 if(t.done)return -Infinity;
 const h=(new Date(t.deadline).getTime()-Date.now())/3600000;
 const urgency=h<0?50:h<=24?40:h<=72?25:h<=168?15:5;
 const imp={high:30,medium:20,low:10}[t.importance]||10;
 const quick=Math.max(0,10-Math.floor(Math.max(1,Number(t.duration)||1)/30));
 return urgency+imp+quick;
}
function sorted(){return [...tasks].sort((a,b)=>a.done!==b.done?(a.done?1:-1):(score(b)-score(a)||new Date(a.deadline)-new Date(b.deadline)))}
function fmt(v){
 const d=new Date(v);return isNaN(d)?"Tanggal tidak valid":d.toLocaleString("id-ID",{day:"numeric",month:"short",year:"numeric",hour:"2-digit",minute:"2-digit"})
}
function reason(t){
 const h=(new Date(t.deadline)-Date.now())/3600000;
 const due=h<0?"deadline sudah terlewat":h<=24?"deadline dalam "+Math.max(1,Math.ceil(h))+" jam":h<=48?"deadline besok":h<=168?"deadline dalam "+Math.ceil(h/24)+" hari":"deadline masih "+Math.ceil(h/24)+" hari lagi";
 const importance={high:"kepentingan tinggi",medium:"kepentingan sedang",low:"kepentingan rendah"}[t.importance];
 return "Disarankan dikerjakan "+(h<0?"segera":"lebih dahulu")+" karena "+due+", estimasi "+t.duration+" menit, dan "+importance+".";
}
function badge(t){
 if(t.done)return ["SELESAI","green"];
 if(isLate(t))return ["TERLAMBAT","red"];
 const s=score(t);return s>=65?["PRIORITAS TINGGI","red"]:s>=40?["SEDANG","yellow"]:["RENDAH","gray"];
}
function toggleDone(id){
 const task=tasks.find(t=>t.id===id);
 if(!task)return;
 if(storageBlocked){showToast("Perubahan diblokir agar data yang tidak terbaca tidak tertimpa.","warning");return}
 task.done=!task.done;task.updatedAt=new Date().toISOString();
 task.completedAt=task.done?task.updatedAt:null;
 recordActivity(task.done?"completed":"reopened",task);
 if(!save()){renderAll();return}
 renderAll();
 showToast(task.done?"Tugas selesai. Kerja bagus!":"Tugas dibuka kembali",task.done?"success":"");
 playSound(task.done?"success":"tap");
}
function removeTask(id){
 const t=tasks.find(x=>x.id===id);
 if(storageBlocked){showToast("Perubahan diblokir agar data yang tidak terbaca tidak tertimpa.","warning");return}
 if(t&&confirm('Hapus tugas "'+t.title+'"?')){
  tasks=tasks.filter(x=>x.id!==id);
  if(!save()){renderAll();return}
  renderAll();showToast("Tugas berhasil dihapus","warning");playSound("warning")
 }
}
function openTask(t=null){
 if(storageBlocked){showToast("Perubahan diblokir agar data yang tidak terbaca tidak tertimpa.","warning");return}
 playSound("tap");
 $("taskForm").reset();$("formError").textContent="";$("taskId").value=t?t.id:"";
 $("formTitle").textContent=t?"Edit Tugas":"Tambah Tugas";
 if(t){
  $("title").value=t.title;$("subject").value=t.subject;$("deadline").value=t.deadline;
  $("importance").value=t.importance;$("duration").value=t.duration;$("description").value=t.description||"";
 }else{
  $("importance").value="medium";$("duration").value=60;
  $("deadline").value=localDate(new Date(Date.now()+86400000));
 }
 $("taskModal").classList.add("open");$("title").focus();
}
function closeTask(){$("taskModal").classList.remove("open")}
function editTask(id){const t=tasks.find(x=>x.id===id);if(t)openTask(t)}
$("taskForm").addEventListener("submit",e=>{
 e.preventDefault();
 const id=$("taskId").value,title=$("title").value.trim(),subject=$("subject").value.trim();
 const deadline=$("deadline").value,importance=$("importance").value;
 const duration=Number($("duration").value),description=$("description").value.trim();
 if(!title||!subject||!deadline||isNaN(new Date(deadline).getTime())||!Number.isFinite(duration)||duration<1||duration>10080){
  $("formError").textContent="Periksa kembali nama tugas, mata kuliah, deadline, dan durasi.";return;
 }
 const old=tasks.find(t=>t.id===id);
 const now=new Date().toISOString();
 const item={id:id||uid(),title,subject,deadline,importance,duration,description,
  done:old?old.done:false,isSample:old?old.isSample:false,
  createdAt:old?old.createdAt:now,updatedAt:now,completedAt:old?old.completedAt:null};
 tasks=id?tasks.map(t=>t.id===id?item:t):[...tasks,item];
 if(!id)recordActivity("created",item);
 if(!save()){renderAll();return}
 closeTask();renderAll();showToast(id?"Tugas berhasil diperbarui":"Tugas baru berhasil ditambahkan");playSound("success");
});
function taskCard(t){
 const b=badge(t);
 return `<article class="task-row ${t.done?"done":""}">
 <div class="task-row-top"><div class="task-row-info">
 <div class="task-row-title">${esc(t.title)} ${t.isSample?'<span class="pill gray">CONTOH</span>':""}</div>
 <div class="task-row-meta">${esc(t.subject)}<br>Deadline: ${esc(fmt(t.deadline))}<br>Durasi: ${esc(t.duration)} menit · Kepentingan: ${esc(t.importance)}${t.description?"<br>"+esc(t.description):""}</div>
 </div><span class="pill ${b[1]}">${b[0]}</span></div>
 <div class="task-row-actions"><button class="btn small" onclick="toggleDone('${t.id}')">${t.done?"Buka kembali":"✓ Selesai"}</button><button class="btn small" onclick="editTask('${t.id}')">Edit</button><button class="btn small" onclick="removeTask('${t.id}')">Hapus</button></div></article>`;
}
function renderTasks(){
 const q=($("taskSearch")?.value||$("globalSearch").value).trim().toLowerCase();
 const filter=$("taskFilter")?.value||"all";
 const sortBy=$("taskSort")?.value||"priority";
 const list=sorted().filter(t=>(t.title+" "+t.subject).toLowerCase().includes(q)&&
 (filter==="all"||(filter==="pending"&&!t.done)||(filter==="completed"&&t.done)||(filter==="overdue"&&isLate(t))));
 if(sortBy==="deadline")list.sort((a,b)=>new Date(a.deadline)-new Date(b.deadline));
 if(sortBy==="title")list.sort((a,b)=>a.title.localeCompare(b.title,"id"));
 $("fullTaskList").innerHTML=list.length?list.map(taskCard).join(""):'<div class="empty">Tidak ada tugas yang sesuai.</div>';
}
function exportTasks(){
 const quote=value=>{
  let text=String(value??"");
  if(/^[\s]*[=+\-@]/.test(text))text="'"+text;
  return '"'+text.replace(/"/g,'""')+'"';
 };
 const rows=[["Nama tugas","Mata kuliah","Deadline","Prioritas","Durasi (menit)","Status","Catatan"],
  ...sorted().map(task=>[task.title,task.subject,fmt(task.deadline),task.importance,task.duration,task.done?"Selesai":isLate(task)?"Terlambat":"Aktif",task.description||""])];
 const csv="\uFEFF"+rows.map(row=>row.map(quote).join(",")).join("\r\n");
 const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
 const link=document.createElement("a");
 link.href=url;link.download="studia-tugas-"+dayKey(new Date())+".csv";
 document.body.appendChild(link);link.click();link.remove();
 window.setTimeout(()=>URL.revokeObjectURL(url),1000);
 showToast("Laporan tugas berhasil diunduh");playSound("success");
}
function downloadJson(filename,value){
 const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download=filename;
 document.body.appendChild(link);link.click();link.remove();
 window.setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function exportBackup(){
 downloadJson("studia-backup-"+dayKey(new Date())+".json",{
  format:BACKUP_FORMAT,version:BACKUP_VERSION,exportedAt:new Date().toISOString(),
  tasks,activityEvents:activityEvents.slice(-2000),focusSessions:focusSessions.slice(-500),
  focusTimer,soundEnabled
 });
 showToast("Cadangan Studia berhasil diunduh");playSound("success");
}
function parseBackup(data){
 if(!data||data.format!==BACKUP_FORMAT||data.version!==BACKUP_VERSION||
  !Array.isArray(data.tasks)||!Array.isArray(data.activityEvents)||!Array.isArray(data.focusSessions))
  throw new Error("Format cadangan tidak dikenali.");
 const importedTasks=data.tasks.map(normalizeTask);
 if(importedTasks.some(task=>task===null)||new Set(importedTasks.map(task=>task.id)).size!==importedTasks.length)
  throw new Error("Cadangan berisi data tugas yang tidak valid atau duplikat.");
 const importedEvents=data.activityEvents;
 if(importedEvents.length>2000||importedEvents.some(event=>!event||typeof event.id!=="string"||
  !["created","completed","reopened"].includes(event.type)||!validTimestamp(event.at)||
  typeof event.taskId!=="string"||typeof event.taskTitle!=="string"))
  throw new Error("Riwayat aktivitas di dalam cadangan tidak valid.");
 const importedSessions=data.focusSessions;
 if(importedSessions.length>500||importedSessions.some(session=>!session||
  typeof session.id!=="string"||!validTimestamp(session.at)||
  !Number.isFinite(Number(session.minutes))||Number(session.minutes)<=0||
  typeof session.task!=="string"||typeof session.taskId!=="string"))
  throw new Error("Riwayat timer di dalam cadangan tidak valid.");
 const timer=data.focusTimer;
 if(!timer||!Number.isFinite(Number(timer.duration))||!Number.isFinite(Number(timer.remaining))||
  Number(timer.remaining)<0||!( [900,1500,2700,3600].includes(Number(timer.duration))||
   (timer.mode==="break"&&Number(timer.duration)===300) )||
  !["focus","break"].includes(timer.mode))
  throw new Error("Pengaturan timer di dalam cadangan tidak valid.");
 return {tasks:importedTasks,activityEvents:importedEvents.slice(-2000),
  focusSessions:importedSessions.slice(-500),focusTimer:{...timer,
   duration:Number(timer.duration),remaining:Number(timer.remaining),
   endAt:Number.isFinite(Number(timer.endAt))&&timer.endAt?Number(timer.endAt):null,
   taskId:typeof timer.taskId==="string"?timer.taskId:"",
   sessionId:typeof timer.sessionId==="string"?timer.sessionId:null},
  soundEnabled:data.soundEnabled!==false};
}
async function importBackupFile(file){
 if(!file)return;
 let imported;
 try{imported=parseBackup(JSON.parse(await file.text()))}
 catch(error){showToast(error instanceof SyntaxError?"File cadangan bukan JSON yang valid.":error.message,"warning");return}
 if(!confirm("Cadangan ini akan mengganti tugas, riwayat, dan pengaturan Studia di browser ini. Lanjutkan?"))return;
 const keys=[KEY,ACTIVITY_KEY,DATA_VERSION_KEY,STUDY_KEY,TIMER_KEY,SOUND_KEY];
 let previous;
 try{previous=keys.map(key=>localStorage.getItem(key))}
 catch(error){setStorageNotice("Tidak dapat membaca data sebelum pemulihan. Cadangan tidak diimpor.",null);console.error("Could not snapshot storage before import",error);return}
 const oldState={tasks,activityEvents,focusSessions,focusTimer,soundEnabled,storageBlocked,storageWarning,storageRawData};
 tasks=imported.tasks;activityEvents=imported.activityEvents;focusSessions=imported.focusSessions;
 focusTimer=imported.focusTimer;soundEnabled=imported.soundEnabled;storageBlocked=false;
 try{
  localStorage.setItem(KEY,JSON.stringify(tasks));
  localStorage.setItem(ACTIVITY_KEY,JSON.stringify(activityEvents));
  localStorage.setItem(DATA_VERSION_KEY,String(DATA_VERSION));
  localStorage.setItem(STUDY_KEY,JSON.stringify(focusSessions));
  localStorage.setItem(TIMER_KEY,JSON.stringify(focusTimer));
  localStorage.setItem(SOUND_KEY,String(soundEnabled));
 }catch(error){
  [tasks,activityEvents,focusSessions,focusTimer,soundEnabled,storageBlocked,storageWarning,storageRawData]=
   [oldState.tasks,oldState.activityEvents,oldState.focusSessions,oldState.focusTimer,oldState.soundEnabled,true,
    "Pemulihan gagal; data sebelumnya dipertahankan jika browser mengizinkan pemulihan.",null];
  keys.forEach((key,index)=>{
   try{if(previous[index]===null)localStorage.removeItem(key);else localStorage.setItem(key,previous[index])}
   catch(rollbackError){console.error("Could not roll back imported storage key "+key,rollbackError)}
  });
  setStorageNotice(storageWarning,null);renderAll();
  console.error("Could not import Studia backup",error);return;
 }
 storageWarning="";storageRawData=null;window.clearInterval(timerInterval);timerInterval=null;
 setStorageNotice("");syncSoundButton();renderAll();
 if(focusTimer.endAt){timerInterval=window.setInterval(updateFocusTick,250);updateFocusTick()}
 showToast("Cadangan berhasil dipulihkan");playSound("success");
}
function downloadRecoveryData(){
 if(storageRawData!==null)downloadJson("studia-data-pemulihan-"+dayKey(new Date())+".json",{
  format:"studia-recovery",capturedAt:new Date().toISOString(),originalData:storageRawData
 });
}
function resetUnreadableStorage(){
 if(!storageBlocked||!confirm("Data lokal yang tidak dapat dibaca akan diganti dengan data kosong. Unduh salinannya terlebih dahulu jika ingin menyimpannya. Lanjutkan?"))return;
 tasks=[];activityEvents=[];focusSessions=[];
 focusTimer={duration:25*60,remaining:25*60,endAt:null,taskId:"",mode:"focus",sessionId:null};
 storageBlocked=false;
 if(!save()||!saveFocusData())return;
 storageWarning="";storageRawData=null;setStorageNotice("");renderAll();
 showToast("Penyimpanan lokal dimulai ulang dalam keadaan kosong.");
}
function renderDashboard(){
 const pending=tasks.filter(t=>!t.done),done=tasks.filter(t=>t.done),late=pending.filter(isLate);
 const rate=tasks.length?Math.round(done.length/tasks.length*100):0;
 $("completionStat").textContent=rate+"%";$("activeStat").textContent=pending.length;
 $("doneStat").textContent=done.length;$("lateStat").textContent=late.length;
 $("navPending").textContent=pending.length;
 $("today").textContent=new Date().toLocaleDateString("id-ID",{weekday:"long",day:"numeric",month:"long",year:"numeric"});
 $("chartRate").textContent=rate+"%";$("chartProgress").style.width=rate+"%";
 $("overviewActive").textContent=pending.length;$("overviewDone").textContent=done.length;
 $("activeProgress").style.width=(tasks.length?pending.length/tasks.length*100:0)+"%";
 $("doneProgress").style.width=rate+"%";
 const mins=pending.reduce((s,t)=>s+(Number(t.duration)||0),0);
 $("totalTime").textContent=(mins/60).toLocaleString("id-ID",{maximumFractionDigits:1})+" jam";
 $("studyInsight").textContent=late.length?late.length+" tugas telah melewati deadline. Evaluasi prioritasmu.":pending.length?"Terus kerjakan tugas secara konsisten.":"Semua tugas sudah selesai!";
 renderTodayBrief(pending,late);
 const focus=sorted().find(t=>!t.done);
 $("focusContent").innerHTML=focus?`<span class="pill">REKOMENDASI UTAMA</span>${focus.isSample?'<span class="pill gray">CONTOH</span>':""}<div class="focus-title">${esc(focus.title)}</div><div class="muted">${esc(focus.subject)}</div><div class="sub">Deadline: ${esc(fmt(focus.deadline))}<br>Estimasi: ${esc(focus.duration)} menit</div><div class="reason">${esc(reason(focus))}</div><button class="btn primary" onclick="$('timerTask').value='${focus.id}';startOrPauseFocus()">Mulai sesi fokus</button> <button class="btn" onclick="editTask('${focus.id}')">Edit tugas</button>`:'<div class="empty">Belum ada tugas aktif.<br>Tambahkan tugas pertamamu atau coba data contoh.</div><button class="btn primary small" onclick="openTask()">＋ Tambah tugas</button> <button class="btn small" onclick="resetSamples()">Coba data contoh</button>';
 const recent=sorted().filter(t=>!t.done).slice(0,4);
 $("assignmentList").innerHTML=recent.length?recent.map(t=>{const b=badge(t);return `<div class="assignment"><div><div class="assignment-name">${esc(t.title)}</div><div class="assignment-sub">${esc(t.subject)}</div></div><div class="assignment-date">${esc(fmt(t.deadline))}</div><span class="pill ${b[1]}">${b[0]}</span></div>`}).join(""):'<div class="empty">Belum ada tugas aktif.</div>';
 renderCompletionHistory();
 renderActivity();
}
function renderTodayBrief(pending,late){
 const today=dayKey(new Date());
 const dueToday=pending.filter(task=>task.deadline.slice(0,10)===today)
  .sort((a,b)=>new Date(a.deadline)-new Date(b.deadline));
 const next=sorted().filter(task=>!task.done).slice(0,3);
 $("todayCount").textContent=dueToday.length;
 $("todayTasksIntro").textContent=dueToday.length?
  dueToday.length+" tugas perlu diselesaikan hari ini.":"Tidak ada tugas dengan tenggat hari ini.";
 $("todayTasksList").innerHTML=dueToday.length?dueToday.map(task=>
  `<button class="today-item" onclick="editTask('${task.id}')"><span>${esc(task.title)}</span><span class="pill">${esc(new Date(task.deadline).toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"}))}</span></button>`
 ).join(""):'<div class="empty">Waktunya bisa digunakan untuk mulai lebih awal atau beristirahat.</div>';
 $("nextDeadlineIntro").textContent=late.length?
  late.length+" tugas terlambat; periksa prioritas dan atur ulang rencanamu tanpa mengubah deadline otomatis.":
  next.length?"Deadline terdekat diurutkan berdasarkan prioritas dan waktu.":"Tidak ada tugas aktif.";
 $("nextDeadlineList").innerHTML=next.length?next.map(task=>
  `<button class="today-item" onclick="editTask('${task.id}')"><span>${esc(task.title)}</span><span class="pill ${isLate(task)?"red":task.isSample?"gray":""}">${esc(task.isSample?"CONTOH · "+fmt(task.deadline):isLate(task)?"Terlambat":fmt(task.deadline))}</span></button>`
 ).join(""):'<div class="empty">Tambahkan tugas untuk melihat prioritas berikutnya.</div>';
}
function renderCompletionHistory(){
 const today=new Date(),first=new Date(today.getFullYear(),today.getMonth(),today.getDate()-27);
 const counts=Array(28).fill(0);
 activityEvents.filter(event=>event.type==="completed").forEach(event=>{
  const date=new Date(event.at);
  const index=Math.floor((new Date(date.getFullYear(),date.getMonth(),date.getDate())-first)/86400000);
  if(index>=0&&index<counts.length)counts[index]++;
 });
 const hasHistory=counts.some(count=>count>0),max=Math.max(1,...counts);
 const points=counts.map((count,index)=>({x:45+index*20,y:140-count/max*120,count}));
 const line=points.map((point,index)=>(index?"L":"M")+point.x+" "+point.y).join(" ");
 $("completionChart").classList.toggle("is-empty",!hasHistory);
 $("chartMax").textContent=String(max);$("chartMid").textContent=String(Math.ceil(max/2));
 $("chartLine").setAttribute("d",hasHistory?line:"");
 $("chartArea").setAttribute("d",hasHistory?line+" L "+points[points.length-1].x+" 145 L "+points[0].x+" 145 Z":"");
 $("chartDots").innerHTML=hasHistory?points.filter((point,index)=>point.count>0).map(point=>
  `<circle cx="${point.x}" cy="${point.y}" r="3" fill="#c2a0ff"><title>${point.count} tugas selesai</title></circle>`
 ).join(""):"";
}
function renderActivity(){
 const today=new Date(),first=new Date(today.getFullYear(),today.getMonth(),today.getDate()-27);
 const dueCounts=new Map();
 tasks.forEach(task=>{
  const key=task.deadline.slice(0,10);
  dueCounts.set(key,(dueCounts.get(key)||0)+1);
 });
 let total=0;
 $("activityGrid").innerHTML=Array.from({length:28},(_,index)=>{
  const date=new Date(first.getFullYear(),first.getMonth(),first.getDate()+index);
  const key=dayKey(date),count=dueCounts.get(key)||0;
  total+=count;
  const level=count>=4?4:count>=3?3:count>=2?2:count?1:0;
  const label=date.toLocaleDateString("id-ID",{weekday:"long",day:"numeric",month:"long"});
  return `<button class="heat-cell level-${level}" onclick="selectDate('${key}')" title="${esc(label)} · ${count} deadline${count===1?"":"s"}" aria-label="${esc(label)}: ${count} deadline${count===1?"":"s"}"></button>`;
 }).join("");
 $("activitySummary").textContent=total+" deadline tercatat";
}
function renderCalendar(){
 [1,2].forEach(n=>{
  const label=$("monthLabel"+(n===1?"":"2")),grid=$("calendarDays"+(n===1?"":"2"));
  label.textContent=months[shownMonth.getMonth()]+" "+shownMonth.getFullYear();
  const first=new Date(shownMonth.getFullYear(),shownMonth.getMonth(),1);
  const count=new Date(shownMonth.getFullYear(),shownMonth.getMonth()+1,0).getDate();
  let html="";
  for(let i=0;i<first.getDay();i++)html+='<span></span>';
  for(let d=1;d<=count;d++){
   const date=new Date(shownMonth.getFullYear(),shownMonth.getMonth(),d);
   const key=dayKey(date),today=key===dayKey(new Date()),selected=key===dayKey(selectedDate);
   const event=tasks.some(t=>t.deadline.slice(0,10)===key&&!t.done);
   html+=`<button class="day ${today?"today":""} ${selected?"selected":""} ${event?"event":""}" onclick="selectDate('${key}')" aria-label="${d} ${months[shownMonth.getMonth()]}">${d}</button>`;
  }
  grid.innerHTML=html;
 });
 renderAgenda();
}
function selectDate(key){
 const [y,m,d]=key.split("-").map(Number);
 selectedDate=new Date(y,m-1,d);shownMonth=new Date(y,m-1,1);
 renderCalendar();
}
function renderAgenda(){
 const key=dayKey(selectedDate);
 const list=tasks.filter(t=>t.deadline.slice(0,10)===key).sort((a,b)=>new Date(a.deadline)-new Date(b.deadline));
 const title=selectedDate.toLocaleDateString("id-ID",{day:"numeric",month:"long",year:"numeric"});
 $("agendaTitle").textContent="Agenda";$("agendaSub").textContent=title;
 const html=list.length?list.map(t=>`<div class="agenda-item"><input class="check" type="checkbox" ${t.done?"checked":""} onchange="toggleDone('${t.id}')" aria-label="Tandai selesai"><div class="agenda-content"><div class="agenda-title">${esc(t.title)}</div><div class="agenda-meta">${esc(t.subject)} · ${esc(t.importance)}</div></div><div class="agenda-time">${esc(new Date(t.deadline).toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"}))}</div></div>`).join(""):'<div class="empty">Tidak ada agenda pada tanggal ini.</div>';
 $("agendaList").innerHTML=html;
 $("scheduleDateTitle").textContent=title;$("scheduleList").innerHTML=html;
}
function renderMonitoring(){
 const pending=tasks.filter(t=>!t.done),done=tasks.filter(t=>t.done),late=pending.filter(isLate);
 const rate=tasks.length?Math.round(done.length/tasks.length*100):0;
 $("mTotal").textContent=tasks.length;$("mRate").textContent=rate+"%";
 $("mLate").textContent=late.length;
 $("mHours").textContent=(pending.reduce((s,t)=>s+(Number(t.duration)||0),0)/60).toLocaleString("id-ID",{maximumFractionDigits:1})+"h";
 const groups=[["Selesai",done.length],["Belum selesai",pending.length],["Terlambat",late.length]];
 $("monitorBars").innerHTML=groups.map(([name,n])=>`<div class="metric-row"><span>${name}</span><strong>${n}</strong></div><div class="progress" style="margin-bottom:16px"><div style="width:${tasks.length?n/tasks.length*100:0}%"></div></div>`).join("");
}
function renderClassroom(){
 const subjects=[...new Set(tasks.map(t=>t.subject))];
 $("classroomList").innerHTML=subjects.length?subjects.map(s=>{
  const ts=tasks.filter(t=>t.subject===s),d=ts.filter(t=>t.done).length;
  return `<article class="card"><div class="stat-icon">▣</div><h3 style="margin-top:13px">${esc(s)}</h3><div class="sub">${ts.length} tugas · ${d} selesai</div><div class="progress"><div style="width:${ts.length?d/ts.length*100:0}%"></div></div><button class="btn small" onclick="navigate('tasks');$('taskSearch').value=${JSON.stringify(s)};renderTasks()">Lihat tugas</button></article>`;
 }).join(""):'<div class="card empty">Mata kuliah muncul setelah kamu menambahkan tugas.</div>';
}
function renderMessages(){
 const pending=tasks.filter(t=>!t.done);
 const messages=[];
 pending.filter(isLate).forEach(t=>messages.push(["Deadline terlewat",t.title+" — "+t.subject,"red"]));
 pending.filter(t=>!isLate(t)&&(new Date(t.deadline)-Date.now())<=86400000).forEach(t=>messages.push(["Deadline mendekat",t.title+" — "+fmt(t.deadline),"yellow"]));
 const actionable=messages.length;
 if(!actionable)messages.push(["Semua terkendali","Tidak ada peringatan deadline berdasarkan tugas yang tersimpan.","green"]);
 const html=messages.map(m=>`<div class="agenda-item"><span class="pill ${m[2]}">●</span><div class="agenda-content"><div class="agenda-title">${esc(m[0])}</div><div class="agenda-meta">${esc(m[1])}</div></div></div>`).join("");
 $("messageList").innerHTML=html;
 $("notificationList").innerHTML=html;
 $("notificationDot").classList.toggle("active",actionable>0);
}
function openNotifications(){
 renderMessages();$("notificationModal").classList.add("open");playSound("tap");
 $("closeNotificationsBtn").focus();
}
function closeNotifications(){$("notificationModal").classList.remove("open")}
function renderAll(){
 renderDashboard();renderTasks();renderCalendar();renderMonitoring();renderClassroom();renderMessages();
 renderFocusTimer();
}
function navigate(view){
 document.querySelectorAll(".view").forEach(v=>v.classList.remove("active"));
 $("view-"+view).classList.add("active");
 document.querySelectorAll(".nav[data-view]").forEach(b=>b.classList.toggle("active",b.dataset.view===view));
 $("sidebar").classList.remove("open");
 if(view==="tasks")renderTasks();
 window.scrollTo({top:0,behavior:"smooth"});
}
document.querySelectorAll(".nav[data-view]").forEach(b=>b.addEventListener("click",()=>navigate(b.dataset.view)));
$("prevMonth").onclick=$("prevMonth2").onclick=()=>{shownMonth=new Date(shownMonth.getFullYear(),shownMonth.getMonth()-1,1);renderCalendar()};
$("nextMonth").onclick=$("nextMonth2").onclick=()=>{shownMonth=new Date(shownMonth.getFullYear(),shownMonth.getMonth()+1,1);renderCalendar()};
$("globalSearch").addEventListener("input",()=>{
 $("taskSearch").value=$("globalSearch").value;
 if($("globalSearch").value.trim())navigate("tasks");
 renderTasks();
});
$("menuBtn").onclick=()=>$("sidebar").classList.toggle("open");
 $("sampleBtn").onclick=resetSamples;
 $("exportTasksBtn").onclick=exportTasks;
  $("exportBackupBtn").onclick=exportBackup;
  $("importBackupBtn").onclick=()=>$("backupFile").click();
  $("backupFile").onchange=async event=>{
   const file=event.target.files[0];event.target.value="";
   await importBackupFile(file);
  };
  $("downloadRecoveryBtn").onclick=downloadRecoveryData;
  $("resetStorageBtn").onclick=resetUnreadableStorage;
 $("timerStartBtn").onclick=startOrPauseFocus;
 $("timerResetBtn").onclick=resetFocusTimer;
 $("timerDuration").onchange=resetFocusTimer;
 $("timerTask").onchange=()=>{focusTimer.taskId=$("timerTask").value;saveFocusData()};
 $("notificationBtn").onclick=openNotifications;
 $("closeNotificationsBtn").onclick=closeNotifications;
 $("allMessagesBtn").onclick=()=>{closeNotifications();navigate("messages")};
 $("soundToggle").onclick=()=>{
  if(storageBlocked){showToast("Penyimpanan tidak tersedia; preferensi suara tidak dapat disimpan.","warning");return}
  soundEnabled=!soundEnabled;
  try{localStorage.setItem(SOUND_KEY,String(soundEnabled))}catch(e){
   storageBlocked=true;setStorageNotice("Preferensi suara belum tersimpan karena penyimpanan browser gagal.",null);
   console.error("Could not save sound preference",e);return;
  }
  syncSoundButton();playSound("tap");
  showToast(soundEnabled?"Efek suara diaktifkan":"Efek suara dimatikan");
 };
document.addEventListener("keydown",e=>{if(e.key==="Escape"){closeTask();closeNotifications()}});
syncSoundButton();
load();loadFocusData();renderAll();
if(focusTimer.endAt){timerInterval=window.setInterval(updateFocusTick,250);updateFocusTick()}

/**
 * 萬能科技大學 - 商業軟體應用 ✕ Agentic AI ✕ iPAS AI 應用規劃師
 * 前端核心邏輯與互動系統 (支援在線 API 與單機離線雙模)
 * 授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu)
 */

// Firebase Configuration (vnu-business-software-11501)
const firebaseConfig = {
  apiKey: "AIzaSyBvnm6fkAl8BLGkNvyfvyvUzQK4cTz4aK8",
  authDomain: "vnu-business-software-11501.firebaseapp.com",
  projectId: "vnu-business-software-11501",
  storageBucket: "vnu-business-software-11501.firebasestorage.app",
  messagingSenderId: "422671793777",
  appId: "1:422671793777:web:dfa1d400c17a80daf025d0",
  measurementId: "G-CZVC62B1PV"
};

let firebaseApp = null;
let firebaseAuth = null;
let firestoreDb = null;
let isFirebaseAvailable = false;
let currentFirebaseUser = null;
let isTeacherUser = false;
let studentWorksData = [];
let currentWorksFilter = 'all';

// Authorized Teacher Emails
const TEACHER_EMAILS = [
  'kevin87332000',
  'kevin87332000@gmail.com',
  'jimchiu',
  'jimchiu@mail.vnu.edu.tw',
  'vnuemba@gmail.com',
  'h12s12bs',
  'h12s12bs@gmail.com'
];

// Global State
const state = {
  curriculum: null,
  agentTemplates: [],
  ipasGuide: null,
  questions: [],
  vibeGuide: null,
  onlineResources: null,
  currentTab: 'orientation',
  currentWeekFilter: 'all',
  selectedAgentId: 'word_document_agent',
  isSimulatingAgent: false,
  // Exam State
  exam: {
    active: false,
    questions: [],
    currentIndex: 0,
    answers: {},
    timerInterval: null,
    remainingSeconds: 0,
    examType: '',
    title: ''
  },
  // Slide Presenter State
  presenter: {
    isOpen: false,
    currentWeek: 1,
    currentSlideIdx: 0,
    fontSizeOffset: 0,
    isNotesOpen: false,
    isOutlineOpen: false
  },
  mistakeIds: JSON.parse(localStorage.getItem('vnu_bsa_mistakes') || '[]'),
  earnedBadges: JSON.parse(localStorage.getItem('vnu_bsa_badges') || '["badge_newbie"]'),
  student: JSON.parse(localStorage.getItem('vnu_bsa_student') || '{"id": "進企管四系1甲", "name": "同學"}')
};

// Initialize Platform
document.addEventListener('DOMContentLoaded', async () => {
  initStudentInfo();
  loadDefaultSampleWorks();
  initFirebase();
  await loadPlatformData();
  setupNavigation();
  setupKeyboardShortcuts();
  setupTouchSwipeListeners();
  renderAllSections();
  checkSystemStatus();
});

// Load Data (Hybrid online/offline)
async function loadPlatformData() {
  // Check if offline embedded data exists
  if (window.OFFLINE_DATA) {
    state.curriculum = window.OFFLINE_DATA.curriculum;
    state.agentTemplates = window.OFFLINE_DATA.agentTemplates;
    state.ipasGuide = window.OFFLINE_DATA.ipasGuide;
    state.questions = window.OFFLINE_DATA.questions;
    state.vibeGuide = window.OFFLINE_DATA.vibeGuide;
    state.onlineResources = window.OFFLINE_DATA.onlineResources;
    console.log("Loaded offline embedded dataset.");
    return;
  }

  try {
    const [currRes, agentRes, ipasRes, qRes, vibeRes, demoRes] = await Promise.all([
      fetch('/api/curriculum').then(r => r.json()),
      fetch('/api/agent_templates').then(r => r.json()),
      fetch('/api/ipas_guide').then(r => r.json()),
      fetch('/api/questions?count=300&shuffle=false').then(r => r.json()),
      fetch('/api/vibe_guide').then(r => r.json()).catch(() => null),
      fetch('/api/online_resources').then(r => r.json()).catch(() => null)
    ]);
    state.curriculum = currRes;
    state.agentTemplates = agentRes;
    state.ipasGuide = ipasRes;
    state.questions = qRes.questions || [];
    state.vibeGuide = vibeRes;
    state.onlineResources = demoRes;
    console.log("Loaded online dataset from Flask API.");
  } catch (err) {
    console.warn("Fetch from server failed, falling back to window objects:", err);
  }
}

function initStudentInfo() {
  const display = document.getElementById('studentDisplay');
  if (display) {
    display.textContent = `${state.student.id} ｜ ${state.student.name}`;
  }
}

function updateStudentProfile() {
  const newId = prompt("請輸入您的學號或班級代碼：", state.student.id);
  if (newId) state.student.id = newId.trim();
  const newName = prompt("請輸入您的姓名：", state.student.name);
  if (newName) state.student.name = newName.trim();
  localStorage.setItem('vnu_bsa_student', JSON.stringify(state.student));
  initStudentInfo();
  renderAchievements();
}

async function checkSystemStatus() {
  try {
    const res = await fetch('/api/system_info');
    if (res.ok) {
      const data = await res.json();
      const statusText = document.getElementById('networkStatusText');
      if (statusText) {
        statusText.innerHTML = `已連線 ｜ 投影網址：<a href="${data.classroom_url}" target="_blank" style="color:#38bdf8; text-decoration:underline;">${data.classroom_url}</a>`;
      }
      return;
    }
  } catch (e) {
    // API not reachable, check environment
  }
  const statusText = document.getElementById('networkStatusText');
  if (statusText) {
    if (location.hostname.includes('github.io')) {
      statusText.innerHTML = '已連線 ｜ <span style="color:#38bdf8; font-weight:700;">GitHub Pages 雲端版</span>';
    } else {
      statusText.textContent = "單機離線免安裝模式";
    }
  }
}

// Navigation Tabs
function setupNavigation() {
  const navButtons = document.querySelectorAll('.nav-tab-btn');
  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      if (target === 'presenter') {
        openSlidePresenter(1, 0);
        return;
      }
      switchTab(target);
    });
  });
}

function switchTab(tabId) {
  if (tabId === 'teacher' && !isTeacherUser) {
    alert("⚠️ 「教師成績管理」僅限授課教師（邱俊維 博士）使用！\n請先以授課教師 Google 帳號登入。");
    return;
  }
  state.currentTab = tabId;
  document.querySelectorAll('.nav-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tabId);
  });
  document.querySelectorAll('.content-section').forEach(sec => {
    sec.classList.toggle('active', sec.id === `sec-${tabId}`);
  });
  if (tabId === 'submissions') {
    updateUploadFormStudentInfo();
    renderStudentWorks(currentWorksFilter);
  } else if (tabId === 'teacher') {
    renderTeacherGradeDashboard();
  } else if (tabId === 'vibe') {
    renderVibeCodingSection();
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render All Sections
function renderAllSections() {
  renderOrientationSection();
  renderVibeCodingSection();
  renderCurriculumSection();
  renderAgentStudioSection();
  renderIpasGuideSection();
  renderAchievements();
  renderStudentWorks();
}

// -------------------------------------------------------------
// SECTION 1: 第一週導論與個人介紹 (Orientation)
// -------------------------------------------------------------
function renderOrientationSection() {
  if (!state.curriculum) return;
  const { instructor, teaching_methodology, grading_policy, course_info } = state.curriculum;

  // Course Info & Instructor Card
  const profContainer = document.getElementById('instructorProfileBox');
  if (profContainer) {
    const emailLinks = instructor.email.split('｜').map(em => em.trim()).map(em => `<a href="mailto:${em}" style="color:#2563eb; text-decoration:none;">${em}</a>`).join(' ｜ ');
    
    profContainer.innerHTML = `
      <div class="profile-container">
        <div class="profile-avatar-box">
          邱俊維
          <span class="sub">助理教授</span>
        </div>
        <div class="profile-info">
          <div class="profile-name">${instructor.name}</div>
          <div class="profile-role">${instructor.title} ｜ ${instructor.degrees}</div>
          <div class="profile-item"><strong>授課班級：</strong><span style="color:#dc2626; font-weight:700;">${course_info.target_class}</span></div>
          <div class="profile-item"><strong>上課時間：</strong><span>${course_info.time}</span></div>
          <div class="profile-item"><strong>教室位置：</strong><span>${course_info.classroom}</span></div>
          <div class="profile-item"><strong>研究室：</strong><span>${instructor.office}</span></div>
          <div class="profile-item"><strong>諮詢時間：</strong><span style="color:#059669; font-weight:600;">${instructor.office_hours}</span></div>
          <div class="profile-item"><strong>聯絡信箱：</strong><span>${emailLinks}</span></div>
          ${instructor.phone ? `<div class="profile-item"><strong>聯絡電話：</strong><span>${instructor.phone}</span></div>` : ''}
          ${instructor.portfolio_website ? `<div class="profile-item"><strong>個人網站：</strong><span><a href="${instructor.portfolio_website}" target="_blank" style="color:#2563eb; text-decoration:underline; font-weight:600;">邱俊維 博士 專屬學術與實務專長網頁 ↗</a></span></div>` : ''}
          <div class="profile-item" style="margin-top:8px;"><strong>專長領域：</strong><span>${instructor.expertise.join(' ｜ ')}</span></div>
        </div>
      </div>
      <div style="margin-top: 16px; padding-top: 14px; border-top: 1px dashed var(--border-color); font-size: 13.5px; color: #475569;">
        <strong style="color:var(--primary-navy); display:block; margin-bottom:8px; font-size:14px;">🏢 經歷與專案成果（依據個人官方網站）：</strong>
        <div style="display:flex; flex-direction:column; gap:10px;">
          ${instructor.experience ? instructor.experience.map(exp => `
            <div style="background:#f8fafc; border-left:3px solid var(--accent-blue); padding:8px 12px; border-radius:4px;">
              <div style="font-weight:700; color:#1e293b; font-size:13.5px;">${exp.role} ｜ <span style="color:#64748b; font-weight:500;">${exp.org}</span></div>
              <div style="font-size:13px; color:#475569; margin-top:3px; line-height:1.5;">${exp.desc}</div>
            </div>
          `).join('') : `<div>${instructor.industry_experience}</div>`}
        </div>
      </div>
    `;
  }

  // OBE 4 Stages
  const obeContainer = document.getElementById('obeStagesBox');
  if (obeContainer) {
    obeContainer.innerHTML = `
      <div class="obe-flow">
        ${teaching_methodology.four_stages.map(st => `
          <div class="obe-step">
            <div class="obe-step-num">${st.stage.split(' ')[0]}</div>
            <div class="obe-step-title">${st.stage.split(' ')[1]}</div>
            <div class="obe-step-time">⏱️ ${st.time}</div>
            <div class="obe-step-desc">${st.description}</div>
          </div>
        `).join('')}
      </div>
      <div style="background:#f1f5f9; padding:14px 18px; border-radius:10px; margin-top:14px; font-size:13.5px;">
        <strong style="color:var(--primary-navy);">人機協同四大基石：</strong>
        <ul style="margin-left: 20px; margin-top: 6px; color:#334155;">
          ${teaching_methodology.collaboration_principles.map(p => `<li style="margin-bottom:4px;">${p}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  // Grading Breakdown & iPAS Bonus
  const gradeContainer = document.getElementById('gradingPolicyBox');
  if (gradeContainer) {
    gradeContainer.innerHTML = `
      <div style="background:#f0fdf4; border:1.5px solid #86efac; border-left:6px solid #16a34a; border-radius:10px; padding:14px 18px; margin-bottom:16px;">
        <div style="font-weight:800; color:#166534; font-size:15px; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
          <i class="fas fa-shield-alt"></i> 學習安心承諾：公平透明、注重實務累積
        </div>
        <div style="font-size:13.5px; color:#14532d; line-height:1.7;">
          • <strong>無上機考試</strong>：免受限於電腦教室限時測驗壓力，期中與期末皆採「繳交個人專案報告」評核。<br>
          • <strong>無每週隨堂作業負擔</strong>：課堂全心專注於實機演練與觀念吸收，不收每週隨堂作業。<br>
          • <strong>個人獨立完成</strong>：不分組、不分工，同學各自依步調完成專屬作品。
        </div>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px; margin-bottom:16px;">
        ${grading_policy.breakdown.map(b => `
          <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:10px; padding:16px; border-left:5px solid var(--primary-blue); box-shadow:0 2px 6px rgba(0,0,0,0.02);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:800; color:var(--primary-navy); font-size:16px;">${b.item}</span>
              <span style="font-size:22px; font-weight:900; color:var(--accent-amber);">${b.percentage}</span>
            </div>
            <div style="font-size:13px; color:#64748b; margin-top:8px; line-height:1.5;">${b.description}</div>
          </div>
        `).join('')}
      </div>
      <div style="background:linear-gradient(135deg, #fffbeb, #fef3c7); border:1.5px solid #f59e0b; border-radius:12px; padding:18px 22px;">
        <h4 style="color:#b45309; font-weight:800; font-size:16px; margin-bottom:8px;">${grading_policy.ipas_bonus.title}</h4>
        <ul style="margin-left:20px; color:#78350f; font-size:14px;">
          ${grading_policy.ipas_bonus.rules.map(r => `<li style="margin-bottom:4px;">${r}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  // Rubrics Table
  const rubricsContainer = document.getElementById('rubricsTableBox');
  if (rubricsContainer) {
    rubricsContainer.innerHTML = `
      <table class="rubric-table">
        <thead>
          <tr>
            <th>評量向度 (權重)</th>
            <th>極佳 (90-100分)</th>
            <th>良好 (80-89分)</th>
            <th>尚可 (70-79分)</th>
            <th>待加強 (&lt;70分)</th>
          </tr>
        </thead>
        <tbody>
          ${grading_policy.rubrics.map(r => `
            <tr>
              <td class="dim-title">${r.dimension}</td>
              <td style="color:#166534; background:#f0fdf4;">${r.exemplary}</td>
              <td style="color:#1e3a8a;">${r.proficient}</td>
              <td style="color:#854d0e;">${r.developing}</td>
              <td style="color:#991b1b; background:#fef2f2;">${r.unsatisfactory}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }
}

// -------------------------------------------------------------
// SECTION: Vibe Coding 與線上示範資源 (Vibe Coding & Demo Datasets)
// -------------------------------------------------------------
function renderVibeCodingSection() {
  renderOnlineResourcesBox();
  renderVibeGuideBox();
}

function renderOnlineResourcesBox() {
  const container = document.getElementById('onlineDemoResourcesBox');
  if (!container) return;

  const data = state.onlineResources;
  if (!data || !data.resources) {
    container.innerHTML = `
      <div class="card">
        <div style="color:#64748b; font-size:14px; text-align:center; padding:20px;">
          載入示範檔案中...
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="card" style="border-top: 4px solid #0284c7; margin-bottom:24px;">
      <div class="card-header">
        <span class="card-title">📂 課堂線上示範檔案庫與 Agentic AI 實戰專區 (Live Business Datasets & AI Agents)</span>
        <span class="card-badge" style="background:#e0f2fe; color:#0369a1;">5 大權威實務檔案</span>
      </div>
      <p style="font-size:14px; color:#475569; line-height:1.6; margin-bottom:20px;">
        ${data.description}
      </p>

      <div style="display:flex; flex-direction:column; gap:24px;">
        ${data.resources.map((res, idx) => `
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:12px; padding:20px; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                  <span style="font-size:12px; font-weight:800; background:#0284c7; color:#fff; padding:3px 10px; border-radius:6px;">
                    範例 ${idx + 1} ｜ ${res.category}
                  </span>
                  <span style="font-size:11px; font-weight:700; background:#e2e8f0; color:#334155; padding:2px 8px; border-radius:4px;">
                    ${res.type ? res.type.toUpperCase() : 'FILE'}
                  </span>
                </div>
                <strong style="font-size:17px; color:#0f172a; display:block; margin-bottom:4px;">${res.name}</strong>
                <div style="font-size:12px; color:#64748b;">
                  <i class="fas fa-database"></i> 來源：${res.source} ｜ 實體檔名：<code>${res.filename}</code>
                </div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${res.download_url ? `
                  <a href="${res.download_url}" download class="btn-sm" style="background:#059669; color:#fff; text-decoration:none; padding:7px 14px; border-radius:6px; font-weight:700; display:inline-flex; align-items:center; gap:6px; font-size:12px;">
                    <i class="fas fa-download"></i> 下載檔案 (${res.file_size || '點擊下載'})
                  </a>
                ` : ''}
                ${res.raw_preview ? `
                  <button class="btn-sm btn-primary" onclick="copyOnlineResourceText('${res.id}')" style="padding:7px 12px; font-size:12px;">
                    <i class="fas fa-copy"></i> 複製原始預覽
                  </button>
                ` : ''}
              </div>
            </div>

            <p style="font-size:13px; color:#334155; line-height:1.6; margin-bottom:14px;">
              ${res.description}
            </p>

            ${res.traditional_bottleneck || res.agentic_ai_workflow ? `
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin-bottom:16px;">
                <div style="background:#fff1f2; border:1px solid #fecdd3; border-radius:8px; padding:12px 14px;">
                  <div style="font-size:12px; font-weight:800; color:#be123c; margin-bottom:4px;">
                    <i class="fas fa-hand-paper"></i> 過去傳統純手動操作痛點
                  </div>
                  <div style="font-size:12px; color:#881337; line-height:1.5;">
                    ${res.traditional_bottleneck}
                  </div>
                </div>
                <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px 14px;">
                  <div style="font-size:12px; font-weight:800; color:#15803d; margin-bottom:4px;">
                    <i class="fas fa-robot"></i> 現代 Agentic AI 代理人工作流
                  </div>
                  <div style="font-size:12px; color:#14532d; line-height:1.5;">
                    ${res.agentic_ai_workflow}
                  </div>
                </div>
              </div>
            ` : ''}

            ${res.raw_preview ? `
              <div style="position:relative; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <div style="font-size:11px; font-weight:700; color:#475569; text-transform:uppercase;">
                    <i class="fas fa-table"></i> 真實數據結構預覽 (Data Preview)：
                  </div>
                  <span style="font-size:11px; color:#94a3b8;">可橫向滾動查看</span>
                </div>
                <textarea id="raw_${res.id}" readonly style="width:100%; height:110px; font-family:Consolas, Monaco, monospace; font-size:12px; line-height:1.5; background:#0f172a; color:#f8fafc; border-radius:6px; padding:10px; border:1px solid #334155; resize:vertical; white-space:pre;">${res.raw_preview}</textarea>
              </div>
            ` : ''}

            <div style="background:#eff6ff; border:1px dashed #60a5fa; border-radius:8px; padding:14px 16px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:13px; font-weight:800; color:#1d4ed8;">
                  <i class="fas fa-terminal"></i> 學生操作 Agentic AI 指令模板 (CLEAR Prompt Template)
                </span>
                <button class="btn-sm" onclick="copyOnlineResourcePrompt('${res.id}')" style="background:#2563eb; color:#fff; border:none; padding:4px 12px; font-size:12px; border-radius:6px; cursor:pointer; font-weight:700;">
                  <i class="fas fa-clone"></i> 一鍵複製 Prompt
                </button>
              </div>
              <pre id="prompt_${res.id}" style="font-size:12px; color:#1e3a8a; line-height:1.6; white-space:pre-wrap; word-break:break-word; margin:0; font-family:Consolas, Monaco, monospace; background:#ffffff; padding:12px; border-radius:6px; border:1px solid #bfdbfe;">${res.ai_prompt_suggestion}</pre>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function renderVibeGuideBox() {
  const container = document.getElementById('vibeGuideContentBox');
  if (!container) return;

  const data = state.vibeGuide;
  if (!data || !data.sections) {
    container.innerHTML = `
      <div class="card">
        <div style="color:#64748b; font-size:14px; text-align:center; padding:20px;">
          載入 Vibe Coding 操作指南中...
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div style="display:flex; flex-direction:column; gap:24px;">
      ${data.sections.map(sec => `
        <div class="card" id="${sec.id}" style="border-top:4px solid #4f46e5;">
          <div class="card-header">
            <span class="card-title">
              <i class="${sec.icon}" style="color:#4f46e5; margin-right:8px;"></i>
              ${sec.num}、${sec.title}
            </span>
            <span class="card-badge" style="background:#e0e7ff; color:#3730a3;">操作指南</span>
          </div>

          ${sec.content ? `
            <div style="display:flex; flex-direction:column; gap:14px; margin-top:8px;">
              ${sec.content.map(c => `
                <div style="background:#f8fafc; border-left:3px solid #6366f1; border-radius:6px; padding:12px 16px;">
                  <strong style="font-size:15px; color:#1e1b4b; display:block; margin-bottom:6px;">${c.heading}</strong>
                  <p style="font-size:14px; color:#334155; line-height:1.65; margin:0; white-space:pre-line;">${c.text}</p>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.clear_framework ? `
            <div style="overflow-x:auto; margin-top:14px;">
              <table class="rubric-table">
                <thead>
                  <tr>
                    ${sec.table_headers.map(th => `<th>${th}</th>`).join('')}
                  </tr>
                </thead>
                <tbody>
                  ${sec.clear_framework.map(cf => `
                    <tr>
                      <td style="font-weight:900; font-size:18px; color:#4f46e5; text-align:center;">${cf.letter}</td>
                      <td><strong>${cf.name}</strong></td>
                      <td style="color:#475569;">${cf.desc}</td>
                      <td style="background:#f0fdf4; color:#166534; font-size:13px;">${cf.example}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          ` : ''}

          ${sec.steps ? `
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:14px;">
              ${sec.steps.map(step => `
                <div style="background:#f1f5f9; border-left:4px solid #8b5cf6; padding:12px 16px; border-radius:6px; font-size:14px; color:#1e293b; line-height:1.6;">
                  ${step}
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.demo_prompt ? `
            <div style="margin-top:14px; background:#0f172a; border-radius:8px; padding:16px; position:relative;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="color:#38bdf8; font-size:12px; font-weight:800;">
                  <i class="fas fa-terminal"></i> 教師示範提示詞 (Live Demo Prompt)
                </span>
                <button class="btn-sm" onclick="copyVibeDemoPrompt()" style="background:#38bdf8; color:#0f172a; font-weight:700; border:none; padding:4px 12px; border-radius:4px; cursor:pointer;">
                  <i class="fas fa-copy"></i> 一鍵複製提示詞
                </button>
              </div>
              <pre id="vibeDemoPromptText" style="color:#f8fafc; font-family:Consolas, Monaco, monospace; font-size:13px; line-height:1.6; white-space:pre-wrap; margin:0;">${sec.demo_prompt}</pre>
            </div>
          ` : ''}

          ${sec.faqs ? `
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:14px; margin-top:14px;">
              ${sec.faqs.map(faq => `
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:14px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="font-weight:800; font-size:14px; color:#b91c1c; margin-bottom:6px;">
                    ${faq.q}
                  </div>
                  <div style="font-size:13px; color:#334155; line-height:1.6;">
                    ${faq.a}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}
        </div>
      `).join('')}
    </div>
  `;
}

// Clipboard Helper Functions for Online Resources
function copyOnlineResourceText(resId) {
  const el = document.getElementById(`raw_${resId}`);
  if (el) {
    copyTextToClipboard(el.value, "原始檔案內容已成功複製到剪貼簿！");
  }
}

function copyOnlineResourcePrompt(resId) {
  const el = document.getElementById(`prompt_${resId}`);
  if (el) {
    copyTextToClipboard(el.innerText, "AI 提示詞已複製！可直接貼給免費版 Antigravity 或 Gemini。");
  }
}

function copyVibeDemoPrompt() {
  const el = document.getElementById('vibeDemoPromptText');
  if (el) {
    copyTextToClipboard(el.innerText, "教師示範提示詞已成功複製到剪貼簿！");
  }
}

function copyTextToClipboard(text, successMsg) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg || "複製成功！");
    }).catch(() => {
      fallbackCopyText(text, successMsg);
    });
  } else {
    fallbackCopyText(text, successMsg);
  }
}

function fallbackCopyText(text, successMsg) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.opacity = "0";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    showToast(successMsg || "複製成功！");
  } catch (err) {
    alert("複製失敗，請手動選取文字複製。");
  }
  document.body.removeChild(textArea);
}

function showToast(msg) {
  let toast = document.getElementById('customToastBox');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'customToastBox';
    toast.style.cssText = 'position:fixed; bottom:28px; right:28px; background:#0f172a; color:#f8fafc; padding:12px 20px; border-radius:8px; font-size:14px; font-weight:700; z-index:9999; box-shadow:0 10px 25px rgba(0,0,0,0.3); border-left:4px solid #10b981; transition:all 0.3s ease; opacity:0; transform:translateY(20px); pointer-events:none;';
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<i class="fas fa-check-circle" style="color:#10b981; margin-right:8px;"></i>${msg}`;
  toast.style.opacity = '1';
  toast.style.transform = 'translateY(0)';
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';
  }, 2500);
}

// Bind to window for inline onclick handlers
window.copyOnlineResourceText = copyOnlineResourceText;
window.copyOnlineResourcePrompt = copyOnlineResourcePrompt;
window.copyVibeDemoPrompt = copyVibeDemoPrompt;
window.copyTextToClipboard = copyTextToClipboard;

// -------------------------------------------------------------
// SECTION 2: 18 週教學地圖與簡報連動 (Curriculum)
// -------------------------------------------------------------
function renderCurriculumSection() {
  if (!state.curriculum) return;
  const container = document.getElementById('weeklyCardsList');
  if (!container) return;

  const weeks = state.curriculum.weeks;
  container.innerHTML = weeks.map(w => `
    <div class="week-card" data-module="${w.module}">
      <div class="week-header-row">
        <div>
          <div class="week-badge-box">
            <span class="week-number-badge">第 ${String(w.week).padStart(2, '0')} 週</span>
            <span class="week-module-text">${w.module}</span>
          </div>
          <h3 class="week-title">${w.title}</h3>
          <div class="week-subtitle">${w.subtitle}</div>
        </div>
        <div class="week-actions">
          ${w.download_file ? `
            <a href="${w.download_file.url}" download="${w.download_file.filename}" class="btn-sm" style="background:#059669; color:#ffffff; text-decoration:none; display:inline-flex; align-items:center; gap:6px; font-weight:700; border-radius:6px; padding:6px 12px; font-size:13px; box-shadow:0 1px 2px rgba(0,0,0,0.1);">
              📥 下載本週練習檔 (${w.download_file.ext})
            </a>
          ` : ''}
          <button class="btn-sm btn-amber" onclick="openSlidePresenter(${w.week}, 0)">
            🖥️ 播放本週簡報 (61頁)
          </button>
          <button class="btn-sm btn-primary" onclick="startQuickQuiz(${w.week})">
            💡 課堂觀念導讀 (5則)
          </button>
        </div>
      </div>
      <div class="week-body-grid">
        <div class="week-info-block">
          <strong>實務情境與瓶頸引導 (Hook)</strong>
          <div>${w.hook}</div>
        </div>
        <div class="week-info-block">
          <strong>核心觀念心法 (Concept)</strong>
          <div>${w.concept}</div>
        </div>
        <div class="week-info-block">
          <strong>電腦教室實機 SOP (Practice)</strong>
          <div>${w.practice}</div>
        </div>
        <div class="week-info-block">
          <strong>實務應用與成果指標 (Wrap-up)</strong>
          <div>${w.wrapup}</div>
        </div>
      </div>
      ${w.download_file ? `
        <div style="margin-top:12px; padding:10px 14px; background:#ecfdf5; border-left:4px solid #10b981; border-radius:6px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
          <div style="font-size:13px; color:#065f46;">
            <strong>📄 本週練習素材：</strong>${w.download_file.filename}
            <div style="font-size:12px; color:#047857; margin-top:2px;">${w.download_file.description}</div>
          </div>
          <a href="${w.download_file.url}" download="${w.download_file.filename}" class="btn-sm" style="background:#059669; color:#ffffff; text-decoration:none; display:inline-flex; align-items:center; gap:4px; font-weight:600; padding:5px 12px; font-size:12px; border-radius:4px;">
            📥 立即下載 (.docx)
          </a>
        </div>
      ` : ''}
      <div style="margin-top:14px;">
        <div style="font-size:12px; font-weight:700; color:#0284c7; margin-bottom:4px;">
          🎯 iPAS 認證對標考點：${w.ipas_mapping}
        </div>
        <div class="prompt-box">
          <button class="btn-copy" onclick="copyPrompt('${encodeURIComponent(w.prompt_example)}')">📋 複製提示詞</button>
          ${w.prompt_example}
        </div>
      </div>
    </div>
  `).join('');
}

function filterCurriculumModule(modName, btn) {
  document.querySelectorAll('.module-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  const cards = document.querySelectorAll('.week-card');
  cards.forEach(card => {
    if (modName === 'all' || card.dataset.module.includes(modName)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

function copyPrompt(encodedText) {
  const text = decodeURIComponent(encodedText);
  navigator.clipboard.writeText(text).then(() => {
    alert("提示詞已成功複製至剪貼簿！可直接貼入 AI 工具使用。");
  }).catch(() => {
    prompt("請手動複製以下提示詞：", text);
  });
}

// -------------------------------------------------------------
// SECTION 3: Agentic AI 商業實戰沙盒 (AI Studio)
// -------------------------------------------------------------
function renderAgentStudioSection() {
  const selector = document.getElementById('agentSelectorBox');
  if (!selector || !state.agentTemplates) return;

  selector.innerHTML = state.agentTemplates.map(ag => `
    <div class="agent-card ${ag.id === state.selectedAgentId ? 'active' : ''}" onclick="selectAgent('${ag.id}')">
      <div class="agent-icon" style="background:${ag.badge_color};">
        <i class="${ag.icon}"></i>
      </div>
      <div class="agent-name">${ag.name}</div>
      <div class="agent-software">應用工具：${ag.target_software}</div>
      <div style="font-size:12px; color:#64748b; margin-top:6px;">${ag.category}</div>
    </div>
  `).join('');

  renderActiveAgentDetails();
}

function selectAgent(agentId) {
  state.selectedAgentId = agentId;
  document.querySelectorAll('.agent-card').forEach(c => {
    c.classList.remove('active');
  });
  renderAgentStudioSection();
}

function renderActiveAgentDetails() {
  const activeAgent = state.agentTemplates.find(a => a.id === state.selectedAgentId);
  if (!activeAgent) return;

  const detailBox = document.getElementById('activeAgentDetails');
  if (detailBox) {
    detailBox.innerHTML = `
      <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:12px; padding:24px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <h3 style="font-size:20px; font-weight:800; color:var(--primary-navy);">${activeAgent.name}</h3>
            <p style="font-size:14px; color:#475569; margin-top:4px;">${activeAgent.description}</p>
          </div>
          <button class="btn-sm btn-amber" style="padding:10px 20px; font-size:15px; font-weight:800;" onclick="runAgentSimulation()">
            🚀 啟動 Agent 自主執行與推理
          </button>
        </div>
        <div style="margin-top:16px; background:#f8fafc; padding:14px; border-radius:8px; border-left:4px solid ${activeAgent.badge_color};">
          <strong style="color:var(--primary-navy);">觸發情境 (Trigger)：</strong>${activeAgent.trigger}
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px;">
          <div style="background:#f8fafc; padding:14px; border-radius:8px;">
            <strong style="color:var(--primary-navy); display:block; margin-bottom:6px;">🛠️ 可用工具 (Tools Calling)：</strong>
            <ul style="font-size:13px; color:#334155; margin-left:18px;">
              ${activeAgent.tools_available.map(t => `<li style="margin-bottom:4px;"><code>${t.name}</code>: ${t.desc}</li>`).join('')}
            </ul>
          </div>
          <div style="background:#f8fafc; padding:14px; border-radius:8px;">
            <strong style="color:#b91c1c; display:block; margin-bottom:6px;">🛡️ 安全防護欄 (Guardrails)：</strong>
            <ul style="font-size:13px; color:#334155; margin-left:18px;">
              ${activeAgent.guardrails.map(g => `<li style="margin-bottom:4px;">${g}</li>`).join('')}
            </ul>
          </div>
        </div>
      </div>
    `;
  }
}

async function runAgentSimulation() {
  if (state.isSimulatingAgent) return;
  state.isSimulatingAgent = true;

  const terminalBody = document.getElementById('reactTerminalBody');
  terminalBody.innerHTML = `<div style="color:#94a3b8; font-style:italic;">⚡ Agentic AI 推理引擎啟動中... 正在載入情境與工具集...</div>`;

  let trace = [];
  const activeAgent = state.agentTemplates.find(a => a.id === state.selectedAgentId);

  if (activeAgent && activeAgent.simulated_trace) {
    trace = activeAgent.simulated_trace;
  } else {
    try {
      const res = await fetch('/api/simulate_agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template_id: state.selectedAgentId })
      });
      const data = await res.json();
      trace = data.trace || [];
    } catch (e) {
      console.warn("API simulation fallback");
    }
  }

  terminalBody.innerHTML = '';
  for (let i = 0; i < trace.length; i++) {
    const step = trace[i];
    await new Promise(r => setTimeout(r, 650));
    renderTerminalStep(terminalBody, step);
    terminalBody.scrollTop = terminalBody.scrollHeight;
  }

  state.isSimulatingAgent = false;
  unlockBadge('badge_react_master');
}

function renderTerminalStep(container, step) {
  const div = document.createElement('div');
  div.className = `step-row step-${step.type}`;

  let label = 'THOUGHT';
  if (step.type === 'action') label = `ACTION: ${step.tool || ''}`;
  else if (step.type === 'observation') label = 'OBSERVATION';
  else if (step.type === 'guardrail') label = 'GUARDRAIL AUDIT';
  else if (step.type === 'human_in_the_loop') label = 'HUMAN-IN-THE-LOOP';
  else if (step.type === 'final_output') label = 'DELIVERABLE COMPLETE';

  let contentHtml = step.content || '';
  if (step.type === 'action' && step.input) {
    contentHtml = `<div>${contentHtml}</div><pre style="margin-top:4px; font-size:12px; background:rgba(0,0,0,0.3); padding:6px; border-radius:4px;">${JSON.stringify(step.input, null, 2)}</pre>`;
  } else if (step.type === 'observation' && step.result) {
    contentHtml = `<div>${step.result}</div>`;
  }

  div.innerHTML = `<span class="step-badge">${label}</span> ${contentHtml}`;
  container.appendChild(div);
}

async function runCustomScenarioSim() {
  const input = document.getElementById('customScenarioInput');
  if (!input || !input.value.trim()) {
    alert("請先輸入您的商業流程情境或任務需求！");
    return;
  }
  const text = input.value.trim();
  const terminalBody = document.getElementById('reactTerminalBody');
  terminalBody.innerHTML = `<div style="color:#94a3b8; font-style:italic;">⚡ 正在為自訂商業情境規劃 Agentic 跨軟體協同任務...</div>`;

  try {
    const res = await fetch('/api/simulate_agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ custom_scenario: text })
    });
    const data = await res.json();
    const trace = data.trace || [];
    terminalBody.innerHTML = '';
    for (let i = 0; i < trace.length; i++) {
      await new Promise(r => setTimeout(r, 600));
      renderTerminalStep(terminalBody, trace[i]);
      terminalBody.scrollTop = terminalBody.scrollHeight;
    }
  } catch (e) {
    alert("自訂模擬需在連線伺服器模式下執行。");
  }
}

// -------------------------------------------------------------
// SECTION 4: iPAS AI 應用規劃師 證照專區與自我評量 (iPAS Zone)
// -------------------------------------------------------------
function renderIpasGuideSection() {
  if (!state.ipasGuide) return;
  const guideBox = document.getElementById('ipasGuideContent');
  if (!guideBox) return;

  const { cert_info, subjects, high_frequency_cheatsheet } = state.ipasGuide;
  guideBox.innerHTML = `
    <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:12px; padding:24px; margin-bottom:24px;">
      <h3 style="font-size:20px; font-weight:800; color:var(--primary-navy); margin-bottom:8px;">${cert_info.title}</h3>
      <p style="font-size:14px; color:#475569;">發證主管機關：<strong>${cert_info.issuing_body}</strong> ｜ 及格門檻：<strong>${cert_info.passing_score}</strong></p>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px; margin-top:16px;">
        ${subjects.map(s => `
          <div style="background:#f8fafc; border:1px solid var(--border-color); border-top:4px solid var(--primary-blue); border-radius:8px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:13px; font-weight:800; color:var(--primary-blue);">${s.code}</span>
              <span style="font-size:12px; font-weight:700; background:#e2e8f0; padding:2px 8px; border-radius:10px;">權重 ${s.weight}</span>
            </div>
            <h4 style="font-size:16px; font-weight:700; color:var(--primary-navy); margin:6px 0;">${s.name}</h4>
            <div style="font-size:13px; color:#475569; margin-top:8px;">
              ${s.key_topics.map(t => `<div style="margin-bottom:4px;">• <strong>${t.topic}</strong></div>`).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <div style="background:#f0fdf4; border:1.5px solid #22c55e; border-radius:12px; padding:20px; margin-bottom:24px;">
      <h4 style="color:#15803d; font-size:16px; font-weight:800; margin-bottom:10px;">⚡ iPAS AI 應用規劃師 核心觀念重點錦囊</h4>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:12px;">
        ${high_frequency_cheatsheet.map(c => `
          <div style="background:#ffffff; padding:10px 14px; border-radius:6px; font-size:13px; border:1px solid #bbf7d0;">
            <span style="font-weight:700; color:#166534;">${c.point}</span> ${c.detail}
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

// Start Concept Reviews (課堂觀念導讀與自主學習)
function startQuickQuiz(weekNum) {
  switchTab('ipas');
  startExam('weekly_5', `第 ${weekNum} 週 課堂重點觀念自我檢視 (5則)`, weekNum);
}

function startExamMode(mode) {
  if (mode === 'weekly_5') {
    const week = prompt("請選擇欲進行觀念自我檢視的週次 (1 到 18)：", "1");
    if (week && parseInt(week) >= 1 && parseInt(week) <= 18) {
      startExam('weekly_5', `第 ${week} 週 課堂重點觀念自我檢視 (5則)`, parseInt(week));
    }
  } else if (mode === 'chapter') {
    const mod = prompt("請選擇單元模組觀念主題 (如: Word, Excel, PPT, Agentic, 資安)：", "Excel");
    if (mod) startExam('chapter', `【${mod}】單元核心觀念精熟複習`, null, mod);
  } else if (mode === 'midterm_50') {
    if (confirm("即將開啟【期中 50 題核心觀念自我檢核】\n• 涵蓋第 1 至 9 週重點觀念\n• 本練習純供自我檢核學習吸收度，無成績壓力\n準備好立即開始？")) {
      startExam('midterm_50', "iPAS 期中 50 題核心觀念自我檢核 (無計分壓力)");
    }
  } else if (mode === 'final_100') {
    if (confirm("即將開啟【期末 100 題綜合觀念總回顧】\n• 涵蓋全學期 18 週題庫\n• 協助同學融會貫通並儲備考證實力\n準備好立即開始？")) {
      startExam('final_100', "iPAS 期末 100 題綜合觀念總回顧 (無計分壓力)");
    }
  }
}

function startExam(examType, title, weekFilter = null, moduleFilter = null) {
  let pool = [...state.questions];

  if (weekFilter) {
    pool = pool.filter(q => q.weeks && q.weeks.includes(weekFilter));
  } else if (moduleFilter) {
    pool = pool.filter(q => (q.module && q.module.includes(moduleFilter)) || (q.subject && q.subject.includes(moduleFilter)));
  } else if (examType === 'midterm_50') {
    pool = pool.filter(q => q.weeks && q.weeks.some(w => w <= 9));
  }

  // Shuffle pool
  pool.sort(() => Math.random() - 0.5);

  let count = 5;
  let durationMinutes = 10;
  if (examType === 'weekly_5') { count = 5; durationMinutes = 10; }
  else if (examType === 'chapter') { count = Math.min(pool.length, 15); durationMinutes = 20; }
  else if (examType === 'midterm_50') { count = Math.min(pool.length, 50); durationMinutes = 60; }
  else if (examType === 'final_100') { count = Math.min(pool.length, 100); durationMinutes = 100; }

  const selected = pool.slice(0, count);
  if (selected.length === 0) {
    alert("找不到符合條件的題目，請重新選擇！");
    return;
  }

  state.exam.active = true;
  state.exam.questions = selected;
  state.exam.currentIndex = 0;
  state.exam.answers = {};
  state.exam.examType = examType;
  state.exam.title = title;
  state.exam.remainingSeconds = durationMinutes * 60;

  // Toggle UI views
  document.getElementById('ipasIntroArea').style.display = 'none';
  document.getElementById('ipasExamArea').style.display = 'block';
  document.getElementById('ipasResultArea').style.display = 'none';

  startExamTimer();
  renderExamQuestion();
  renderExamSidebar();
}

function startExamTimer() {
  if (state.exam.timerInterval) clearInterval(state.exam.timerInterval);
  state.exam.timerInterval = setInterval(() => {
    state.exam.remainingSeconds--;
    updateTimerDisplay();
    if (state.exam.remainingSeconds <= 0) {
      clearInterval(state.exam.timerInterval);
      alert("作答時間截止！系統將自動為您交卷計分。");
      submitCurrentExam();
    }
  }, 1000);
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const display = document.getElementById('examTimerDisplay');
  if (!display) return;
  const mins = Math.floor(state.exam.remainingSeconds / 60);
  const secs = state.exam.remainingSeconds % 60;
  display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  if (state.exam.remainingSeconds <= 300) {
    display.style.color = '#ef4444';
  } else {
    display.style.color = '#f59e0b';
  }
}

function renderExamQuestion() {
  const container = document.getElementById('activeQuestionContainer');
  const q = state.exam.questions[state.exam.currentIndex];
  if (!q) return;

  const currentAns = state.exam.answers[q.id];

  container.innerHTML = `
    <div class="question-card">
      <div class="q-meta">
        <span class="q-subject-badge">${q.subject || 'iPAS 考科'}</span>
        <span class="q-module-badge">${q.module || '專業模組'}</span>
        <span style="font-size:12px; color:#94a3b8; margin-left:auto;">
          第 <strong>${state.exam.currentIndex + 1}</strong> / ${state.exam.questions.length} 題
        </span>
      </div>
      <div class="q-text">${q.id}. ${q.question}</div>
      <div class="options-list">
        ${q.options.map((opt, idx) => `
          <button class="opt-btn ${currentAns === idx ? 'selected' : ''}" onclick="selectExamOption(${q.id}, ${idx})">
            <span class="opt-index">${['A', 'B', 'C', 'D'][idx]}</span>
            <span>${opt}</span>
          </button>
        `).join('')}
      </div>
      <div style="display:flex; justify-content:space-between; margin-top:24px; padding-top:16px; border-top:1px solid var(--border-color);">
        <button class="btn-sm" onclick="navExamQuestion(-1)" ${state.exam.currentIndex === 0 ? 'disabled' : ''}>
          ⬅ 上一題
        </button>
        <button class="btn-sm btn-primary" onclick="navExamQuestion(1)" ${state.exam.currentIndex === state.exam.questions.length - 1 ? 'disabled' : ''}>
          下一題 ➔
        </button>
      </div>
    </div>
  `;
}

function selectExamOption(qId, optIdx) {
  state.exam.answers[qId] = optIdx;
  renderExamQuestion();
  renderExamSidebar();
}

function navExamQuestion(delta) {
  const next = state.exam.currentIndex + delta;
  if (next >= 0 && next < state.exam.questions.length) {
    state.exam.currentIndex = next;
    renderExamQuestion();
    renderExamSidebar();
  }
}

function jumpToExamQuestion(index) {
  state.exam.currentIndex = index;
  renderExamQuestion();
  renderExamSidebar();
}

function renderExamSidebar() {
  const titleElem = document.getElementById('examTitleDisplay');
  if (titleElem) titleElem.textContent = state.exam.title;

  const grid = document.getElementById('examNavGrid');
  if (!grid) return;

  grid.innerHTML = state.exam.questions.map((q, idx) => {
    const isAnswered = state.exam.answers[q.id] !== undefined;
    const isCurrent = idx === state.exam.currentIndex;
    return `
      <button class="q-nav-btn ${isAnswered ? 'answered' : ''} ${isCurrent ? 'current' : ''}" onclick="jumpToExamQuestion(${idx})">
        ${idx + 1}
      </button>
    `;
  }).join('');
}

function submitCurrentExam() {
  const answeredCount = Object.keys(state.exam.answers).length;
  const total = state.exam.questions.length;
  if (answeredCount < total) {
    if (!confirm(`您尚有 ${total - answeredCount} 題未作答，確定要現在交卷嗎？`)) {
      return;
    }
  }

  if (state.exam.timerInterval) clearInterval(state.exam.timerInterval);

  // Score calculation
  let correctCount = 0;
  const moduleStats = {};
  const details = [];

  state.exam.questions.forEach(q => {
    const userAns = state.exam.answers[q.id];
    const isCorrect = (userAns === q.answer);
    if (isCorrect) correctCount++;

    const mod = q.module || '綜合模組';
    if (!moduleStats[mod]) moduleStats[mod] = { total: 0, correct: 0 };
    moduleStats[mod].total++;
    if (isCorrect) moduleStats[mod].correct++;

    // Record mistakes in notebook
    if (!isCorrect) {
      if (!state.mistakeIds.includes(q.id)) {
        state.mistakeIds.push(q.id);
      }
    } else {
      // If correct, remove from mistakeIds if was there
      state.mistakeIds = state.mistakeIds.filter(id => id !== q.id);
    }

    details.push({
      id: q.id,
      question: q.question,
      options: q.options,
      user_answer: userAns,
      correct_answer: q.answer,
      is_correct: isCorrect,
      explanation: q.explanation,
      module: mod
    });
  });

  localStorage.setItem('vnu_bsa_mistakes', JSON.stringify(state.mistakeIds));

  const score = Math.round((correctCount / total) * 1000) / 10;
  const passed = score >= 70.0;

  // Unlock badges
  if (passed) {
    unlockBadge('badge_ipas_pass');
    if (score >= 90) unlockBadge('badge_top_scorer');
  }

  // Show results
  renderExamResults({ score, correctCount, total, passed, moduleStats, details });
}

function renderExamResults(result) {
  document.getElementById('ipasExamArea').style.display = 'none';
  const resultArea = document.getElementById('ipasResultArea');
  resultArea.style.display = 'block';

  const badgeColor = result.passed ? '#059669' : '#e11d48';
  const badgeText = result.passed ? '🎉 恭喜通過！達到 iPAS 專業及格標準 (≥70分)' : '💪 尚未達標，請檢閱下方解析並加強弱點模組！';

  resultArea.innerHTML = `
    <div class="result-header">
      <h2 style="font-size:24px; font-weight:800;">${state.exam.title} 測驗成果報告</h2>
      <div class="score-display">${result.score}<span style="font-size:24px; color:#ffffff;"> 分</span></div>
      <div style="font-size:16px; font-weight:700; color:${result.passed ? '#86efac' : '#fca5a5'};">
        ${badgeText}
      </div>
      <div style="margin-top:10px; font-size:14px; opacity:0.9;">
        答對 <strong>${result.correctCount}</strong> 題 ｜ 總題數 <strong>${result.total}</strong> 題 ｜ 正確率 <strong>${result.score}%</strong>
      </div>
      <div style="margin-top:16px;">
        <button class="btn-sm btn-amber" onclick="exitExamToCenter()">返回證照專區</button>
      </div>
    </div>

    <!-- Radar Chart Block -->
    <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:12px; padding:24px; margin-bottom:24px;">
      <h3 style="font-size:18px; font-weight:800; color:var(--primary-navy); margin-bottom:12px; text-align:center;">
        📊 iPAS 專業模組落點能力雷達圖 (Competency Radar Chart)
      </h3>
      <div class="radar-container" id="radarSvgContainer">
        ${generateRadarSvg(result.moduleStats)}
      </div>
    </div>

    <!-- Detailed Explanations -->
    <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:12px; padding:24px;">
      <h3 style="font-size:18px; font-weight:800; color:var(--primary-navy); margin-bottom:16px;">
        逐題精闢詳解清單 (${result.details.length} 題)
      </h3>
      <div style="display:flex; flex-direction:column; gap:16px;">
        ${result.details.map((d, idx) => `
          <div style="border:1px solid ${d.is_correct ? '#86efac' : '#fca5a5'}; background:${d.is_correct ? '#f0fdf4' : '#fff1f2'}; border-radius:10px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span style="font-weight:700; color:var(--primary-navy);">第 ${idx + 1} 題：${d.question}</span>
              <span style="font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px; color:#ffffff; background:${d.is_correct ? '#16a34a' : '#dc2626'};">
                ${d.is_correct ? '答對' : '答錯'}
              </span>
            </div>
            <div style="font-size:13.5px; color:#334155; margin:6px 0;">
              <div>您的作答：<strong>${d.user_answer !== undefined ? ['A', 'B', 'C', 'D'][d.user_answer] + '. ' + d.options[d.user_answer] : '未作答'}</strong></div>
              <div>正確答案：<strong style="color:#16a34a;">${['A', 'B', 'C', 'D'][d.correct_answer]}. ${d.options[d.correct_answer]}</strong></div>
            </div>
            <div style="background:#ffffff; border:1px dashed #cbd5e1; border-radius:6px; padding:10px 14px; font-size:13px; color:#475569; margin-top:8px;">
              💡 <strong>詳解剖析：</strong>${d.explanation}
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function exitExamToCenter() {
  document.getElementById('ipasIntroArea').style.display = 'block';
  document.getElementById('ipasExamArea').style.display = 'none';
  document.getElementById('ipasResultArea').style.display = 'none';
}

// Custom Pure SVG Radar Chart Generator
function generateRadarSvg(stats) {
  const modules = Object.keys(stats);
  if (modules.length === 0) return '<div style="color:#94a3b8;">無足夠數據繪製雷達圖</div>';

  const defaultKeys = modules.length >= 3 ? modules : ['Word 商業文書', 'Excel 數據分析', 'PowerPoint 簡報', 'Agentic AI 核心', '資安法規與流程'];
  const size = 380;
  const center = size / 2;
  const radius = 130;
  const totalAxes = defaultKeys.length;
  const angleStep = (Math.PI * 2) / totalAxes;

  // Background Circles / Polygons
  let gridPolygons = '';
  for (let level = 1; level <= 4; level++) {
    const levelR = (radius / 4) * level;
    let points = [];
    for (let i = 0; i < totalAxes; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = center + levelR * Math.cos(angle);
      const y = center + levelR * Math.sin(angle);
      points.push(`${x.toFixed(1)},${y.toFixed(1)}`);
    }
    gridPolygons += `<polygon points="${points.join(' ')}" fill="none" stroke="#e2e8f0" stroke-width="1.5" />`;
  }

  // Axis lines & labels
  let axisLines = '';
  let labels = '';
  let dataPoints = [];

  defaultKeys.forEach((key, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const xEnd = center + radius * Math.cos(angle);
    const yEnd = center + radius * Math.sin(angle);
    axisLines += `<line x1="${center}" y1="${center}" x2="${xEnd.toFixed(1)}" y2="${yEnd.toFixed(1)}" stroke="#cbd5e1" stroke-width="1" />`;

    // Calculate score ratio
    let ratio = 0.5;
    if (stats[key] && stats[key].total > 0) {
      ratio = stats[key].correct / stats[key].total;
    }
    const dataR = radius * Math.max(0.1, Math.min(1.0, ratio));
    const dataX = center + dataR * Math.cos(angle);
    const dataY = center + dataR * Math.sin(angle);
    dataPoints.push(`${dataX.toFixed(1)},${dataY.toFixed(1)}`);

    // Label Position
    const labelR = radius + 26;
    const lx = center + labelR * Math.cos(angle);
    const ly = center + labelR * Math.sin(angle);
    const pctText = stats[key] ? `${Math.round(ratio * 100)}%` : '50%';
    labels += `
      <text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="middle" dominant-baseline="middle" font-size="11" font-weight="700" fill="#1e293b">
        ${key.substring(0, 8)} (${pctText})
      </text>
    `;
  });

  const dataPolygon = `<polygon points="${dataPoints.join(' ')}" fill="rgba(37, 99, 235, 0.35)" stroke="#2563eb" stroke-width="2.5" />`;

  return `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size}" ${size} style="max-width:100%; height:auto;">
      ${gridPolygons}
      ${axisLines}
      ${dataPolygon}
      ${labels}
    </svg>
  `;
}

// -------------------------------------------------------------
// SECTION 5: 學習成就勳章與錯題本 (Achievements)
// -------------------------------------------------------------
function renderAchievements() {
  const badgeContainer = document.getElementById('badgesGrid');
  if (!badgeContainer) return;

  const BADGES_SPEC = [
    { id: 'badge_newbie', name: '商業軟體先鋒', desc: '成功登入並開始修習 18 週課程', icon: '🌟' },
    { id: 'badge_prompt_master', name: 'CLEAR 提問宗師', desc: '精熟五大商務提示詞結構', icon: '✍️' },
    { id: 'badge_word_expert', name: 'Word 長報告大師', desc: '精熟樣式集、多層次編號與三線表', icon: '📄' },
    { id: 'badge_excel_ninja', name: 'XLOOKUP 查表之王', desc: '掌握多條件統計與動態切片器', icon: '📊' },
    { id: 'badge_ppt_guru', name: '金字塔簡報領袖', desc: '熟練 SCQA 結構與 CRAP 圖解化', icon: '📑' },
    { id: 'badge_react_master', name: 'Agentic 架構師', desc: '成功在沙盒完成 ReAct 自主推理執行', icon: '🤖' },
    { id: 'badge_ipas_pass', name: 'iPAS 認證準規劃師', desc: '自我評量取得 70 分以上及格認證', icon: '🎯' },
    { id: 'badge_top_scorer', name: '榮譽榜首高分王', desc: '自我評量取得 90 分以上卓越成績', icon: '👑' },
    { id: 'badge_work_submitted', name: '實戰成果發表先驅', desc: '成功繳交商業軟體實作或期中/期末成果專案', icon: '🚀' }
  ];

  badgeContainer.innerHTML = BADGES_SPEC.map(b => {
    const isEarned = state.earnedBadges.includes(b.id);
    return `
      <div style="background:#ffffff; border:1px solid ${isEarned ? '#f59e0b' : '#e2e8f0'}; border-radius:12px; padding:20px; text-align:center; opacity:${isEarned ? '1' : '0.45'}; box-shadow:${isEarned ? '0 4px 15px rgba(245, 158, 11, 0.15)' : 'none'};">
        <div style="font-size:36px; margin-bottom:8px;">${b.icon}</div>
        <div style="font-size:16px; font-weight:800; color:var(--primary-navy);">${b.name}</div>
        <div style="font-size:12px; color:#64748b; margin-top:4px;">${b.desc}</div>
        <div style="margin-top:10px;">
          <span style="font-size:11px; font-weight:700; padding:2px 8px; border-radius:10px; background:${isEarned ? '#fef3c7' : '#f1f5f9'}; color:${isEarned ? '#b45309' : '#94a3b8'};">
            ${isEarned ? '已解鎖 🏆' : '未達成 🔒'}
          </span>
        </div>
      </div>
    `;
  }).join('');

  // Mistake Notebook
  renderMistakeNotebook();
}

function unlockBadge(badgeId) {
  if (!state.earnedBadges.includes(badgeId)) {
    state.earnedBadges.push(badgeId);
    localStorage.setItem('vnu_bsa_badges', JSON.stringify(state.earnedBadges));
    renderAchievements();
  }
}

function renderMistakeNotebook() {
  const container = document.getElementById('mistakeNotebookBox');
  if (!container) return;

  const mistakes = state.questions.filter(q => state.mistakeIds.includes(q.id));
  if (mistakes.length === 0) {
    container.innerHTML = `<div style="text-align:center; color:#16a34a; padding:20px; font-weight:700;">🎉 錯題本目前為空！您答過的題目全數掌握，太棒了！</div>`;
    return;
  }

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
      <span style="font-size:14px; font-weight:700; color:var(--primary-navy);">收錄錯題共 <strong>${mistakes.length}</strong> 題</span>
      <button class="btn-sm btn-amber" onclick="retakeMistakes()">🔥 考前一鍵重練錯題 (${mistakes.length}題)</button>
    </div>
    <div style="display:flex; flex-direction:column; gap:12px;">
      ${mistakes.map(m => `
        <div style="background:#ffffff; border:1px solid #fed7aa; border-radius:8px; padding:14px; border-left:4px solid #f97316;">
          <div style="font-weight:700; font-size:14px; color:var(--primary-navy);">${m.id}. ${m.question}</div>
          <div style="font-size:13px; color:#16a34a; margin-top:4px;">正確答案：${['A', 'B', 'C', 'D'][m.answer]}. ${m.options[m.answer]}</div>
          <div style="font-size:12px; color:#64748b; margin-top:4px;">💡 ${m.explanation}</div>
        </div>
      `).join('')}
    </div>
  `;
}

function retakeMistakes() {
  const mistakes = state.questions.filter(q => state.mistakeIds.includes(q.id));
  if (mistakes.length === 0) return;
  switchTab('ipas');

  state.exam.active = true;
  state.exam.questions = [...mistakes].sort(() => Math.random() - 0.5);
  state.exam.currentIndex = 0;
  state.exam.answers = {};
  state.exam.examType = 'mistakes';
  state.exam.title = `個人錯題複習練習 (${mistakes.length} 題)`;
  state.exam.remainingSeconds = mistakes.length * 90;

  document.getElementById('ipasIntroArea').style.display = 'none';
  document.getElementById('ipasExamArea').style.display = 'block';
  document.getElementById('ipasResultArea').style.display = 'none';

  startExamTimer();
  renderExamQuestion();
  renderExamSidebar();
}

// -------------------------------------------------------------
// SECTION 6: 18 週全螢幕簡報授課模式 (Slides Presenter Integration)
// -------------------------------------------------------------
function openSlidePresenter(week = 1, slideIdx = 0) {
  const slidesData = window.COURSE_SLIDES_DATA;
  if (!slidesData || !slidesData.slidesByWeek) {
    alert("正在載入簡報資料庫，請稍候...");
    return;
  }

  state.presenter.isOpen = true;
  state.presenter.currentWeek = week;
  state.presenter.currentSlideIdx = slideIdx;

  const overlay = document.getElementById('slidesPresenterOverlay');
  if (overlay) overlay.classList.add('open');

  populatePresenterWeekSelector();
  renderPresenterSlide();
}

function closeSlidePresenter() {
  state.presenter.isOpen = false;
  const overlay = document.getElementById('slidesPresenterOverlay');
  if (overlay) overlay.classList.remove('open');
}

function populatePresenterWeekSelector() {
  const sel = document.getElementById('presenterWeekSelect');
  if (!sel || !window.COURSE_SLIDES_DATA || !window.COURSE_SLIDES_DATA.weeks) return;

  sel.innerHTML = window.COURSE_SLIDES_DATA.weeks.map(w => {
    let rawTitle = w.title || '';
    // Strip duplicated "第 XX 週：" or "第 XX 週:" prefix if already present
    rawTitle = rawTitle.replace(/^第\s*\d+\s*週[：:]\s*/, '');
    const isSelected = parseInt(w.week) === parseInt(state.presenter.currentWeek);
    return `<option value="${w.week}" ${isSelected ? 'selected' : ''}>第 ${String(w.week).padStart(2, '0')} 週：${rawTitle}</option>`;
  }).join('');
  sel.value = String(state.presenter.currentWeek);
}

function onPresenterWeekChange() {
  const sel = document.getElementById('presenterWeekSelect');
  if (sel && sel.value) {
    state.presenter.currentWeek = parseInt(sel.value);
    state.presenter.currentSlideIdx = 0;
    renderPresenterSlide();
  }
}

function nextPresenterWeek() {
  if (state.presenter.currentWeek < 18) {
    state.presenter.currentWeek++;
    state.presenter.currentSlideIdx = 0;
    populatePresenterWeekSelector();
    renderPresenterSlide();
  } else {
    alert("已是第 18 週（全學期總結課程）。");
  }
}

function prevPresenterWeek() {
  if (state.presenter.currentWeek > 1) {
    state.presenter.currentWeek--;
    state.presenter.currentSlideIdx = 0;
    populatePresenterWeekSelector();
    renderPresenterSlide();
  } else {
    alert("已是第 01 週（課程導引與環境建置）。");
  }
}
window.nextPresenterWeek = nextPresenterWeek;
window.prevPresenterWeek = prevPresenterWeek;
window.onPresenterWeekChange = onPresenterWeekChange;
window.openSlidePresenter = openSlidePresenter;
window.closeSlidePresenter = closeSlidePresenter;

function renderPresenterSlide() {
  const slidesData = window.COURSE_SLIDES_DATA;
  if (!slidesData) return;
  const weekSlides = slidesData.slidesByWeek[String(state.presenter.currentWeek)] || [];
  if (weekSlides.length === 0) return;

  const slide = weekSlides[state.presenter.currentSlideIdx];
  if (!slide) return;

  // Counter
  const counter = document.getElementById('presenterCounter');
  if (counter) {
    counter.innerHTML = `<span style="color:#f59e0b; font-size:18px;">${state.presenter.currentSlideIdx + 1}</span> / ${weekSlides.length}`;
  }

  // Render Slide Stage
  const stage = document.getElementById('slideStageCanvas');
  if (!stage) return;

  const baseSize = 28 + (state.presenter.fontSizeOffset || 0);
  const subSize = baseSize + 2;        // 30px
  const cardTitleSize = baseSize + 4;  // 32px
  const titleSize = baseSize + 12;     // 40px
  const heroTitleSize = baseSize + 22; // 50px

  let bodyContent = '';
  if (slide.type === 'title') {
    bodyContent = `
      <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:48px 36px;">
        <span class="badge-pill" style="font-size:20px; font-weight:800; padding:6px 18px; margin-bottom:20px; background:#d97706; color:#ffffff;">${slide.badge || '課程單元'}</span>
        <h1 style="font-size:${heroTitleSize}px; font-weight:900; color:#1e3a8a; margin-bottom:24px; line-height:1.25; letter-spacing:-0.5px;">${slide.title}</h1>
        <div style="font-size:${subSize}px; color:#334155; max-width:1150px; white-space:pre-line; line-height:1.6; font-weight:600;">${slide.subtitle || ''}</div>
      </div>
    `;
  } else if (slide.type === 'prompt') {
    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#0284c7; font-size:16px; font-weight:700;">${slide.badge || '實戰 Prompt 模板'}</span>
            <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
            <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || '請點擊複製按鈕，貼入免費版 AI 對話視窗'}</div>
          </div>
          <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div class="presenter-grid-prompt" style="flex:1; padding:24px 36px; display:grid; grid-template-columns: 2fr 1fr; gap:24px; align-items:stretch; overflow-y:auto;">
          <div style="background:#0f172a; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 6px 20px rgba(0,0,0,0.15);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #334155; padding-bottom:10px;">
              <div style="display:flex; gap:6px; align-items:center;">
                <span style="width:12px; height:12px; border-radius:50%; background:#ef4444; display:inline-block;"></span>
                <span style="width:12px; height:12px; border-radius:50%; background:#f59e0b; display:inline-block;"></span>
                <span style="width:12px; height:12px; border-radius:50%; background:#10b981; display:inline-block;"></span>
                <span style="color:#94a3b8; font-size:14px; font-weight:700; margin-left:10px;">PROMPT TEMPLATE</span>
              </div>
              <button class="btn-sm" onclick="copyPresenterPromptText()" style="background:#0284c7; color:#fff; border:none; padding:6px 16px; font-size:14px; font-weight:700; border-radius:6px; cursor:pointer;">
                <i class="fas fa-copy"></i> 一鍵複製提示詞
              </button>
            </div>
            ${slide.prompt_role ? `
              <div style="margin-bottom:12px;">
                <span style="background:#1e293b; color:#38bdf8; border:1px solid #0284c7; font-size:14px; font-weight:700; padding:4px 10px; border-radius:6px;">
                  🎭 設定專家角色：${slide.prompt_role}
                </span>
              </div>
            ` : ''}
            <pre id="activePresenterPrompt" style="flex:1; color:#f8fafc; font-family:Consolas, Monaco, 'Courier New', monospace; font-size:${baseSize - 4}px; line-height:1.7; white-space:pre-wrap; margin:0; overflow-y:auto;">${slide.prompt_text || slide.prompt || ''}</pre>
          </div>
          <div style="display:flex; flex-direction:column; gap:16px; overflow-y:auto;">
            ${slide.side_html ? slide.side_html : (slide.side_steps ? `
              <div style="background:#ffffff; border:2px solid #bfdbfe; border-top:6px solid #0284c7; border-radius:12px; padding:20px; box-shadow:0 4px 12px rgba(0,0,0,0.04); flex:1;">
                <div style="font-size:${cardTitleSize}px; font-weight:900; color:#1e3a8a; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                  <span>📋</span> 一步一步帶你做 (Step-by-Step)
                </div>
                ${slide.side_steps.map((st, idx) => `
                  <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid #0284c7; border-radius:8px; padding:12px 14px; margin-bottom:12px;">
                    <div style="font-size:15px; font-weight:800; color:#0f172a; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                      <span style="background:#0284c7; color:#fff; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:12px; font-weight:900;">${idx+1}</span>
                      <span>${st.title}</span>
                    </div>
                    <div style="font-size:13px; color:#475569; line-height:1.6; white-space:pre-line;">${st.desc}</div>
                  </div>
                `).join('')}
                ${slide.side_tip ? `
                  <div style="margin-top:10px; background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706; padding:10px 14px; border-radius:6px; font-size:13px; color:#92400e; line-height:1.6;">
                    <strong>💡 經理人操作要領：</strong>${slide.side_tip}
                  </div>
                ` : ''}
              </div>
            ` : `
            <div style="background:#f0fdf4; border:2px solid #86efac; border-top:6px solid #16a34a; border-radius:12px; padding:20px; flex:1;">
              <h3 style="color:#166534; font-size:${cardTitleSize}px; font-weight:800; margin-bottom:10px;">
                💡 CLEAR 提問架構解析
              </h3>
              <div style="font-size:${baseSize - 4}px; color:#14532d; line-height:1.7;">
                <div style="margin-bottom:8px;">• <strong>C (背景)</strong>：交代專案情境與目標受眾</div>
                <div style="margin-bottom:8px;">• <strong>L (限制)</strong>：限定格式、條列排版與字數</div>
                <div style="margin-bottom:8px;">• <strong>E (期望)</strong>：指名需要案由、表格與負責人</div>
                <div style="margin-bottom:8px;">• <strong>A (行動)</strong>：使用明確專業動詞【整理/編排】</div>
                <div>• <strong>R (角色)</strong>：設定辦公室資深特助或專業顧問</div>
              </div>
            </div>
            <div style="background:#eff6ff; border:2px solid #bfdbfe; border-top:6px solid #2563eb; border-radius:12px; padding:18px;">
              <div style="font-size:14px; font-weight:700; color:#1e40af; margin-bottom:6px;">
                📌 課堂提問操作技巧
              </div>
              <div style="font-size:${baseSize - 6}px; color:#1e3a8a; line-height:1.5;">
                點擊上方【一鍵複製提示詞】後，切換至免費版 Antigravity 或 Google Gemini，直接按 Ctrl+V 貼上即可開始生成！
              </div>
            </div>
            `)}
          </div>
        </div>
      </div>
    `;
  } else if (slide.type === 'sop' || slide.type === 'step') {
    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#1e3a8a; font-size:16px; font-weight:700;">${slide.badge || '操作 SOP'}</span>
            <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
            <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
          </div>
          <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: ${slide.diagram_html ? '1.2fr 1fr' : '2fr 1fr'}; gap:24px; align-items:stretch; overflow-y:auto;">
          <div style="background:#ffffff; border:2px solid #cbd5e1; border-top:8px solid #1e3a8a; border-radius:12px; padding:24px; box-shadow:0 4px 12px rgba(0,0,0,0.04); display:flex; flex-direction:column;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
              <span style="width:42px; height:42px; border-radius:50%; background:#1e3a8a; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:20px;">
                ${slide.step_num || 'SOP'}
              </span>
              <h3 style="color:#1e3a8a; font-size:${cardTitleSize}px; font-weight:900; margin:0;">
                ${slide.step_title || slide.title}
              </h3>
            </div>
            <div style="font-size:${baseSize}px; color:#0f172a; line-height:1.75; font-weight:500; flex:1;">
              ${slide.step_desc || ''}
            </div>
            ${slide.step_tip ? `
              <div style="margin-top:16px; background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706; padding:12px 16px; border-radius:6px; font-size:${baseSize - 4}px; color:#92400e; line-height:1.6;">
                <strong>💡 操作指引：</strong> ${slide.step_tip}
              </div>
            ` : ''}
          </div>
          ${slide.diagram_html ? `
            <div style="background:#f8fafc; border:2px solid #cbd5e1; border-radius:12px; padding:20px; display:flex; flex-direction:column; justify-content:center; align-items:center; overflow:hidden;">
              ${slide.diagram_html}
            </div>
          ` : `
            <div style="background:#fffbeb; border:2px solid #fde68a; border-top:8px solid #d97706; border-radius:12px; padding:24px; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
              <h3 style="color:#d97706; font-size:${cardTitleSize}px; font-weight:900; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>💡</span> 關鍵提醒與操作要點
              </h3>
              <div style="font-size:${baseSize - 2}px; color:#334155; line-height:1.7; font-weight:500;">
                ${slide.step_tip || '依照步驟指示在 Cloud Shell 終端機或 VS Code 編輯器中實施，如有疑問請隨時向老師提問。'}
              </div>
            </div>
          `}
        </div>
      </div>
    `;
  } else if (slide.type === 'comparison') {
    const cardsHtml = (slide.cards || []).map((c, i) => `
      <div style="background:#ffffff; border:2px solid ${c.theme === 'emerald' ? '#86efac' : '#cbd5e1'}; border-top:8px solid ${c.theme === 'emerald' ? '#059669' : '#e11d48'}; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <span style="font-size:${cardTitleSize}px; font-weight:900; color:#0f172a;">${c.title}</span>
          <span style="font-size:16px; font-weight:800; padding:4px 12px; border-radius:12px; background:${c.theme === 'emerald' ? '#d1fae5' : '#fee2e2'}; color:${c.theme === 'emerald' ? '#065f46' : '#991b1b'};">${c.tag || '對照'}</span>
        </div>
        <div style="font-size:${baseSize}px; color:#1e293b; line-height:1.7; flex:1; font-weight:500; white-space:pre-line;">${c.content || c.desc || ''}</div>
      </div>
    `).join('');

    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#059669; font-size:16px; font-weight:700;">${slide.badge || '模式對比'}</span>
            <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
            <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
          </div>
          <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap:24px; align-items:stretch; overflow-y:auto;">
          ${cardsHtml}
        </div>
      </div>
    `;
  } else if (slide.type === 'debug') {
    const cardsHtml = (slide.cards || []).map(c => `
      <div style="background:#ffffff; border:2px solid #cbd5e1; border-top:8px solid ${c.theme === 'rose' ? '#e11d48' : c.theme === 'amber' ? '#d97706' : '#2563eb'}; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <span style="font-size:${cardTitleSize}px; font-weight:900; color:#0f172a;">${c.title}</span>
          <span style="font-size:16px; font-weight:800; padding:4px 12px; border-radius:12px; background:#e2e8f0; color:#334155;">${c.tag || '說明'}</span>
        </div>
        <div style="font-size:${baseSize}px; color:#1e293b; line-height:1.7; flex:1; font-weight:500;">${c.content || c.desc || ''}</div>
      </div>
    `).join('');

    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#dc2626; font-size:16px; font-weight:700;">${slide.badge || '常見問題排解'}</span>
            <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
            <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
          </div>
          <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap:24px; align-items:stretch; overflow-y:auto;">
          ${cardsHtml}
        </div>
      </div>
    `;
  } else if (slide.type === 'drill') {
    const cardsHtml = (slide.cards || []).map(c => `
      <div style="background:#ffffff; border:2px solid #cbd5e1; border-top:8px solid #0284c7; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <span style="font-size:${cardTitleSize}px; font-weight:900; color:#0f172a;">${c.title}</span>
          <span style="font-size:16px; font-weight:800; padding:4px 12px; border-radius:12px; background:#e0f2fe; color:#0369a1;">${c.tag || '實作'}</span>
        </div>
        <div style="font-size:${baseSize}px; color:#1e293b; line-height:1.7; flex:1; font-weight:500;">${c.content || c.desc || ''}</div>
      </div>
    `).join('');

    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#0284c7; font-size:16px; font-weight:700;">${slide.badge || '隨堂實作演練'}</span>
            <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
            <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
          </div>
          <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap:24px; align-items:stretch; overflow-y:auto;">
          ${cardsHtml}
        </div>
      </div>
    `;
  } else {
    // General Cards Layout with optional Diagram HTML support
    const cards = slide.cards || [];
    let cardsHtml = '';
    if (cards.length > 0) {
      cardsHtml = cards.map(c => `
        <div style="background:#ffffff; border:2px solid #cbd5e1; border-top:8px solid ${c.theme === 'amber' ? '#d97706' : c.theme === 'emerald' ? '#059669' : '#1e3a8a'}; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <span style="font-size:${cardTitleSize}px; font-weight:900; color:#0f172a;">${c.title}</span>
            <span style="font-size:16px; font-weight:800; padding:4px 12px; border-radius:12px; background:#e2e8f0; color:#334155;">${c.tag || '重點'}</span>
          </div>
          <div style="font-size:${baseSize}px; color:#1e293b; line-height:1.7; flex:1; font-weight:500;">${c.content || c.desc || ''}</div>
        </div>
      `).join('');
    } else {
      // Fallback if cards is empty
      cardsHtml = `
        <div style="background:#ffffff; border:2px solid #cbd5e1; border-top:8px solid #1e3a8a; border-radius:12px; padding:24px; display:flex; flex-direction:column; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
          <div style="font-size:${cardTitleSize}px; font-weight:900; color:#0f172a; margin-bottom:12px;">核心要點說明</div>
          <div style="font-size:${baseSize}px; color:#1e293b; line-height:1.7; font-weight:500;">${slide.subtitle || '請依循教師現場說明進行學習與操作。'}</div>
        </div>
      `;
    }

    if (slide.diagram_html) {
      bodyContent = `
        <div style="display:flex; flex-direction:column; height:100%;">
          <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
            <div>
              <span class="badge-pill" style="background:#1e3a8a; font-size:16px; font-weight:700;">${slide.badge || '核心觀念'}</span>
              <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
              <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
            </div>
            <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
          </div>
          <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: 1.2fr 1fr; gap:24px; align-items:stretch; overflow-y:auto;">
            <div style="background:#f8fafc; border:2px solid #cbd5e1; border-radius:12px; padding:20px; display:flex; flex-direction:column; justify-content:center; align-items:center; overflow:hidden;">
              ${slide.diagram_html}
            </div>
            <div style="display:flex; flex-direction:column; gap:16px;">
              ${cardsHtml}
            </div>
          </div>
        </div>
      `;
    } else {
      bodyContent = `
        <div style="display:flex; flex-direction:column; height:100%;">
          <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
            <div>
              <span class="badge-pill" style="background:#1e3a8a; font-size:16px; font-weight:700;">${slide.badge || '核心觀念'}</span>
              <h2 style="font-size:${titleSize}px; font-weight:800; color:#1e3a8a; margin-top:6px; margin-bottom:4px;">${slide.title}</h2>
              <div style="font-size:${baseSize - 4}px; color:#475569; font-weight:600;">${slide.subtitle || ''}</div>
            </div>
            <div style="font-size:16px; font-weight:700; color:#64748b;">${slide.sec || ''} ｜ 頁碼 ${slide.num}</div>
          </div>
          <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap:24px; align-items:stretch; overflow-y:auto;">
            ${cardsHtml}
          </div>
        </div>
      `;
    }
  }

  stage.innerHTML = bodyContent;

  // Speaker notes
  const notesText = document.getElementById('speakerNotesText');
  if (notesText) {
    notesText.textContent = slide.speaker_note || "本頁尚無演講者備忘稿。";
  }
}

function copyPresenterPromptText() {
  const el = document.getElementById('activePresenterPrompt');
  if (el) {
    copyTextToClipboard(el.innerText, "提示詞已成功複製到剪貼簿！可直接貼給 AI 使用。");
  }
}
window.copyPresenterPromptText = copyPresenterPromptText;


function changePresenterFontSize(delta) {
  state.presenter.fontSizeOffset = (state.presenter.fontSizeOffset || 0) + delta;
  if (state.presenter.fontSizeOffset < -6) state.presenter.fontSizeOffset = -6;
  if (state.presenter.fontSizeOffset > 14) state.presenter.fontSizeOffset = 14;
  updateFontSizeLabel();
  renderPresenterSlide();
}

function resetPresenterFontSize() {
  state.presenter.fontSizeOffset = 0;
  updateFontSizeLabel();
  renderPresenterSlide();
}

function updateFontSizeLabel() {
  const lbl = document.getElementById('presenterFontSizeLabel');
  if (lbl) {
    const sz = 28 + (state.presenter.fontSizeOffset || 0);
    lbl.textContent = `${sz}px`;
  }
}

function nextPresenterSlide() {
  const slidesData = window.COURSE_SLIDES_DATA;
  if (!slidesData || !slidesData.slidesByWeek) return;
  const weekSlides = slidesData.slidesByWeek[String(state.presenter.currentWeek)] || [];
  
  if (state.presenter.currentSlideIdx < weekSlides.length - 1) {
    state.presenter.currentSlideIdx++;
    renderPresenterSlide();
  } else if (state.presenter.currentWeek < 18) {
    // Smoothly transition to the next week's first slide
    state.presenter.currentWeek++;
    state.presenter.currentSlideIdx = 0;
    populatePresenterWeekSelector();
    renderPresenterSlide();
  } else {
    // Reached the end of week 18
    alert("已完成全學期 18 週全套簡報講義瀏覽！");
  }
}

function prevPresenterSlide() {
  const slidesData = window.COURSE_SLIDES_DATA;
  if (!slidesData || !slidesData.slidesByWeek) return;

  if (state.presenter.currentSlideIdx > 0) {
    state.presenter.currentSlideIdx--;
    renderPresenterSlide();
  } else if (state.presenter.currentWeek > 1) {
    // Smoothly transition to previous week's last slide
    state.presenter.currentWeek--;
    const prevWeekSlides = slidesData.slidesByWeek[String(state.presenter.currentWeek)] || [];
    state.presenter.currentSlideIdx = Math.max(0, prevWeekSlides.length - 1);
    populatePresenterWeekSelector();
    renderPresenterSlide();
  }
}
window.nextPresenterSlide = nextPresenterSlide;
window.prevPresenterSlide = prevPresenterSlide;

function togglePresenterSpeakerNotes() {
  state.presenter.isNotesOpen = !state.presenter.isNotesOpen;
  const drawer = document.getElementById('presenterNotesDrawer');
  if (drawer) drawer.style.display = state.presenter.isNotesOpen ? 'block' : 'none';
}
window.togglePresenterSpeakerNotes = togglePresenterSpeakerNotes;

function togglePresenterFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(e => console.log("全螢幕切換受限：" + e.message));
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
  }
}
window.togglePresenterFullscreen = togglePresenterFullscreen;

// Touch Swipe Listener for Mobile and Tablet
function setupTouchSwipeListeners() {
  const overlay = document.getElementById('slidesPresenterOverlay');
  if (!overlay) return;

  let touchStartX = 0;
  let touchStartY = 0;
  let touchEndX = 0;
  let touchEndY = 0;

  overlay.addEventListener('touchstart', (e) => {
    if (e.touches && e.touches.length === 1) {
      touchStartX = e.touches[0].screenX;
      touchStartY = e.touches[0].screenY;
    }
  }, { passive: true });

  overlay.addEventListener('touchend', (e) => {
    if (e.changedTouches && e.changedTouches.length === 1) {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe();
    }
  }, { passive: true });

  function handleSwipe() {
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;
    // Horizontal swipe threshold: 45px, horizontal distance must dominate vertical distance
    if (Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
      if (deltaX < 0) {
        // Swipe Left -> Next Slide
        nextPresenterSlide();
      } else {
        // Swipe Right -> Prev Slide
        prevPresenterSlide();
      }
    }
  }
}

// Global Keyboard Shortcuts
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

    if (state.presenter.isOpen) {
      if (e.shiftKey && (e.key === 'ArrowRight' || e.key === 'PageDown')) {
        e.preventDefault();
        nextPresenterWeek();
      } else if (e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'PageUp')) {
        e.preventDefault();
        prevPresenterWeek();
      } else if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextPresenterSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevPresenterSlide();
      } else if (e.key.toLowerCase() === 'f') {
        e.preventDefault();
        togglePresenterFullscreen();
      } else if (e.key.toLowerCase() === 'n') {
        e.preventDefault();
        togglePresenterSpeakerNotes();
      } else if (e.key === 'Escape') {
        closeSlidePresenter();
      }
    }
  });
}

/* ==========================================================================
   FIREBASE AUTHENTICATION & GOOGLE SIGN-IN
   ========================================================================== */

function initFirebase() {
  if (typeof firebase !== 'undefined' && firebase.initializeApp) {
    try {
      if (!firebase.apps || firebase.apps.length === 0) {
        firebaseApp = firebase.initializeApp(firebaseConfig);
      } else {
        firebaseApp = firebase.app();
      }
      firebaseAuth = firebase.auth();
      firestoreDb = firebase.firestore();
      isFirebaseAvailable = true;
      console.log('✅ Firebase 初始化成功 (專案: vnu-business-software-11501)');

      firebaseAuth.onAuthStateChanged(async (user) => {
        currentFirebaseUser = user;
        if (user) {
          const userEmail = (user.email || '').toLowerCase().trim();
          isTeacherUser = TEACHER_EMAILS.some(em => userEmail.includes(em.toLowerCase()));
          console.log('👤 使用者已登入 Google:', user.email, isTeacherUser ? '【授課教師 邱俊維 博士】' : '【一般學生】');

          await loadUserProfileFromFirestore(user);
          updateUserNavUI();
          updateUploadFormStudentInfo();
          listenToFirestoreWorks();

          if (isTeacherUser) {
            const navTeacher = document.getElementById('nav-teacher-tab-item');
            if (navTeacher) navTeacher.style.display = 'block';
            const teacherExport = document.getElementById('teacher-export-menu-item');
            if (teacherExport) teacherExport.style.display = 'flex';
          }
        } else {
          console.log('👤 使用者已登出 (訪客模式)');
          isTeacherUser = false;
          updateUserNavUI();
          updateUploadFormStudentInfo();
          const navTeacher = document.getElementById('nav-teacher-tab-item');
          if (navTeacher) navTeacher.style.display = 'none';
          const teacherExport = document.getElementById('teacher-export-menu-item');
          if (teacherExport) teacherExport.style.display = 'none';
          if (state.currentTab === 'teacher') {
            switchTab('orientation');
          }
        }
      });
    } catch (e) {
      console.warn('⚠️ Firebase 初始化警告:', e);
      isFirebaseAvailable = false;
    }
  } else {
    console.log('ℹ️ 離線或未載入 Firebase SDK，使用本機模式');
  }
}

function loginWithGoogle() {
  if (!isFirebaseAvailable || !firebaseAuth) {
    if (typeof firebase !== 'undefined' && firebase.initializeApp) {
      initFirebase();
    }
  }

  if (!isFirebaseAvailable || !firebaseAuth) {
    alert('Firebase 雲端驗證服務載入中或處於離線狀態，系統已為您直接開啟學籍登記視窗！');
    openModal('userProfileModal');
    return;
  }

  try {
    const provider = new firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({ prompt: 'select_account' });
    firebaseAuth.signInWithPopup(provider).then((result) => {
      console.log('Google 登入成功:', result.user.email);
    }).catch((error) => {
      console.error('Google 登入失敗:', error);
      if (error.code === 'auth/popup-closed-by-user') return;
      if (error.code === 'auth/popup-blocked') {
        const tryRedirect = confirm('⚠️ 您的瀏覽器封鎖了 Google 登入彈跳視窗！\n\n是否改用直接頁面跳轉 (Redirect) 方式進行 Google 登入？');
        if (tryRedirect) {
          firebaseAuth.signInWithRedirect(provider);
        }
        return;
      }
      if (error.code === 'auth/unauthorized-domain') {
        alert(`⚠️ Firebase 網域尚未授權提示：\n\n目前網站網域為：【${window.location.hostname}】\n\n請至 Firebase Console (專案：vnu-business-software-11501)\n-> Authentication\n-> Settings (設定)\n-> Authorized domains (已授權的網域)\n將【${window.location.hostname}】加入授權網域清單即可順利登入！`);
        return;
      }
      alert('Google 登入提示：' + (error.message || error));
    });
  } catch (err) {
    console.error('啟動登入程序錯誤:', err);
    alert('啟動登入視窗失敗：' + err.message);
  }
}

function logoutUser() {
  if (firebaseAuth) {
    firebaseAuth.signOut().then(() => {
      alert('您已安全登出 Google 帳號。');
    });
  } else {
    alert('已清除登入狀態。');
  }
}

async function loadUserProfileFromFirestore(user) {
  if (!firestoreDb) return;
  try {
    if (isTeacherUser) {
      state.student.id = 'TEACHER';
      state.student.name = '邱俊維 博士';
      localStorage.setItem('vnu_bsa_student', JSON.stringify(state.student));

      try {
        await firestoreDb.collection('users').doc(user.uid).set({
          uid: user.uid,
          email: user.email || '',
          studentId: 'TEACHER',
          studentName: '邱俊維 博士',
          className: '萬能科技大學 企管系 授課教師',
          photoURL: user.photoURL || '',
          role: 'teacher',
          updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        }, { merge: true });
      } catch (e) {}
      return;
    }

    const doc = await firestoreDb.collection('users').doc(user.uid).get();
    if (doc.exists) {
      const data = doc.data();
      state.student.id = data.studentId || '';
      state.student.name = data.studentName || user.displayName || '同學';
      localStorage.setItem('vnu_bsa_student', JSON.stringify(state.student));

      if (!state.student.id || !state.student.name || state.student.id === '進企管四系1甲' || state.student.name === '同學') {
        openModal('userProfileModal', true);
      }
    } else {
      state.student.id = '';
      state.student.name = user.displayName || '';
      openModal('userProfileModal', true);
    }
  } catch (e) {
    console.warn('載入 Firestore 使用者學籍失敗:', e);
  }
}

async function saveUserProfileModal() {
  const idInput = document.getElementById('modal-student-id');
  const nameInput = document.getElementById('modal-student-name');
  const studentId = idInput ? idInput.value.trim() : '';
  const studentName = nameInput ? nameInput.value.trim() : '';

  if (!studentId) {
    alert('請輸入您的「學號」！');
    if (idInput) idInput.focus();
    return;
  }
  if (!studentName) {
    alert('請輸入您的「姓名」！');
    if (nameInput) nameInput.focus();
    return;
  }

  state.student.id = studentId;
  state.student.name = studentName;
  localStorage.setItem('vnu_bsa_student', JSON.stringify(state.student));

  if (currentFirebaseUser && firestoreDb) {
    try {
      await firestoreDb.collection('users').doc(currentFirebaseUser.uid).set({
        uid: currentFirebaseUser.uid,
        email: currentFirebaseUser.email || '',
        studentId: studentId,
        studentName: studentName,
        className: '進企管四系1甲',
        photoURL: currentFirebaseUser.photoURL || '',
        role: 'student',
        updatedAt: firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true });
      console.log('學籍資訊已儲存至 Firestore users 集合');
    } catch (e) {
      console.warn('更新 Firestore 學籍資訊失敗:', e);
    }
  }

  updateUserNavUI();
  updateUploadFormStudentInfo();
  closeModal('userProfileModal');
  alert(`登記完成！歡迎【進企管四系1甲】${studentName} (${studentId}) 同學！`);
}

function openModal(modalId, force = false) {
  const modal = document.getElementById(modalId);
  if (!modal) return;
  modal.classList.add('open');

  if (modalId === 'userProfileModal') {
    const emailField = document.getElementById('modal-user-email');
    const idField = document.getElementById('modal-student-id');
    const nameField = document.getElementById('modal-student-name');
    if (emailField) emailField.value = currentFirebaseUser ? currentFirebaseUser.email : '訪客模式 (未登入 Google)';
    if (idField) idField.value = (state.student.id !== '進企管四系1甲') ? state.student.id : '';
    if (nameField) nameField.value = (state.student.name !== '同學') ? state.student.name : (currentFirebaseUser?.displayName || '');

    const cancelBtn = document.getElementById('modal-cancel-btn');
    if (cancelBtn) {
      cancelBtn.style.display = force ? 'none' : 'inline-block';
    }
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('open');
}

function toggleUserMenu() {
  const menu = document.getElementById('userDropdownMenu');
  if (!menu) return;
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

window.addEventListener('click', (e) => {
  const box = document.getElementById('user-auth-box');
  const menu = document.getElementById('userDropdownMenu');
  if (box && menu && !box.contains(e.target)) {
    menu.style.display = 'none';
  }
});

function updateUserNavUI() {
  const btnGoogleLogin = document.getElementById('btn-google-login');
  const userAuthBox = document.getElementById('user-auth-box');
  const studentDisplay = document.getElementById('studentDisplay');
  const userAvatarImg = document.getElementById('user-avatar-img');
  const userAvatarIcon = document.getElementById('user-avatar-icon');
  const dropdownEmail = document.getElementById('dropdown-user-email');

  if (currentFirebaseUser) {
    if (btnGoogleLogin) btnGoogleLogin.style.display = 'none';
    if (userAuthBox) userAuthBox.style.display = 'inline-block';
    if (dropdownEmail) dropdownEmail.textContent = currentFirebaseUser.email || '已登入 Google';

    if (currentFirebaseUser.photoURL && userAvatarImg) {
      userAvatarImg.src = currentFirebaseUser.photoURL;
      userAvatarImg.style.display = 'inline-block';
      if (userAvatarIcon) userAvatarIcon.style.display = 'none';
    } else {
      if (userAvatarImg) userAvatarImg.style.display = 'none';
      if (userAvatarIcon) userAvatarIcon.style.display = 'inline-block';
    }
  } else {
    if (btnGoogleLogin) btnGoogleLogin.style.display = 'inline-flex';
    if (userAuthBox) userAuthBox.style.display = 'none';
  }

  if (studentDisplay) {
    const sId = state.student.id || '未登記';
    const sName = state.student.name || '同學';
    studentDisplay.textContent = `${sId} ｜ ${sName}`;
  }
}

function updateUploadFormStudentInfo() {
  const infoText = document.getElementById('upload-student-info-text');
  const emailText = document.getElementById('upload-student-email-text');
  const hintBadge = document.getElementById('upload-login-hint');

  if (infoText) {
    infoText.textContent = `進企管四系1甲 ｜ ${state.student.id || '未填學號'} ｜ ${state.student.name || '同學'}`;
  }
  if (emailText) {
    emailText.textContent = currentFirebaseUser ? `已驗證：${currentFirebaseUser.email}` : '未登入 Google 帳號 (請先登入以確保成績歸屬)';
  }
  if (hintBadge) {
    if (currentFirebaseUser) {
      hintBadge.textContent = '已登入 驗證通過';
      hintBadge.style.background = '#dcfce7';
      hintBadge.style.color = '#15803d';
    } else {
      hintBadge.textContent = '建議先登入';
      hintBadge.style.background = '#fef3c7';
      hintBadge.style.color = '#b45309';
    }
  }
}

/* ==========================================================================
   STUDENT WORKS SUBMISSION & GALLERY LOGIC
   ========================================================================= */

function loadDefaultSampleWorks() {
  const sampleWorks = (window.OFFLINE_DATA && window.OFFLINE_DATA.sampleWorks) || [];
  const localSubmitted = JSON.parse(localStorage.getItem('vnu_bsa_submitted_works') || '[]');
  const existingIds = new Set(localSubmitted.map(w => w.id));
  const nonDuplicateSamples = sampleWorks.filter(w => !existingIds.has(w.id));
  studentWorksData = [...localSubmitted, ...nonDuplicateSamples];
}

let unsubscribeFirestoreWorks = null;
function listenToFirestoreWorks() {
  if (!firestoreDb) return;
  if (unsubscribeFirestoreWorks) unsubscribeFirestoreWorks();

  try {
    unsubscribeFirestoreWorks = firestoreDb.collection('works')
      .onSnapshot((snapshot) => {
        const firestoreWorks = [];
        snapshot.forEach(doc => {
          firestoreWorks.push(doc.data());
        });
        if (firestoreWorks.length > 0) {
          firestoreWorks.sort((a, b) => (b.submitted_at || '').localeCompare(a.submitted_at || ''));
          const existingIds = new Set(firestoreWorks.map(w => w.id));
          const sampleWorks = (window.OFFLINE_DATA && window.OFFLINE_DATA.sampleWorks) || [];
          const nonDuplicateSamples = sampleWorks.filter(w => !existingIds.has(w.id));
          studentWorksData = [...firestoreWorks, ...nonDuplicateSamples];
        } else {
          loadDefaultSampleWorks();
        }
        renderStudentWorks(currentWorksFilter);
        if (isTeacherUser) {
          renderTeacherGradeDashboard();
        }
      }, (err) => {
        console.warn('Firestore works 監聽提醒:', err);
      });
  } catch (e) {
    console.warn('建立 Firestore works 監聽失敗:', e);
  }
}

async function handleProjectSubmit(e) {
  e.preventDefault();

  if (!currentFirebaseUser) {
    alert('⚠️ 依系統規範，請先使用 Google 帳號登入再行繳交作業！');
    loginWithGoogle();
    return;
  }

  if (!isTeacherUser && (!state.student.id || !state.student.name || state.student.id === '進企管四系1甲' || state.student.name === '同學')) {
    alert('⚠️ 請先登記您的「學號」與「真實姓名」！');
    openModal('userProfileModal', true);
    return;
  }

  const weekSelect = document.getElementById('upload-week-select');
  const selectedOpt = weekSelect ? weekSelect.options[weekSelect.selectedIndex] : null;
  const rawReportType = selectedOpt ? selectedOpt.getAttribute('data-type') || selectedOpt.value : '期中報告';
  const reportType = rawReportType.includes('期末') ? '期末成果' : (rawReportType.includes('期中') ? '期中報告' : '自主練習');
  const weekNum = parseInt(selectedOpt?.getAttribute('data-week') || (reportType === '期末成果' ? '18' : (reportType === '期中報告' ? '9' : '1')));
  const weekTitle = selectedOpt ? selectedOpt.text : reportType;

  const titleInput = document.getElementById('upload-title');
  const title = titleInput ? titleInput.value.trim() : '';
  const categorySelect = document.getElementById('upload-category');
  const category = categorySelect ? categorySelect.value : '線上部署網頁 (GitHub Pages / 雲端發布)';
  const liveUrlInput = document.getElementById('upload-live-url');
  const liveUrl = liveUrlInput ? liveUrlInput.value.trim() : '';
  const conceptInput = document.getElementById('upload-concept');
  const concept = conceptInput ? conceptInput.value.trim() : '';
  const promptInput = document.getElementById('upload-prompt-summary');
  const promptSummary = promptInput ? promptInput.value.trim() : '';

  if (!liveUrl) {
    alert('請填寫作品公開成果連結或雲端網址！');
    if (liveUrlInput) liveUrlInput.focus();
    return;
  }

  const workId = 'WORK-' + Date.now();
  const nowStr = new Date().toLocaleString('zh-TW', { hour12: false });

  const newWork = {
    id: workId,
    uid: currentFirebaseUser ? currentFirebaseUser.uid : '',
    email: currentFirebaseUser ? currentFirebaseUser.email : '',
    student_id: state.student.id,
    student_name: state.student.name,
    class_name: '進企管四系1甲',
    report_type: reportType,
    week: weekNum,
    week_title: weekTitle,
    title: title,
    category: category,
    concept: concept,
    agent_used: 'Agentic AI 協同實作',
    prompt_summary: promptSummary,
    live_url: liveUrl,
    submitted_at: nowStr,
    score: null,
    teacher_comment: ''
  };

  const submitBtn = document.getElementById('btn-submit-work');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 同步儲存中...';
  }

  if (firestoreDb) {
    try {
      await firestoreDb.collection('works').doc(workId).set({
        ...newWork,
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });
      console.log('✅ 作業已同步至 Firestore works 集合');
    } catch (err) {
      console.warn('Firestore 寫入警告 (改用本機儲存):', err);
    }
  }

  // Local storage backup
  studentWorksData.unshift(newWork);
  try {
    const localWorks = JSON.parse(localStorage.getItem('vnu_bsa_submitted_works') || '[]');
    localWorks.unshift(newWork);
    localStorage.setItem('vnu_bsa_submitted_works', JSON.stringify(localWorks));
  } catch (e) {}

  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> 確認上傳並同步至展示廊';
  }

  renderStudentWorks(currentWorksFilter);
  if (isTeacherUser) renderTeacherGradeDashboard();
  unlockBadge('badge_work_submitted');

  document.getElementById('project-upload-form').reset();
  alert(`🎉 恭喜【進企管四系1甲】${state.student.name} 同學！\n《${title}》(${reportType}) 已成功上傳並同步至展示廊！`);
}

function filterWorks(category, btn) {
  currentWorksFilter = category;
  document.querySelectorAll('.gallery-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderStudentWorks(currentWorksFilter);
}

function renderStudentWorks(filter = currentWorksFilter) {
  const grid = document.getElementById('studentWorksGrid');
  const countSpan = document.getElementById('gallery-total-count');
  if (!grid) return;

  const totalWorks = studentWorksData || [];
  if (countSpan) countSpan.textContent = totalWorks.length;

  const filtered = totalWorks.filter(w => {
    if (filter === 'all') return true;
    if (filter === '期中報告' || filter === '期中實作') {
      return w.report_type === '期中報告' || w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9;
    }
    if (filter === '期末成果') {
      return w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18;
    }
    if (filter === '自主練習' || filter === '平時作業') {
      return w.report_type === '自主練習' || w.report_type === '平時作業' || (w.week !== 9 && w.week !== 18);
    }
    if (filter === 'mine') {
      if (currentFirebaseUser && w.uid && w.uid === currentFirebaseUser.uid) return true;
      if (state.student.id && w.student_id === state.student.id) return true;
      return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align:center; padding:50px 20px; color:#94a3b8;">
        <i class="fas fa-folder-open" style="font-size:42px; margin-bottom:12px; display:block; opacity:0.4;"></i>
        <div style="font-size:15px; font-weight:700;">尚無此類別的學生專案成果</div>
        <div style="font-size:13px; margin-top:4px;">歡迎使用左側表單率先繳交作業並同步至此！</div>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map(w => {
    const isFinal = (w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18);
    const isMidterm = (w.report_type === '期中報告' || w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9);

    let headerBg = 'linear-gradient(135deg, #0f766e 0%, #0ea5e9 100%)';
    let typeIcon = 'fas fa-lightbulb';

    if (isFinal) {
      headerBg = 'linear-gradient(135deg, #4338ca 0%, #06b6d4 100%)';
      typeIcon = 'fas fa-trophy';
    } else if (isMidterm) {
      headerBg = 'linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)';
      typeIcon = 'fas fa-file-invoice';
    }

    const isGraded = (w.score !== null && w.score !== undefined && w.score !== '');
    const scoreBadge = isGraded
      ? `<span class="score-tag graded">🏆 評分：${w.score} 分</span>`
      : `<span class="score-tag pending">⏳ 待評分</span>`;

    const teacherControls = isTeacherUser ? `
      <div style="margin-top:10px; padding-top:8px; border-top:1px dashed #e2e8f0; display:flex; justify-content:flex-end; gap:6px;">
        <button type="button" class="btn-sm" onclick="quickGradeWork('${escapeHtml(w.id)}')" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:11px; cursor:pointer;" title="教師評分">✏️ 快速評分</button>
        <button type="button" class="btn-sm" onclick="teacherDeleteWork('${escapeHtml(w.id)}')" style="background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; font-size:11px; cursor:pointer;" title="刪除此作業">🗑️</button>
      </div>
    ` : '';

    return `
      <div class="work-card">
        <div class="work-card-header" style="background:${headerBg};">
          <div style="display:flex; align-items:center; gap:8px;">
            <i class="${typeIcon}"></i>
            <span style="font-weight:800; font-size:13px;">${escapeHtml(w.report_type || '實作作業')}</span>
          </div>
          <span style="font-size:11px; font-weight:700; background:rgba(255,255,255,0.25); padding:2px 8px; border-radius:10px;">
            第 ${w.week || 1} 週
          </span>
        </div>
        <div class="work-card-body">
          <h4 class="work-card-title">${escapeHtml(w.title || '無標題作品')}</h4>
          <div class="work-card-meta">
            👤 <strong>${escapeHtml(w.student_name || '同學')}</strong> ｜ 
            <span style="font-family:monospace; color:#475569;">${escapeHtml(w.student_id || '進企管四系1甲')}</span>
          </div>
          <div class="work-card-desc">
            ${escapeHtml(w.concept || '無說明摘要')}
          </div>
          ${w.prompt_summary ? `
            <div style="font-size:12px; background:#f8fafc; border-left:3px solid #38bdf8; padding:6px 10px; margin-bottom:10px; border-radius:4px; color:#475569; line-height:1.4;">
              <strong>🤖 AI 應用：</strong>${escapeHtml(w.prompt_summary)}
            </div>
          ` : ''}
          ${(isGraded && w.teacher_comment) ? `
            <div style="font-size:12px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:6px 10px; margin-bottom:10px; color:#166534; line-height:1.4;">
              <strong>👨‍🏫 邱老師回饋：</strong>${escapeHtml(w.teacher_comment)}
            </div>
          ` : ''}
          <div class="work-card-footer">
            <div>${scoreBadge}</div>
            <div>
              <a href="${escapeHtml(w.live_url || '#')}" target="_blank" rel="noopener noreferrer" class="btn-sm btn-primary" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px; font-size:12px; padding:4px 10px;">
                <i class="fas fa-external-link-alt"></i> 查看成果
              </a>
            </div>
          </div>
          ${teacherControls}
        </div>
      </div>
    `;
  }).join('');
}

/* ==========================================================================
   TEACHER MANAGEMENT DASHBOARD & GRADING
   ========================================================================== */

function renderTeacherGradeDashboard() {
  if (!isTeacherUser) return;
  const tbody = document.getElementById('teacher-grades-tbody');
  if (!tbody) return;

  const totalWorks = studentWorksData || [];

  let midtermCount = 0;
  let finalCount = 0;
  let gradedCount = 0;
  let pendingCount = 0;
  let scoreSum = 0;
  let scoreCount = 0;

  totalWorks.forEach(w => {
    const isFinal = (w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18);
    const isMidterm = (w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9);

    if (isFinal) finalCount++;
    else if (isMidterm) midtermCount++;

    if (w.score !== null && w.score !== undefined && w.score !== '') {
      gradedCount++;
      const s = Number(w.score);
      if (!isNaN(s)) {
        scoreSum += s;
        scoreCount++;
      }
    } else {
      pendingCount++;
    }
  });

  const avgScore = scoreCount > 0 ? (scoreSum / scoreCount).toFixed(1) + ' 分' : '尚無評分';

  const statTotal = document.getElementById('teacher-stat-total');
  const statMidterm = document.getElementById('teacher-stat-midterm');
  const statFinal = document.getElementById('teacher-stat-final');
  const statPending = document.getElementById('teacher-stat-pending');
  const statGraded = document.getElementById('teacher-stat-graded');
  const statAvg = document.getElementById('teacher-stat-avg');

  if (statTotal) statTotal.textContent = totalWorks.length;
  if (statMidterm) statMidterm.textContent = midtermCount;
  if (statFinal) statFinal.textContent = finalCount;
  if (statPending) statPending.textContent = pendingCount;
  if (statGraded) statGraded.textContent = gradedCount;
  if (statAvg) statAvg.textContent = avgScore;

  // Filter toolbar values
  const searchQ = (document.getElementById('teacher-search-input')?.value || '').trim().toLowerCase();
  const filterCat = document.getElementById('teacher-filter-category')?.value || 'all';
  const filterStat = document.getElementById('teacher-filter-status')?.value || 'all';

  const filtered = totalWorks.filter(w => {
    if (searchQ) {
      const matchText = `${w.student_id || ''} ${w.student_name || ''} ${w.title || ''} ${w.concept || ''}`.toLowerCase();
      if (!matchText.includes(searchQ)) return false;
    }
    if (filterCat !== 'all') {
      if ((filterCat === '期中報告' || filterCat === '期中實作') && w.report_type !== '期中報告' && w.report_type !== '期中實作' && w.week !== 9) return false;
      if (filterCat === '期末成果' && w.report_type !== '期末成果' && w.week !== 18) return false;
      if ((filterCat === '自主練習' || filterCat === '平時作業') && (w.report_type === '期中報告' || w.report_type === '期中實作' || w.report_type === '期末成果' || w.week === 9 || w.week === 18)) return false;
    }
    const isGraded = (w.score !== null && w.score !== undefined && w.score !== '');
    if (filterStat === 'graded' && !isGraded) return false;
    if (filterStat === 'pending' && isGraded) return false;
    return true;
  });

  const countElem = document.getElementById('teacher-filtered-count');
  if (countElem) countElem.textContent = `顯示 ${filtered.length} / ${totalWorks.length} 筆`;

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" style="text-align:center; padding:40px; color:#94a3b8;">
          <i class="fas fa-inbox" style="font-size:32px; display:block; margin-bottom:8px; opacity:0.5;"></i>
          尚無符合篩選條件的學生專案成果
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.map(w => {
    const isFinal = (w.report_type === '期末成果' || w.week === 18);
    const isMidterm = (w.report_type === '期中報告' || w.report_type === '期中實作' || w.week === 9);
    let catBadge = `<span style="background:#f1f5f9; color:#475569; font-weight:700; padding:2px 8px; border-radius:10px; font-size:11px;">💡 自主練習</span>`;
    if (isFinal) {
      catBadge = `<span style="background:#e0e7ff; color:#3730a3; font-weight:700; padding:2px 8px; border-radius:10px; font-size:11px;">🏆 期末成果</span>`;
    } else if (isMidterm) {
      catBadge = `<span style="background:#dbeafe; color:#1e40af; font-weight:700; padding:2px 8px; border-radius:10px; font-size:11px;">📌 期中報告</span>`;
    }

    const currentScore = (w.score !== null && w.score !== undefined) ? w.score : '';
    const currentComment = w.teacher_comment || '';

    return `
      <tr id="grade-row-${escapeHtml(w.id)}">
        <td><strong style="font-family:monospace; color:#2563eb;">${escapeHtml(w.student_id || '無學號')}</strong></td>
        <td><strong>${escapeHtml(w.student_name || '同學')}</strong></td>
        <td>${catBadge}</td>
        <td>
          <div style="font-weight:700; color:var(--primary-navy);">${escapeHtml(w.title || '無標題')}</div>
          <div style="font-size:11px; color:#64748b; max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${escapeHtml(w.concept || '')}">
            ${escapeHtml(w.concept || '')}
          </div>
        </td>
        <td>
          <a href="${escapeHtml(w.live_url || '#')}" target="_blank" rel="noopener noreferrer" style="color:#2563eb; text-decoration:underline; font-size:12px; display:inline-flex; align-items:center; gap:4px;">
            <i class="fas fa-external-link-alt"></i> 開啟
          </a>
        </td>
        <td style="font-size:11px; color:#64748b;">${escapeHtml(w.submitted_at || '-')}</td>
        <td>
          <input type="number" id="grade-score-${escapeHtml(w.id)}" value="${currentScore}" min="0" max="100" placeholder="分數" style="width:65px; padding:4px 6px; border:1px solid #cbd5e1; border-radius:6px; font-weight:700; text-align:center;">
        </td>
        <td>
          <input type="text" id="grade-comment-${escapeHtml(w.id)}" value="${escapeHtml(currentComment)}" placeholder="評語..." style="width:160px; padding:4px 8px; border:1px solid #cbd5e1; border-radius:6px; font-size:12px;">
        </td>
        <td style="text-align:center;">
          <button type="button" class="btn-sm btn-primary" onclick="teacherSaveTableGrade('${escapeHtml(w.id)}')" style="padding:4px 8px; font-size:11px; cursor:pointer;" title="儲存此筆給分">💾</button>
          <button type="button" class="btn-sm" onclick="teacherDeleteWork('${escapeHtml(w.id)}')" style="padding:4px 8px; font-size:11px; background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; cursor:pointer;" title="刪除作業">🗑️</button>
        </td>
      </tr>
    `;
  }).join('');
}

async function quickGradeWork(workId) {
  const work = studentWorksData.find(w => w.id === workId);
  if (!work) return;

  const currentScore = (work.score !== null && work.score !== undefined) ? work.score : '';
  const scoreInput = prompt(`請輸入【${work.student_name} (${work.student_id})】的成績 (0 ~ 100)：`, currentScore);
  if (scoreInput === null) return;
  const numScore = parseFloat(scoreInput.trim());
  if (isNaN(numScore) || numScore < 0 || numScore > 100) {
    alert('成績請輸入 0 至 100 之數值！');
    return;
  }
  const commentInput = prompt('請輸入給學生的教師回饋評語：', work.teacher_comment || '實作完整，結構嚴謹，符合商務軟體應用規範！');
  if (commentInput === null) return;

  work.score = numScore;
  work.teacher_comment = commentInput.trim();

  if (firestoreDb) {
    try {
      await firestoreDb.collection('works').doc(workId).set({
        score: numScore,
        teacher_comment: work.teacher_comment,
        gradedAt: firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true });
      console.log('成績已同步至 Firestore');
    } catch (e) {
      console.warn('Firestore 更新成績失敗:', e);
    }
  }

  try {
    const localWorks = JSON.parse(localStorage.getItem('vnu_bsa_submitted_works') || '[]');
    const idx = localWorks.findIndex(w => w.id === workId);
    if (idx >= 0) {
      localWorks[idx].score = numScore;
      localWorks[idx].teacher_comment = work.teacher_comment;
      localStorage.setItem('vnu_bsa_submitted_works', JSON.stringify(localWorks));
    }
  } catch (e) {}

  renderStudentWorks(currentWorksFilter);
  if (isTeacherUser) renderTeacherGradeDashboard();
  alert(`✅ 已成功為【${work.student_name}】評定成績：${numScore} 分！`);
}

async function teacherSaveTableGrade(workId) {
  const scoreInput = document.getElementById(`grade-score-${workId}`);
  const commentInput = document.getElementById(`grade-comment-${workId}`);
  if (!scoreInput) return;

  const rawScore = scoreInput.value.trim();
  if (rawScore === '') {
    alert('請輸入有效分數！');
    scoreInput.focus();
    return;
  }
  const numScore = parseFloat(rawScore);
  if (isNaN(numScore) || numScore < 0 || numScore > 100) {
    alert('分數必須介於 0 至 100 之間！');
    scoreInput.focus();
    return;
  }

  const commentText = commentInput ? commentInput.value.trim() : '';

  const work = studentWorksData.find(w => w.id === workId);
  if (work) {
    work.score = numScore;
    work.teacher_comment = commentText;
  }

  if (firestoreDb) {
    try {
      await firestoreDb.collection('works').doc(workId).set({
        score: numScore,
        teacher_comment: commentText,
        gradedAt: firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true });
      console.log('評分成功同步至 Firestore:', workId);
    } catch (e) {
      console.warn('Firestore 儲存評分警告:', e);
    }
  }

  try {
    const localWorks = JSON.parse(localStorage.getItem('vnu_bsa_submitted_works') || '[]');
    const idx = localWorks.findIndex(w => w.id === workId);
    if (idx >= 0) {
      localWorks[idx].score = numScore;
      localWorks[idx].teacher_comment = commentText;
      localStorage.setItem('vnu_bsa_submitted_works', JSON.stringify(localWorks));
    }
  } catch (e) {}

  renderTeacherGradeDashboard();
  renderStudentWorks(currentWorksFilter);
  alert(`✅ 已成功儲存給分：${numScore} 分！`);
}

async function teacherDeleteWork(workId) {
  if (!confirm('⚠️ 確定要刪除此筆作業資料嗎？此操作無法復原。')) return;

  if (firestoreDb) {
    try {
      await firestoreDb.collection('works').doc(workId).delete();
      console.log('作業已自 Firestore 刪除:', workId);
    } catch (e) {
      console.warn('Firestore 刪除失敗:', e);
    }
  }

  studentWorksData = studentWorksData.filter(w => w.id !== workId);
  try {
    const localWorks = JSON.parse(localStorage.getItem('vnu_bsa_submitted_works') || '[]');
    const newLocal = localWorks.filter(w => w.id !== workId);
    localStorage.setItem('vnu_bsa_submitted_works', JSON.stringify(newLocal));
  } catch (e) {}

  renderTeacherGradeDashboard();
  renderStudentWorks(currentWorksFilter);
  alert('已成功刪除該筆作業！');
}

function exportGradesToCSV() {
  if (!studentWorksData || studentWorksData.length === 0) {
    alert('目前尚無任何作業繳交資料可供匯出！');
    return;
  }

  const headers = ['學號', '姓名', '班級', '作業類別', '作品名稱', '成果公開網址', '繳交時間', '成績', '教師評語'];
  const rows = [headers];

  studentWorksData.forEach(w => {
    rows.push([
      w.student_id || '',
      w.student_name || '',
      w.class_name || '進企管四系1甲',
      w.report_type || '',
      w.title || '',
      w.live_url || '',
      w.submitted_at || '',
      (w.score !== null && w.score !== undefined) ? w.score : '未評分',
      w.teacher_comment || ''
    ]);
  });

  const csvContent = '\uFEFF' + rows.map(r => r.map(field => `"${String(field).replace(/"/g, '""')}"`).join(',')).join('\r\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const dateStr = new Date().toISOString().slice(0, 10);
  a.href = url;
  a.download = `萬能科技大學_商業軟體應用_進企管四系1甲_作業成績總表_${dateStr}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Global Window Exports for Inline HTML Handlers
window.initFirebase = initFirebase;
window.loginWithGoogle = loginWithGoogle;
window.logoutUser = logoutUser;
window.openModal = openModal;
window.closeModal = closeModal;
window.toggleUserMenu = toggleUserMenu;
window.saveUserProfileModal = saveUserProfileModal;
window.handleProjectSubmit = handleProjectSubmit;
window.filterWorks = filterWorks;
window.renderStudentWorks = renderStudentWorks;
window.quickGradeWork = quickGradeWork;
window.teacherSaveTableGrade = teacherSaveTableGrade;
window.teacherDeleteWork = teacherDeleteWork;
window.exportGradesToCSV = exportGradesToCSV;
window.renderTeacherGradeDashboard = renderTeacherGradeDashboard;
window.changePresenterFontSize = changePresenterFontSize;
window.resetPresenterFontSize = resetPresenterFontSize;


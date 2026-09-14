/**
 * 萬能科技大學 - 商業軟體應用 ✕ Agentic AI ✕ iPAS AI 應用規劃師
 * 前端核心邏輯與互動系統 (支援在線 API 與單機離線雙模)
 * 授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu)
 */

// Global State
const state = {
  curriculum: null,
  agentTemplates: [],
  ipasGuide: null,
  questions: [],
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
  await loadPlatformData();
  setupNavigation();
  setupKeyboardShortcuts();
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
    console.log("Loaded offline embedded dataset.");
    return;
  }

  try {
    const [currRes, agentRes, ipasRes, qRes] = await Promise.all([
      fetch('/api/curriculum').then(r => r.json()),
      fetch('/api/agent_templates').then(r => r.json()),
      fetch('/api/ipas_guide').then(r => r.json()),
      fetch('/api/questions?count=300&shuffle=false').then(r => r.json())
    ]);
    state.curriculum = currRes;
    state.agentTemplates = agentRes;
    state.ipasGuide = ipasRes;
    state.questions = qRes.questions || [];
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
  state.currentTab = tabId;
  document.querySelectorAll('.nav-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tabId);
  });
  document.querySelectorAll('.content-section').forEach(sec => {
    sec.classList.toggle('active', sec.id === `sec-${tabId}`);
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render All Sections
function renderAllSections() {
  renderOrientationSection();
  renderCurriculumSection();
  renderAgentStudioSection();
  renderIpasGuideSection();
  renderAchievements();
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
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:16px;">
        ${grading_policy.breakdown.map(b => `
          <div style="background:#ffffff; border:1px solid var(--border-color); border-radius:10px; padding:16px; border-left:5px solid var(--primary-blue);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:700; color:var(--primary-navy); font-size:15px;">${b.item}</span>
              <span style="font-size:20px; font-weight:900; color:var(--accent-amber);">${b.percentage}</span>
            </div>
            <div style="font-size:12.5px; color:#64748b; margin-top:6px;">${b.description}</div>
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
          <button class="btn-sm btn-amber" onclick="openSlidePresenter(${w.week}, 0)">
            🖥️ 播放本週簡報 (61頁)
          </button>
          <button class="btn-sm btn-primary" onclick="startQuickQuiz(${w.week})">
            📝 隨堂快測 (5題)
          </button>
        </div>
      </div>
      <div class="week-body-grid">
        <div class="week-info-block">
          <strong>課堂痛點破冰 (Hook)</strong>
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
          <strong>成果反思與指標 (Wrap-up)</strong>
          <div>${w.wrapup}</div>
        </div>
      </div>
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

// Start Quizzes
function startQuickQuiz(weekNum) {
  switchTab('ipas');
  startExam('weekly_5', `第 ${weekNum} 週 隨堂 5 題快測`, weekNum);
}

function startExamMode(mode) {
  if (mode === 'weekly_5') {
    const week = prompt("請輸入欲進行快測的週次 (1 到 18)：", "1");
    if (week && parseInt(week) >= 1 && parseInt(week) <= 18) {
      startExam('weekly_5', `第 ${week} 週 隨堂 5 題快測`, parseInt(week));
    }
  } else if (mode === 'chapter') {
    const mod = prompt("請輸入測驗模組關鍵字 (如: Word, Excel, PPT, Agentic, 資安)：", "Excel");
    if (mod) startExam('chapter', `【${mod}】單元自主精熟練習`, null, mod);
  } else if (mode === 'midterm_50') {
    if (confirm("即將開始【期中 50 題自我檢測】\n• 涵蓋第 1 至 9 週重點觀念\n• 限時 60 分鐘\n• 及格門檻 70 分\n準備好立即開始？")) {
      startExam('midterm_50', "iPAS 期中 50 題自我檢測 (限時 60 分鐘)");
    }
  } else if (mode === 'final_100') {
    if (confirm("即將開始【期末 100 題綜合自我評量】\n• 涵蓋全學期 18 週題庫\n• 限時 100 分鐘\n• 及格門檻 70 分\n準備好立即開始？")) {
      startExam('final_100', "iPAS 期末 100 題綜合自我評量 (限時 100 分鐘)");
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
    { id: 'badge_top_scorer', name: '榮譽榜首高分王', desc: '自我評量取得 90 分以上卓越成績', icon: '👑' }
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
  if (!sel || !window.COURSE_SLIDES_DATA) return;

  sel.innerHTML = window.COURSE_SLIDES_DATA.weeks.map(w => `
    <option value="${w.week}" ${w.week === state.presenter.currentWeek ? 'selected' : ''}>
      第 ${String(w.week).padStart(2, '0')} 週：${w.title}
    </option>
  `).join('');
}

function onPresenterWeekChange() {
  const sel = document.getElementById('presenterWeekSelect');
  if (sel) {
    state.presenter.currentWeek = parseInt(sel.value);
    state.presenter.currentSlideIdx = 0;
    renderPresenterSlide();
  }
}

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

  let bodyContent = '';
  if (slide.type === 'title') {
    bodyContent = `
      <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:40px;">
        <span class="badge-pill" style="font-size:16px; margin-bottom:16px; background:#d97706;">${slide.badge}</span>
        <h1 style="font-size:42px; font-weight:900; color:#1e3a8a; margin-bottom:16px; line-height:1.25;">${slide.title}</h1>
        <div style="font-size:22px; color:#475569; max-width:1000px; white-space:pre-line;">${slide.subtitle}</div>
      </div>
    `;
  } else if (slide.type === 'step') {
    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#1e3a8a;">${slide.badge}</span>
            <h2 style="font-size:28px; font-weight:800; color:#1e3a8a; margin-top:4px;">${slide.title}</h2>
            <div style="font-size:16px; color:#64748b;">${slide.subtitle}</div>
          </div>
          <div style="font-size:13px; font-weight:700; color:#94a3b8;">${slide.sec} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: 2fr 1fr; gap:20px; align-items:stretch;">
          <div style="background:#f8fafc; border:2px solid #e2e8f0; border-top:6px solid #1e3a8a; border-radius:12px; padding:20px;">
            <h4 style="color:#1e3a8a; font-weight:800; margin-bottom:10px;">動作 SOP 步驟</h4>
            <div style="font-size:18px; color:#1e293b; line-height:1.7;">${slide.step_desc}</div>
          </div>
          <div style="background:#f8fafc; border:2px solid #e2e8f0; border-top:6px solid #d97706; border-radius:12px; padding:20px;">
            <h4 style="color:#d97706; font-weight:800; margin-bottom:10px;">💡 關鍵眉角與秘訣</h4>
            <div style="font-size:16px; color:#475569; line-height:1.6;">${slide.step_tip}</div>
          </div>
        </div>
      </div>
    `;
  } else {
    // General Cards Layout
    const cardsHtml = (slide.cards || []).map(c => `
      <div style="background:#f8fafc; border:2px solid #e2e8f0; border-top:6px solid ${c.theme === 'amber' ? '#d97706' : c.theme === 'emerald' ? '#059669' : '#1e3a8a'}; border-radius:12px; padding:20px; display:flex; flex-direction:column;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <span style="font-size:18px; font-weight:800; color:#1e293b;">${c.title}</span>
          <span style="font-size:12px; font-weight:700; padding:2px 8px; border-radius:10px; background:#e2e8f0;">${c.tag || '重點'}</span>
        </div>
        <div style="font-size:16px; color:#334155; line-height:1.6; flex:1;">${c.content}</div>
      </div>
    `).join('');

    bodyContent = `
      <div style="display:flex; flex-direction:column; height:100%;">
        <div style="padding:16px 36px; border-bottom:2px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; background:#f8fafc;">
          <div>
            <span class="badge-pill" style="background:#1e3a8a;">${slide.badge}</span>
            <h2 style="font-size:28px; font-weight:800; color:#1e3a8a; margin-top:4px;">${slide.title}</h2>
            <div style="font-size:16px; color:#64748b;">${slide.subtitle}</div>
          </div>
          <div style="font-size:13px; font-weight:700; color:#94a3b8;">${slide.sec} ｜ 頁碼 ${slide.num}</div>
        </div>
        <div style="flex:1; padding:24px 36px; display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:20px; align-items:stretch;">
          ${cardsHtml}
        </div>
      </div>
    `;
  }

  stage.innerHTML = bodyContent;

  // Speaker notes
  const notesText = document.getElementById('speakerNotesText');
  if (notesText) {
    notesText.textContent = slide.speaker_note || "本頁尚無演講者備忘稿。";
  }
}

function nextPresenterSlide() {
  const weekSlides = window.COURSE_SLIDES_DATA.slidesByWeek[String(state.presenter.currentWeek)] || [];
  if (state.presenter.currentSlideIdx < weekSlides.length - 1) {
    state.presenter.currentSlideIdx++;
    renderPresenterSlide();
  } else if (state.presenter.currentWeek < 18) {
    if (confirm("已到達本週最後一頁，是否切換至下一週？")) {
      state.presenter.currentWeek++;
      state.presenter.currentSlideIdx = 0;
      populatePresenterWeekSelector();
      renderPresenterSlide();
    }
  }
}

function prevPresenterSlide() {
  if (state.presenter.currentSlideIdx > 0) {
    state.presenter.currentSlideIdx--;
    renderPresenterSlide();
  } else if (state.presenter.currentWeek > 1) {
    if (confirm("已在第一頁，是否切換回上一週？")) {
      state.presenter.currentWeek--;
      state.presenter.currentSlideIdx = 0;
      populatePresenterWeekSelector();
      renderPresenterSlide();
    }
  }
}

function togglePresenterSpeakerNotes() {
  state.presenter.isNotesOpen = !state.presenter.isNotesOpen;
  const drawer = document.getElementById('presenterNotesDrawer');
  if (drawer) drawer.style.display = state.presenter.isNotesOpen ? 'block' : 'none';
}

function togglePresenterFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(e => alert("全螢幕切換受限：" + e.message));
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
  }
}

// Global Keyboard Shortcuts
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

    if (state.presenter.isOpen) {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
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

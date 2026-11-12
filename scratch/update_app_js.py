# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JS_PATH = os.path.join(BASE_DIR, "static", "js", "app.js")

with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add isTeacherWork helper right before filterWorks if not present
is_teacher_func = '''function isTeacherWork(w) {
  if (!w) return false;
  if (w.student_id === 'TEACHER') return true;
  if (w.id && String(w.id).startsWith('DEMO-')) return true;
  if (w.student_group === '授課教師示範' || w.team_name === '授課教師示範') return true;
  const name = String(w.student_name || '');
  if (name.includes('邱俊維') || name.includes('教師') || name.includes('授課教師') || name.includes('邱老師')) return true;
  const author = String(w.author || '');
  if (author.includes('邱俊維') || author.includes('教師') || author.includes('授課教師') || author.includes('邱老師')) return true;
  const em = String(w.email || w.user_email || '').toLowerCase();
  if (em && TEACHER_EMAILS.some(t => em.includes(t.toLowerCase()))) return true;
  return false;
}
'''

# Find filterWorks
target_start = "function filterWorks(category, btn) {"
if target_start not in code:
    print("ERROR: cannot find function filterWorks")
    exit(1)

# Find renderTeacherGradeDashboard start
target_dashboard = "function renderTeacherGradeDashboard() {"
if target_dashboard not in code:
    print("ERROR: cannot find function renderTeacherGradeDashboard")
    exit(1)

# Replace filterWorks through end of renderStudentWorks
part_before = code[:code.find(target_start)]
part_dashboard_and_after = code[code.find(target_dashboard):]

new_block = is_teacher_func + '''
function filterWorks(category, btn) {
  currentWorksFilter = category;
  document.querySelectorAll('.gallery-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) {
    btn.classList.add('active');
  } else {
    const target = document.querySelector(`.gallery-filter-btn[data-filter="${category}"]`);
    if (target) target.classList.add('active');
  }
  renderStudentWorks(currentWorksFilter);
}

function renderStudentWorks(filter = currentWorksFilter) {
  const grid = document.getElementById('studentWorksGrid');
  const countSpan = document.getElementById('gallery-total-count');
  const categoryLabel = document.getElementById('gallery-category-label');
  if (!grid) return;

  const totalWorks = studentWorksData || [];
  const studentWorks = totalWorks.filter(w => !isTeacherWork(w));

  // 1. 各分類之學生實作數量（嚴格排除授課教師示範專案）
  const countAll = studentWorks.length;
  const countMidterm = studentWorks.filter(w => 
    w.report_type === '期中報告' || w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9
  ).length;
  const countFinal = studentWorks.filter(w => 
    w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18
  ).length;
  const countPractice = studentWorks.filter(w => 
    w.report_type === '自主練習' || w.report_type === '平時作業' || (w.week !== 9 && w.week !== 18)
  ).length;
  const countMine = totalWorks.filter(w => {
    if (currentFirebaseUser && w.uid && w.uid === currentFirebaseUser.uid) return true;
    if (state.student.id && w.student_id === state.student.id) return true;
    return false;
  }).length;

  // 2. 即時更新下方各分類按鈕之數量角標 (badge-count)
  const btnAll = document.querySelector('.gallery-filter-btn[data-filter="all"]');
  const btnMidterm = document.querySelector('.gallery-filter-btn[data-filter="期中報告"]');
  const btnFinal = document.querySelector('.gallery-filter-btn[data-filter="期末成果"]');
  const btnPractice = document.querySelector('.gallery-filter-btn[data-filter="自主練習"]');
  const btnMine = document.querySelector('.gallery-filter-btn[data-filter="mine"]');

  if (btnAll) btnAll.innerHTML = `全部展示 <span class="badge-count">(${countAll})</span>`;
  if (btnMidterm) btnMidterm.innerHTML = `📌 期中報告 <span class="badge-count">(${countMidterm})</span>`;
  if (btnFinal) btnFinal.innerHTML = `🏆 期末成果 <span class="badge-count">(${countFinal})</span>`;
  if (btnPractice) btnPractice.innerHTML = `💡 自主練習 <span class="badge-count">(${countPractice})</span>`;
  if (btnMine) btnMine.innerHTML = `👤 我的作品 <span class="badge-count">(${countMine})</span>`;

  // 3. 依據目前點選的字卡切換，動態改變頂部「共收錄 X 件實作專案」之數值與前綴（排除教師專案）
  let activeStudentCount = countAll;
  let activeName = '';
  if (filter === '期中報告' || filter === '期中實作') {
    activeStudentCount = countMidterm;
    activeName = '期中報告';
  } else if (filter === '期末成果') {
    activeStudentCount = countFinal;
    activeName = '期末成果';
  } else if (filter === '自主練習' || filter === '平時作業') {
    activeStudentCount = countPractice;
    activeName = '自主練習';
  } else if (filter === 'mine') {
    activeStudentCount = countMine;
    activeName = '我的作品';
  } else {
    activeStudentCount = countAll;
    activeName = '';
  }

  if (countSpan) countSpan.textContent = activeStudentCount;
  if (categoryLabel) categoryLabel.textContent = activeName ? `${activeName} ` : '';

  // 4. 篩選展示廊要呈現的卡片清單
  const filtered = totalWorks.filter(w => {
    if (filter === 'all') return true;
    if (filter === '期中報告' || filter === '期中實作') {
      return w.report_type === '期中報告' || w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9;
    }
    if (filter === '期末成果') {
      return w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18;
    }
    if (filter === '自主練習' || filter === '平時作業') {
      if (isTeacherWork(w)) return false;
      return w.report_type === '自主練習' || w.report_type === '平時作業' || (w.week !== 9 && w.week !== 18);
    }
    if (filter === 'mine') {
      if (currentFirebaseUser && w.uid && w.uid === currentFirebaseUser.uid) return true;
      if (state.student.id && w.student_id === state.student.id) return true;
      return false;
    }
    return true;
  });

  // 教師示範標竿置頂展示，方便學生參考觀摩，其餘按繳交時間降序排列
  filtered.sort((a, b) => {
    const aIsTeacher = isTeacherWork(a) ? 1 : 0;
    const bIsTeacher = isTeacherWork(b) ? 1 : 0;
    if (aIsTeacher !== bIsTeacher) return bIsTeacher - aIsTeacher;
    return (b.submitted_at || '').localeCompare(a.submitted_at || '');
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
    const isTeacher = isTeacherWork(w);
    const isFinal = (w.report_type === '期末成果' || (w.week_title && w.week_title.includes('期末')) || w.week === 18);
    const isMidterm = (w.report_type === '期中報告' || w.report_type === '期中實作' || (w.week_title && w.week_title.includes('期中')) || w.week === 9);

    let headerBg = 'linear-gradient(135deg, #0f766e 0%, #0ea5e9 100%)';
    let typeIcon = 'fas fa-lightbulb';

    if (isTeacher) {
      headerBg = 'linear-gradient(135deg, #1e293b 0%, #0284c7 100%)';
      typeIcon = 'fas fa-chalkboard-teacher';
    } else if (isFinal) {
      headerBg = 'linear-gradient(135deg, #4338ca 0%, #06b6d4 100%)';
      typeIcon = 'fas fa-trophy';
    } else if (isMidterm) {
      headerBg = 'linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)';
      typeIcon = 'fas fa-file-invoice';
    }

    const isGraded = (w.score !== null && w.score !== undefined && w.score !== '');
    let scoreBadge = '';
    if (isTeacher) {
      scoreBadge = `<span class="score-tag graded" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a;">🌟 示範標竿 (100分)</span>`;
    } else {
      scoreBadge = isGraded
        ? `<span class="score-tag graded">🏆 評分：${w.score} 分</span>`
        : `<span class="score-tag pending">⏳ 待評分</span>`;
    }

    const teacherControls = (isTeacherUser && !isTeacher) ? `
      <div style="margin-top:10px; padding-top:8px; border-top:1px dashed #e2e8f0; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:10px; font-weight:700; color:#dc2626; background:#fee2e2; padding:2px 6px; border-radius:4px;"><i class="fas fa-user-shield"></i> 邱老師專屬管理</span>
        <div style="display:flex; gap:6px;">
          <button type="button" class="btn-sm" onclick="quickGradeWork('${escapeHtml(w.id)}')" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:11px; cursor:pointer;" title="教師評分">✏️ 快速評分</button>
          <button type="button" class="btn-sm" onclick="teacherDeleteWork('${escapeHtml(w.id)}')" style="background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; font-size:11px; cursor:pointer;" title="刪除此作業">🗑️</button>
        </div>
      </div>
    ` : '';

    return `
      <div class="work-card">
        <div class="work-card-header" style="background:${headerBg};">
          <div style="display:flex; align-items:center; gap:8px;">
            <i class="${typeIcon}"></i>
            <span style="font-weight:800; font-size:13px;">${isTeacher ? `👨‍🏫 教師示範（${escapeHtml(w.report_type || '專案')}）` : escapeHtml(w.report_type || '實作作業')}</span>
          </div>
          <span style="font-size:11px; font-weight:700; background:rgba(255,255,255,0.25); padding:2px 8px; border-radius:10px;">
            第 ${w.week || 1} 週
          </span>
        </div>
        <div class="work-card-body">
          <h4 class="work-card-title">${escapeHtml(w.title || '無標題作品')}</h4>
          <a href="${escapeHtml(w.live_url || '#')}" target="_blank" rel="noopener noreferrer" class="work-preview-container" title="點擊開啟專案成果網頁">
            <img src="https://image.thum.io/get/width/600/crop/800/${encodeURI(w.live_url || '')}" 
                 alt="網站即時預覽圖" 
                 class="work-preview-img" 
                 loading="lazy" 
                 onerror="this.onerror=null; this.src='https://api.microlink.io/?url=' + encodeURIComponent('${encodeURI(w.live_url || '')}') + '&screenshot=true&meta=false';">
            <div class="work-preview-overlay">
              <i class="fas fa-external-link-alt"></i> 點擊造訪成果網站
            </div>
          </a>
          <div class="work-card-meta">
            ${isTeacher ? `
              👨‍🏫 <strong>${escapeHtml(w.student_name || '邱俊維 博士')}</strong> ｜ 
              <span style="background:#fef3c7; color:#b45309; padding:2px 8px; border-radius:6px; font-weight:700; font-size:11px;">授課教師示範專案</span>
            ` : `
              👤 <strong>${escapeHtml(w.student_name || '同學')}</strong> ｜ 
              <span style="font-family:monospace; color:#475569;">${escapeHtml(w.student_id || '進企管四系1甲')}</span>
            `}
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

'''

# Also update renderTeacherGradeDashboard to exclude teacher works from student grade stats
dashboard_code = part_dashboard_and_after.replace(
    "const totalWorks = studentWorksData || [];",
    "const totalWorks = (studentWorksData || []).filter(w => !isTeacherWork(w));"
)

# Also update teacherCleanupDuplicates and exportGradesToCSV if needed
dashboard_code = dashboard_code.replace(
    "// Skip teacher demo works\n    if (w.id && w.id.startsWith('DEMO-')) return;",
    "// Skip teacher demo works\n    if (isTeacherWork(w)) return;"
)
dashboard_code = dashboard_code.replace(
    "studentWorksData.forEach(w => {\n    rows.push([",
    "studentWorksData.forEach(w => {\n    if (isTeacherWork(w)) return;\n    rows.push(["
)

full_code = part_before + new_block + dashboard_code
with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(full_code)

print("SUCCESS: Updated static/js/app.js")

# -*- coding: utf-8 -*-
"""
萬能科技大學 - 商業軟體應用 (11501) ✕ Agentic AI ✕ iPAS AI 應用規劃師
全方位互動教學與考證平台
授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu)
"""
import os
import sys
import json
import socket
import random
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    return {}

def get_local_ip():
    """Get LAN IP address for classroom projection and student connection"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return '127.0.0.1'

# In-memory storage for classroom quiz submissions & live activity feed
CLASSROOM_RECORDS = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/slides_data.js')
def get_slides_data():
    """Serve slides_data.js directly from workspace root"""
    return send_from_directory(BASE_DIR, 'slides_data.js', mimetype='application/javascript')

@app.route('/api/system_info')
def system_info():
    local_ip = get_local_ip()
    port = 5000
    return jsonify({
        'status': 'online',
        'course': '萬能科技大學 - 商業軟體應用 (11501)',
        'instructor': '邱俊維 博士 (Dr. Chun-Wei Chiu)',
        'target_class': '進企管四系 1 甲 (J501 企業經營模擬室)',
        'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'local_ip': local_ip,
        'classroom_url': f"http://{local_ip}:{port}",
        'total_submissions': len(CLASSROOM_RECORDS)
    })

@app.route('/api/curriculum')
def get_curriculum():
    data = load_json_file('curriculum.json')
    return jsonify(data)

@app.route('/api/agent_templates')
def get_agent_templates():
    data = load_json_file('agent_templates.json')
    return jsonify(data)

@app.route('/api/ipas_guide')
def get_ipas_guide():
    data = load_json_file('ipas_guide.json')
    return jsonify(data)

@app.route('/api/sample_works')
def get_sample_works():
    data = load_json_file('sample_works.json')
    return jsonify(data)

@app.route('/api/questions')
def get_questions():
    all_q = load_json_file('questions.json')
    if not isinstance(all_q, list):
        all_q = []
    
    # Query parameters
    week = request.args.get('week', type=int)
    chapter = request.args.get('chapter', type=int)
    module = request.args.get('module')
    subject = request.args.get('subject')
    count = request.args.get('count', type=int)
    shuffle = request.args.get('shuffle', default='true').lower() == 'true'
    exam_type = request.args.get('exam_type') # 'weekly_5', 'midterm_50', 'final_100'

    filtered = all_q
    if week:
        filtered = [q for q in filtered if week in q.get('weeks', [])]
    elif chapter:
        filtered = [q for q in filtered if q.get('chapter') == chapter]
    elif module:
        filtered = [q for q in filtered if q.get('module') == module]
    elif subject:
        filtered = [q for q in filtered if q.get('subject') == subject]
    
    if exam_type == 'weekly_5':
        count = 5
    elif exam_type == 'midterm_50':
        # First half: Weeks 1 to 9
        filtered = [q for q in filtered if any(w <= 9 for w in q.get('weeks', []))]
        count = 50
    elif exam_type == 'final_100':
        count = 100

    if shuffle:
        filtered = list(filtered)
        random.shuffle(filtered)

    if count and count > 0:
        filtered = filtered[:count]

    return jsonify({
        'total_matched': len(filtered),
        'questions': filtered
    })

@app.route('/api/submit_quiz', methods=['POST'])
def submit_quiz():
    """Score quiz submissions, provide radar analysis and explanations"""
    payload = request.get_json() or {}
    student_id = payload.get('student_id', '匿名學生')
    student_name = payload.get('student_name', '訪客')
    answers = payload.get('answers', {}) # {str(question_id): selected_option_int}
    
    all_q = load_json_file('questions.json')
    all_q_map = {q['id']: q for q in all_q}
    
    total = len(answers)
    if total == 0:
        return jsonify({'error': '未提供任何作答'}), 400

    correct_count = 0
    details = []
    module_stats = {}
    subject_stats = {}

    for q_id_str, user_ans in answers.items():
        try:
            q_id = int(q_id_str)
        except ValueError:
            continue
        q_item = all_q_map.get(q_id)
        if not q_item:
            continue
        
        is_correct = (user_ans == q_item['answer'])
        if is_correct:
            correct_count += 1

        mod = q_item.get('module', '綜合商業應用')
        if mod not in module_stats:
            module_stats[mod] = {'total': 0, 'correct': 0}
        module_stats[mod]['total'] += 1
        if is_correct:
            module_stats[mod]['correct'] += 1

        subj = q_item.get('subject', '科目二')
        if subj not in subject_stats:
            subject_stats[subj] = {'total': 0, 'correct': 0}
        subject_stats[subj]['total'] += 1
        if is_correct:
            subject_stats[subj]['correct'] += 1

        details.append({
            'id': q_id,
            'question': q_item['question'],
            'options': q_item['options'],
            'user_answer': user_ans,
            'correct_answer': q_item['answer'],
            'is_correct': is_correct,
            'explanation': q_item['explanation'],
            'module': mod,
            'subject': subj,
            'chapter': q_item.get('chapter', 1)
        })

    score = round((correct_count / total) * 100, 1)
    passed = score >= 70.0

    record = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'student_id': student_id,
        'student_name': student_name,
        'score': score,
        'correct_count': correct_count,
        'total': total,
        'passed': passed
    }
    CLASSROOM_RECORDS.append(record)

    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total': total,
        'passed': passed,
        'module_stats': module_stats,
        'subject_stats': subject_stats,
        'details': details
    })

@app.route('/api/simulate_agent', methods=['POST'])
def simulate_agent():
    """Simulate Agentic AI ReAct execution for classroom demonstration"""
    payload = request.get_json() or {}
    template_id = payload.get('template_id')
    custom_scenario = payload.get('custom_scenario')
    
    templates = load_json_file('agent_templates.json')
    if isinstance(templates, list):
        matched = next((t for t in templates if t['id'] == template_id), None)
        if matched:
            return jsonify({
                'status': 'success',
                'agent_name': matched['name'],
                'target_software': matched.get('target_software', '商業軟體'),
                'trace': matched['simulated_trace']
            })
    
    # Dynamic trace generation for custom input
    scenario_text = custom_scenario or "自訂商業軟體自動化任務"
    custom_trace = [
        {"step": 1, "type": "thought", "content": f"【目標意圖分析】：收到業務指令「{scenario_text[:80]}...」，開始解析商業痛點、定義交付物格式與調用工具。"},
        {"step": 2, "type": "action", "tool": "parse_business_data", "input": {"scenario": scenario_text[:50]}, "status": "SUCCESS"},
        {"step": 3, "type": "observation", "result": "意圖辨識完成：需跨 Word、Excel、PPT 協同作業，抽取 3 項核心業務實體與 1 個財務指標。"},
        {"step": 4, "type": "thought", "content": "【工具呼叫與資料處理】：調用 Excel 清洗引擎進行 TRIM/CLEAN 空白清除，並以 XLOOKUP 補齊產品單價。"},
        {"step": 5, "type": "action", "tool": "excel_xlookup_and_pivot", "input": {"formula": "=XLOOKUP(A2, 主檔!A:A, 主檔!C:C)"}, "status": "SUCCESS"},
        {"step": 6, "type": "guardrail", "content": "【安全防護欄與防呆審核】：檢查公式是否鎖定絕對參照 $？數字是否均為實質數值？檢驗通過！"},
        {"step": 7, "type": "action", "tool": "word_generate_proposal", "input": {"format": "企劃書黃金五結構", "table": "三線表規範"}, "status": "SUCCESS"},
        {"step": 8, "type": "action", "tool": "ppt_scqa_and_speaker_notes", "input": {"structure": "SCQA 金字塔", "speech_time": "90 秒講稿"}, "status": "SUCCESS"},
        {"step": 9, "type": "human_in_the_loop", "content": "【Human-in-the-Loop 人機審批】：三合一套件已產出。請授權主管確認營運指標與預算金額無誤後點擊批准發布。"},
        {"step": 10, "type": "final_output", "content": "【自主執行圓滿完成】：已生成標準長報告 .docx、動態儀表板 .xlsx 與 10 頁提案簡報 .pptx，全流程自動存查完成。"}
    ]
    return jsonify({
        'status': 'success',
        'agent_name': '自訂商業流程 Agentic AI',
        'target_software': 'Word / Excel / PPT 一條搞定',
        'trace': custom_trace
    })

@app.route('/api/leaderboard')
def get_leaderboard():
    recent = list(reversed(CLASSROOM_RECORDS[-30:]))
    return jsonify({
        'count': len(CLASSROOM_RECORDS),
        'records': recent
    })

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    print("=" * 75)
    print("🚀 萬能科技大學【商業軟體應用 ✕ Agentic AI ✕ iPAS AI 應用規劃師】教學平台已啟動！")
    print(f"👨‍🏫 授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu)")
    print(f"🏫 授課班級：進企管四系 1 甲 (J501 企業經營模擬室)")
    print(f"💻 教師本機連線網址：http://localhost:{port}")
    print(f"📡 電腦教室學生連線網址：http://{local_ip}:{port}")
    print("=" * 75)
    app.run(host='0.0.0.0', port=port, debug=False)

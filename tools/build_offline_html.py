# -*- coding: utf-8 -*-
"""
Build standalone offline HTML files:
1. index.html (Root entrypoint for GitHub Pages / static hosting)
2. 平台首頁(單機離線直接點開).html
3. 商業軟體應用.html
Zero external server dependencies, works in any browser directly.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Read Data Files
def read_json(fname):
    with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8-sig') as f:
        return json.load(f)

curriculum = read_json("curriculum.json")
agent_templates = read_json("agent_templates.json")
ipas_guide = read_json("ipas_guide.json")
questions = read_json("questions.json")
sample_works = read_json("sample_works.json")

# Read CSS and JS
with open(os.path.join(STATIC_DIR, "css", "style.css"), 'r', encoding='utf-8') as f:
    css_content = f.read()

with open(os.path.join(STATIC_DIR, "js", "app.js"), 'r', encoding='utf-8') as f:
    js_content = f.read()

# Read HTML template
with open(os.path.join(TEMPLATES_DIR, "index.html"), 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace CSS link with inline style
html_content = html_content.replace(
    '<link rel="stylesheet" href="/static/css/style.css">',
    f'<style>\n{css_content}\n</style>'
)

# Prepare Offline Data JS Block
offline_data_script = f"""
<script>
window.OFFLINE_DATA = {{
  curriculum: {json.dumps(curriculum, ensure_ascii=False)},
  agentTemplates: {json.dumps(agent_templates, ensure_ascii=False)},
  ipasGuide: {json.dumps(ipas_guide, ensure_ascii=False)},
  questions: {json.dumps(questions, ensure_ascii=False)},
  sampleWorks: {json.dumps(sample_works, ensure_ascii=False)}
}};
</script>
"""

# Replace scripts:
# 1. Update slides_data.js to relative path "slides_data.js" so it loads when opened from local filesystem or GitHub Pages
# 2. Insert offline data script
# 3. Inline app.js
html_content = html_content.replace('<script src="/slides_data.js"></script>', '<script src="slides_data.js"></script>')
html_content = html_content.replace(
    '<script src="/static/js/app.js"></script>',
    f'{offline_data_script}\n<script>\n{js_content}\n</script>'
)

# Output targets
targets = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "商業軟體應用.html"),
    os.path.join(BASE_DIR, "平台首頁(單機離線直接點開).html")
]

for t in targets:
    with open(t, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated: {t} ({os.path.getsize(t):,} bytes)")


#!/usr/bin/env python3
"""
Leo Lee's Personal Site Generator
==================================
Generates:
  - FTP-style resource directory indexes
  - Resource overview page (card layout)
  - Blog posts from Markdown (with tag support)
  - Tag archive pages
  - RSS feed for blog posts
  - Sitemap.xml for SEO
  - 404 page
  - Dark/Light theme support on all pages
"""

import os
import json
import datetime
import markdown
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

# ── Configuration ──────────────────────────────────────────────────────────

BASE_URL = "https://lqy306.github.io"
SITE_TITLE = "Leo Lee"
SITE_DESCRIPTION = "一名来自中国福建厦门的学生，Arch Linux 忠实拥趸，热爱摄影与开源技术。"
AUTHOR = "Leo Lee"
LANG = "zh-CN"
NOW = datetime.datetime.now()
YEAR = NOW.year

# ── CSS ────────────────────────────────────────────────────────────────────

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&"
    "family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&"
    "family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');"
)

COMMON_CSS = FONT_IMPORT + """

/* ── Self-hosted fonts ── */

/* F1.8 (SIL OFL 1.1) — for logo / headings */
@font-face {
    font-family: 'F1.8';
    src: url('/fonts/F1.8-Regular.woff2') format('woff2'),
         url('/fonts/F1.8-Regular.otf') format('opentype');
    font-display: swap;
}

/* 寒蝉圆黑体 ChillRoundGothic Bold (SIL OFL 1.1) — for Chinese text */
@font-face {
    font-family: 'ChillRoundGothic';
    src: url('/fonts/ChillRoundGothic_Bold.woff2') format('woff2');
    font-display: swap;
}

/* ═══════════════════════════════════════════════
   Theme Variables
   ═══════════════════════════════════════════════ */
:root {
    --clr-black: #34322D;
    --clr-gray: #F8F8F8;
    --clr-white: #FFFFFF;
    --clr-accent: #1793d1;
    --clr-accent-light: rgba(23, 147, 209, 0.08);
    --clr-accent-glow: rgba(23, 147, 209, 0.2);
    --clr-border: rgba(52, 50, 45, 0.1);
    --clr-border-hover: rgba(52, 50, 45, 0.2);

    --body-bg: var(--clr-white);
    --surface-bg: var(--clr-gray);
    --nav-bg: rgba(255, 255, 255, 0.92);
    --card-bg: rgba(248, 248, 248, 0.55);
    --card-bg-hover: rgba(248, 248, 248, 1);

    --text-primary: var(--clr-black);
    --text-secondary: #666;
    --text-muted: #999;
    --text-on-accent: var(--clr-white);

    --footer-bg: var(--clr-black);
    --footer-text: var(--clr-gray);

    --code-bg: var(--clr-black);
    --code-text: var(--clr-accent);
    --pre-bg: var(--clr-black);
    --pre-text: var(--clr-gray);

    --post-bg: rgba(248, 248, 248, 0.55);
    --table-bg: rgba(248, 248, 248, 0.55);
    --breadcrumb-bg: var(--clr-accent-light);
}

[data-theme="dark"] {
    --clr-black: #E8E6E3;
    --clr-gray: #1b1b2f;
    --clr-white: #121212;
    --clr-accent: #4FC3F7;
    --clr-accent-light: rgba(79, 195, 247, 0.10);
    --clr-accent-glow: rgba(79, 195, 247, 0.20);
    --clr-border: rgba(232, 230, 227, 0.08);
    --clr-border-hover: rgba(232, 230, 227, 0.18);

    --body-bg: #121212;
    --surface-bg: #1b1b2f;
    --nav-bg: rgba(18, 18, 18, 0.92);
    --card-bg: rgba(27, 27, 47, 0.55);
    --card-bg-hover: rgba(27, 27, 47, 1);

    --text-primary: #E8E6E3;
    --text-secondary: #A0A0A0;
    --text-muted: #686868;
    --text-on-accent: #121212;

    --footer-bg: #0b0b17;
    --footer-text: #A0A0A0;

    --code-bg: #0d0d1a;
    --code-text: var(--clr-accent);
    --pre-bg: #0d0d1a;
    --pre-text: #E8E6E3;

    --post-bg: rgba(27, 27, 47, 0.55);
    --table-bg: rgba(27, 27, 47, 0.55);
    --breadcrumb-bg: var(--clr-accent-light);
}

/* ═══════════════════════════════════════════════
   Base
   ═══════════════════════════════════════════════ */
* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
    font-family: 'DM Sans', 'ChillRoundGothic', 'Noto Sans SC', sans-serif;
    background: var(--body-bg);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background 0.3s ease, color 0.3s ease;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    width: 100%;
}

/* ═══════════════════════════════════════════════
   Navigation
   ═══════════════════════════════════════════════ */
nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 1000;
    background: var(--nav-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--clr-border);
    transition: background 0.3s ease, border-color 0.3s ease;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.85rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-family: 'F1.8', 'Libre Baskerville', 'Noto Serif SC', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    text-decoration: none;
    letter-spacing: -0.02em;
    transition: color 0.3s ease;
}

.nav-links {
    display: flex;
    gap: 1.8rem;
    list-style: none;
    align-items: center;
}

.nav-links a {
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.3s ease;
    position: relative;
}

.nav-links a::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--clr-accent);
    transition: width 0.3s ease;
}

.nav-links a:hover { color: var(--clr-accent); }
.nav-links a:hover::after { width: 100%; }

/* Theme Toggle */
.theme-toggle {
    background: none;
    border: 2px solid var(--clr-border);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    color: var(--text-primary);
    transition: all 0.3s ease;
    padding: 0;
    line-height: 1;
}

.theme-toggle:hover {
    border-color: var(--clr-accent);
    color: var(--clr-accent);
    transform: rotate(15deg);
}

/* ═══════════════════════════════════════════════
   Main Content
   ═══════════════════════════════════════════════ */
main {
    flex: 1;
    margin-top: 80px;
}

h1 {
    font-family: 'Libre Baskerville', 'Noto Serif SC', serif;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    padding-bottom: 1rem;
    border-bottom: 3px solid var(--clr-accent);
    transition: color 0.3s ease, border-bottom 0.3s ease;
}

h2, h3, h4, h5, h6 {
    font-family: 'Libre Baskerville', 'Noto Serif SC', serif;
    color: var(--text-primary);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    transition: color 0.3s ease;
}

a {
    color: var(--clr-accent);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover { color: var(--text-primary); text-decoration: underline; }

/* Breadcrumb */
.breadcrumb {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--breadcrumb-bg);
    border-radius: 8px;
    border-left: 4px solid var(--clr-accent);
    transition: background 0.3s ease, border-left 0.3s ease;
}

.breadcrumb a { margin-right: 0.5rem; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: var(--table-bg);
    border-radius: 8px;
    overflow: hidden;
    transition: background 0.3s ease;
}

thead { background: var(--text-primary); color: var(--body-bg); transition: background 0.3s ease, color 0.3s ease; }

th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

td {
    padding: 1rem;
    border-bottom: 1px solid var(--clr-border);
    vertical-align: middle;
    transition: border-color 0.3s ease;
}

tbody tr:hover { background: var(--surface-bg); transition: background 0.3s ease; }
tbody tr:last-child td { border-bottom: none; }

/* Tags */
.tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    margin: 0.15rem;
    background: var(--breadcrumb-bg);
    color: var(--clr-accent);
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
    text-decoration: none;
}

.tag:hover {
    background: var(--clr-accent);
    color: var(--text-on-accent);
    text-decoration: none;
}

.table-info {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--breadcrumb-bg);
    border-radius: 8px;
    border-left: 4px solid var(--clr-accent);
    transition: background 0.3s ease, border-left 0.3s ease;
}

.table-info p { margin: 0; color: var(--text-secondary); transition: color 0.3s ease; }
.table-info .count { font-weight: 700; color: var(--clr-accent); }

/* Footer */
footer {
    margin-top: 4rem;
    padding: 2rem;
    background: var(--footer-bg);
    color: var(--footer-text);
    text-align: center;
    transition: background 0.3s ease, color 0.3s ease;
}

footer p { font-size: 0.9rem; margin: 0; }
footer a { color: var(--clr-accent); transition: color 0.3s ease; }
footer a:hover { color: var(--footer-text); }

/* Post Content */
.post-content {
    background: var(--post-bg);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid var(--clr-border);
    margin: 2rem 0;
    transition: background 0.3s ease, border-color 0.3s ease;
}

.post-content h1, .post-content h2, .post-content h3 {
    color: var(--text-primary);
    margin-top: 1.5em;
    border-bottom: 2px solid var(--clr-accent);
    padding-bottom: 0.5rem;
}

.post-content h1 { font-size: 2rem; }
.post-content h2 { font-size: 1.5rem; }
.post-content h3 { font-size: 1.2rem; }

.post-content img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.post-content code {
    background: var(--code-bg);
    color: var(--code-text);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.9em;
    transition: background 0.3s ease, color 0.3s ease;
}

.post-content pre {
    background: var(--pre-bg);
    color: var(--pre-text);
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1.5rem 0;
    border-left: 4px solid var(--clr-accent);
    transition: background 0.3s ease, color 0.3s ease, border-left 0.3s ease;
}

.post-content pre code {
    background: transparent;
    color: inherit;
    padding: 0;
}

.post-content blockquote {
    border-left: 4px solid var(--clr-accent);
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    font-style: italic;
    color: var(--text-secondary);
    transition: color 0.3s ease;
}

.post-content table { margin: 1.5rem 0; }
.post-content ul, .post-content ol { margin: 1.5rem 0 1.5rem 2rem; }
.post-content li { margin-bottom: 0.5rem; }

.post-meta {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
    transition: color 0.3s ease;
}

.post-tags { margin-bottom: 2rem; }

/* Resource cards */
.resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.resource-card {
    background: var(--card-bg);
    border: 1px solid var(--clr-border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    text-decoration: none;
    color: var(--text-primary);
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.resource-card:hover {
    border-color: var(--clr-accent);
    background: var(--card-bg-hover);
    transform: translateY(-4px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.08);
    text-decoration: none;
}

.resource-card .resource-icon {
    font-size: 2rem;
    color: var(--clr-accent);
}

.resource-card .resource-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.resource-card .resource-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    flex: 1;
}

.resource-card .resource-meta {
    font-size: 0.8rem;
    color: var(--text-muted);
    display: flex;
    gap: 1rem;
}

/* 404 Page */
.error-page {
    text-align: center;
    padding: 6rem 2rem;
}

.error-page h1 {
    font-size: 6rem;
    border: none;
    color: var(--clr-accent);
    margin-bottom: 0;
}

.error-page p {
    font-size: 1.2rem;
    color: var(--text-secondary);
    margin: 1.5rem 0;
    transition: color 0.3s ease;
}

/* Archive list */
.archive-list { list-style: none; }

.archive-list li {
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--clr-border);
    display: flex;
    gap: 1.5rem;
    align-items: baseline;
}

.archive-list li:last-child { border-bottom: none; }

.archive-date {
    font-size: 0.85rem;
    color: var(--text-muted);
    white-space: nowrap;
    min-width: 6em;
}

.archive-title {
    font-size: 1.05rem;
    font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
    .container { padding: 1rem; }
    h1 { font-size: 1.8rem; }
    .nav-links { display: none; }
    table { font-size: 0.9rem; }
    th, td { padding: 0.75rem; }
    .resource-grid { grid-template-columns: 1fr; }
    .archive-list li { flex-direction: column; gap: 0.3rem; }
    .archive-date { min-width: auto; }
    .error-page h1 { font-size: 4rem; }
}

@media (max-width: 480px) {
    .nav-container { padding: 0.85rem 1rem; }
    .logo { font-size: 1.2rem; }
}

/* Print */
@media print {
    nav { display: none; }
    main { margin-top: 0; }
}
"""

# ── Theme Toggle Script ───────────────────────────────────────────────────

THEME_SCRIPT = """
<script>
(function() {
    var toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    var icon = document.getElementById('theme-icon');
    var html = document.documentElement;
    var saved = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = saved || (prefersDark ? 'dark' : 'light');
    html.setAttribute('data-theme', theme);
    if (icon) icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    toggle.addEventListener('click', function() {
        var current = html.getAttribute('data-theme');
        var next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        if (icon) icon.className = next === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    });
})();
</script>
"""

# ── Helper Functions ──────────────────────────────────────────────────────

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.1f}{unit}{suffix}"
        b /= factor
    return f"{b:.1f}Y{suffix}"


def read_meta_json(dir_path):
    meta_path = os.path.join(dir_path, ".meta.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def parse_markdown_frontmatter(text):
    meta = {}
    rest = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            front = parts[1].strip()
            rest = parts[2].strip()
            for line in front.split("\n"):
                if ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "tags":
                        val = [t.strip().strip('"').strip("'") for t in val.strip("[]").split(",") if t.strip()]
                    elif key == "date":
                        try:
                            val = str(datetime.datetime.strptime(val, "%Y-%m-%d").date())
                        except ValueError:
                            pass
                    meta[key] = val
    return meta, rest


def make_breadcrumb_html(parts):
    crumbs = [f'<a href="{BASE_URL}">🏠 首页</a>']
    current = BASE_URL
    for name, rel_url in parts[:-1]:
        current = f"{current}/{rel_url}" if current != BASE_URL else f"{BASE_URL}/{rel_url}"
        crumbs.append(f' / <a href="{current}">{name}</a>')
    if parts:
        last_name = parts[-1][0]
        crumbs.append(f' / <strong>{last_name}</strong>')
    return "".join(crumbs)


def nav_html():
    return f"""
    <nav>
        <div class="nav-container">
            <a href="{BASE_URL}" class="logo">Leo Lee</a>
            <ul class="nav-links">
                <li><a href="{BASE_URL}">首页</a></li>
                <li><a href="{BASE_URL}/post/">博客</a></li>
                <li><a href="{BASE_URL}/resources/">资源</a></li>
                <li>
                    <button class="theme-toggle" id="theme-toggle" aria-label="切换主题">
                        <i class="fas fa-moon" id="theme-icon"></i>
                    </button>
                </li>
            </ul>
        </div>
    </nav>"""


def footer_html(custom_text=None):
    text = custom_text or "使用 Arch Linux 精神构建"
    return f"""
    <footer>
        <p>&copy; {YEAR} Leo Lee | {text} | Built with <a href="https://claude.ai/code">Claude Code</a></p>
        <p style="font-size:0.75rem;margin-top:0.5rem;opacity:0.7;">
            字体 <a href="/fonts/F1.8-Regular.otf">F1.8</a> 遵循 <a href="https://openfontlicense.org">SIL Open Font License, Version 1.1</a>
        </p>
    </footer>"""


def page_template(title, description, body_html, breadcrumb_parts=None, extra_headers=""):
    breadcrumb = ""
    if breadcrumb_parts:
        breadcrumb = f'<div class="breadcrumb">{make_breadcrumb_html(breadcrumb_parts)}</div>'
    return f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {SITE_TITLE}</title>
    <meta name="description" content="{xml_escape(description)}">
    {extra_headers}
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}
    <main>
        <div class="container">
            {breadcrumb}
            {body_html}
        </div>
    </main>
{footer_html()}
{THEME_SCRIPT}
</body>
</html>"""


# ── Resource Directory Generator ──────────────────────────────────────────

def generate_ftp_index(target_dir, root_repo_dir):
    rel_path = os.path.relpath(target_dir, root_repo_dir)
    display_path = "/" if rel_path == "." else "/" + rel_path
    meta = read_meta_json(target_dir)

    rows = []
    if rel_path != ".":
        rows.append(f'<tr><td><a href="../">📁 .. (上级目录)</a></td><td>-</td><td>-</td></tr>')

    skip_items = {'index.html', 'generate_index.py', '.github', '.git', 'fonts', '.meta.json'}
    items = [i for i in os.listdir(target_dir) if i not in skip_items]
    dirs = sorted([i for i in items if os.path.isdir(os.path.join(target_dir, i))])
    files = sorted([i for i in items if os.path.isfile(os.path.join(target_dir, i))])

    for d in dirs:
        d_path = os.path.join(target_dir, d)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(d_path)).strftime('%Y-%m-%d %H:%M:%S')
        sub_meta = read_meta_json(d_path)
        desc = f" — {sub_meta['description']}" if sub_meta and 'description' in sub_meta else ""
        rows.append(f'<tr><td><a href="{d}/">📁 {d}/</a>{desc}</td><td>{mtime}</td><td>-</td></tr>')

    for f in files:
        f_path = os.path.join(target_dir, f)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f_path)).strftime('%Y-%m-%d %H:%M:%S')
        size = get_size_format(os.path.getsize(f_path))
        rows.append(f'<tr><td><a href="{f}">📄 {f}</a></td><td>{mtime}</td><td>{size}</td></tr>')

    page_title = meta["name"] if meta and "name" in meta else f"Index of {display_path}"
    desc_html = f'<p>{xml_escape(meta["description"])}</p>' if meta and "description" in meta else ""
    count = len(rows)

    if rel_path == ".":
        bp = []
    else:
        bp = [("资源", "resources"), (page_title, rel_path)]

    body = f"""
            <h1>📂 {page_title}</h1>
            {desc_html}
            <div class="table-info">
                <p>此目录包含 <span class="count">{count}</span> 项。</p>
            </div>
            <table>
                <thead><tr><th>名称</th><th>修改时间</th><th>大小</th></tr></thead>
                <tbody>{"".join(rows)}</tbody>
            </table>"""

    html = page_template(page_title, desc_html or page_title, body, breadcrumb_parts=bp)
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def generate_resource_overview(root_repo_dir):
    res_dir = os.path.join(root_repo_dir, "resources")
    if not os.path.exists(res_dir):
        return

    categories = {}
    for d in sorted(os.listdir(res_dir)):
        d_path = os.path.join(res_dir, d)
        if not os.path.isdir(d_path) or d.startswith("."):
            continue
        meta = read_meta_json(d_path) or {}
        cat = meta.get("category", "其他")
        categories.setdefault(cat, []).append({
            "dir": d,
            "name": meta.get("name", d.replace("_", " ").replace("-", " ").title()),
            "description": meta.get("description", ""),
            "icon": meta.get("icon", "📁"),
            "size": sum(
                os.path.getsize(os.path.join(d_path, f))
                for f in os.listdir(d_path) if os.path.isfile(os.path.join(d_path, f))
            ),
        })

    total = sum(len(items) for items in categories.values())
    cat_parts = ""
    for cat_name, items in sorted(categories.items()):
        cards = ""
        for item in items:
            size_str = get_size_format(item["size"]) if item["size"] > 0 else ""
            cards += (
                f'<a href="{item["dir"]}/" class="resource-card">'
                f'<div class="resource-icon">{item["icon"]}</div>'
                f'<div class="resource-name">{item["name"]}</div>'
                f'<div class="resource-desc">{xml_escape(item["description"])}</div>'
                f'<div class="resource-meta">'
                + (f'<span>📦 {size_str}</span>' if size_str else "")
                + f'<span>📂 {item["dir"]}/</span></div></a>\n'
            )
        cat_parts += f'<h2>📁 {cat_name}</h2>\n<div class="resource-grid">\n{cards}</div>\n'

    body = f"""
            <h1>📦 资源分享</h1>
            <div class="table-info">
                <p>共有 <span class="count">{total}</span> 个资源分类。</p>
            </div>
            {cat_parts}"""

    html = page_template("资源分享", "资源分享页面", body, breadcrumb_parts=[("资源", "resources")])
    with open(os.path.join(res_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ── Blog Post Generator ────────────────────────────────────────────────────

def convert_md_to_html(md_path, html_path, title, tags=None, date_str=None):
    with open(md_path, "r", encoding="utf-8") as f:
        html_content = markdown.markdown(f.read(), extensions=["fenced_code", "tables", "toc"])

    mtime = date_str or datetime.datetime.fromtimestamp(os.path.getmtime(md_path)).strftime('%Y-%m-%d')
    slug = os.path.basename(os.path.dirname(html_path))

    tags_html = ""
    if tags:
        tag_links = "".join(f'<a href="{BASE_URL}/tags/{t}/" class="tag">#{t}</a> ' for t in tags)
        tags_html = f'<div class="post-tags">{tag_links}</div>'

    body = f"""
            <article>
                <h1>{title}</h1>
                <div class="post-meta">📅 发布于 {mtime}</div>
                {tags_html}
                <div class="post-content">
                    {html_content}
                </div>
            </article>"""

    html = page_template(
        title,
        f"{title} - 博客文章",
        body,
        breadcrumb_parts=[("博客", "post"), (title, slug)],
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)


def process_posts(post_dir, root_repo_dir):
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)

    all_tags = {}
    all_posts = []

    for d in sorted(os.listdir(post_dir)):
        d_path = os.path.join(post_dir, d)
        if not os.path.isdir(d_path):
            continue
        md_files = [f for f in os.listdir(d_path) if f.endswith(".md")]
        if not md_files:
            continue

        md_full_path = os.path.join(d_path, md_files[0])
        with open(md_full_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        front_meta, _ = parse_markdown_frontmatter(raw_text)
        title = front_meta.get("title", d.replace("_", " ").replace("-", " ").title())
        tags = front_meta.get("tags", [])
        post_date = front_meta.get("date")
        description = front_meta.get("description", "")

        convert_md_to_html(md_full_path, os.path.join(d_path, "index.html"), title, tags, post_date)

        mtime = post_date or datetime.datetime.fromtimestamp(os.path.getmtime(md_full_path)).strftime('%Y-%m-%d')
        post_info = {"title": title, "url": f"{d}/", "date": mtime, "tags": tags, "description": description}
        all_posts.append(post_info)

        for tag in tags:
            all_tags.setdefault(tag, []).append(post_info)

    all_posts.sort(key=lambda x: x["date"], reverse=True)
    generate_post_listing(post_dir, all_posts)
    generate_tag_pages(post_dir, all_tags, root_repo_dir)
    generate_rss(post_dir, all_posts)
    return all_posts, all_tags


def generate_post_listing(post_dir, all_posts):
    rows = ""
    for p in all_posts:
        tag_links = " ".join(f'<a href="{BASE_URL}/tags/{t}/" class="tag">#{t}</a>' for t in p["tags"])
        rows += f'<tr><td><a href="{p["url"]}">📝 {p["title"]}</a><br><span style="font-size:0.8rem;color:var(--text-muted);">{tag_links}</span></td><td>{p["date"]}</td></tr>\n'

    body = f"""
            <h1>📝 博客文章</h1>
            <div class="table-info">
                <p>共有 <span class="count">{len(all_posts)}</span> 篇文章。<a href="rss.xml">📡 RSS 订阅</a></p>
            </div>
            <table>
                <thead><tr><th>标题</th><th>发布日期</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>"""

    extra = '<link rel="alternate" type="application/rss+xml" title="RSS" href="https://lqy306.github.io/post/rss.xml">'
    html = page_template("博客", "个人博客", body, breadcrumb_parts=[("博客", "post")], extra_headers=extra)
    with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def generate_tag_pages(post_dir, all_tags, root_repo_dir):
    tags_dir = os.path.join(root_repo_dir, "tags")
    os.makedirs(tags_dir, exist_ok=True)

    tag_list_html = "".join(
        f'<a href="{tag}/" class="tag" style="font-size:1rem;padding:0.4rem 1rem;">#{tag} ({len(posts)})</a> '
        for tag, posts in sorted(all_tags.items())
    )

    for tag_name, posts in sorted(all_tags.items()):
        tag_dir = os.path.join(tags_dir, tag_name)
        os.makedirs(tag_dir, exist_ok=True)

        rows = "".join(
            f'<tr><td><a href="{BASE_URL}/post/{p["url"]}">📝 {p["title"]}</a></td><td>{p["date"]}</td></tr>\n'
            for p in sorted(posts, key=lambda x: x["date"], reverse=True)
        )

        body = f"""
                <h1>🏷️ #{tag_name}</h1>
                <div class="table-info"><p>共有 <span class="count">{len(posts)}</span> 篇带有此标签的文章。</p></div>
                <table><thead><tr><th>标题</th><th>发布日期</th></tr></thead><tbody>{rows}</tbody></table>"""

        html = page_template(f"标签: {tag_name}", f"标签 #{tag_name}", body,
                             breadcrumb_parts=[("标签", "tags"), (f"#{tag_name}", tag_name)])
        with open(os.path.join(tag_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

    body = f"""
            <h1>🏷️ 标签</h1>
            <div class="table-info"><p>共有 <span class="count">{len(all_tags)}</span> 个标签。</p></div>
            <div style="margin: 2rem 0; line-height: 2.5;">{tag_list_html}</div>"""

    html = page_template("标签", "博客标签索引", body, breadcrumb_parts=[("标签", "tags")])
    with open(os.path.join(tags_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def generate_rss(post_dir, all_posts):
    pub_date = NOW.strftime("%a, %d %b %Y %H:%M:%S +0800")
    items = ""
    for p in all_posts[:20]:
        dt = datetime.datetime.strptime(p["date"], "%Y-%m-%d")
        items += f"""        <item>
            <title>{xml_escape(p["title"])}</title>
            <link>{BASE_URL}/post/{p["url"]}</link>
            <guid>{BASE_URL}/post/{p["url"]}</guid>
            <pubDate>{dt.strftime("%a, %d %b %Y %H:%M:%S +0800")}</pubDate>
            <description>{xml_escape(p.get("description", p["title"]))}</description>
        </item>
"""

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{SITE_TITLE} 的博客</title>
        <link>{BASE_URL}/post/</link>
        <description>{SITE_DESCRIPTION}</description>
        <language>{LANG}</language>
        <lastBuildDate>{pub_date}</lastBuildDate>
        <atom:link href="{BASE_URL}/post/rss.xml" rel="self" type="application/rss+xml"/>
{items}    </channel>
</rss>"""
    with open(os.path.join(post_dir, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss)


# ── Sitemap & 404 ─────────────────────────────────────────────────────────

def generate_sitemap(root_repo_dir, all_posts):
    urls = [
        (BASE_URL + "/", "2026-06-05", "daily", "1.0"),
        (BASE_URL + "/resources/", "2026-06-05", "weekly", "0.8"),
        (BASE_URL + "/post/", "2026-06-05", "daily", "0.9"),
        (BASE_URL + "/tags/", "2026-06-05", "weekly", "0.5"),
    ]
    for p in all_posts:
        urls.append((f'{BASE_URL}/post/{p["url"]}', p["date"], "monthly", "0.7"))
    all_tag_set = set()
    for p in all_posts:
        all_tag_set.update(p["tags"])
    for tag in sorted(all_tag_set):
        urls.append((f'{BASE_URL}/tags/{tag}/', "2026-06-05", "weekly", "0.6"))

    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc, lastmod, changefreq, priority in urls:
        url_el = ET.SubElement(root, "url")
        ET.SubElement(url_el, "loc").text = loc
        ET.SubElement(url_el, "lastmod").text = lastmod
        ET.SubElement(url_el, "changefreq").text = changefreq
        ET.SubElement(url_el, "priority").text = priority
    ET.ElementTree(root).write(os.path.join(root_repo_dir, "sitemap.xml"), encoding="utf-8", xml_declaration=True)


def generate_404():
    body = """
            <div class="error-page">
                <h1>404</h1>
                <p>🌙 页面在星空中迷失了方向……</p>
                <p>你寻找的页面不存在，或已被移动到其他地方。</p>
                <p>
                    <a href=\"""" + BASE_URL + """/" class="tag" style="font-size:1rem;padding:0.6rem 1.5rem;">🏠 返回首页</a>
                    <a href=\"""" + BASE_URL + """/post/" class="tag" style="font-size:1rem;padding:0.6rem 1.5rem;">📝 浏览博客</a>
                </p>
            </div>"""
    html = page_template("404", "页面未找到", body)
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(html)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = os.getcwd()

    print("📁 生成资源目录索引...")
    res_dir = os.path.join(root, "resources")
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    for r, dirs, files in os.walk(res_dir):
        generate_ftp_index(r, root)
    generate_resource_overview(root)
    print("   ✓ 资源目录索引已生成")

    print("📝 处理博客文章...")
    all_posts, all_tags = process_posts(os.path.join(root, "post"), root)
    print(f"   ✓ 已处理 {len(all_posts)} 篇文章")
    print(f"   ✓ 已生成 {len(all_tags)} 个标签归档")

    print("🗺️  生成站点地图...")
    generate_sitemap(root, all_posts)
    print("   ✓ sitemap.xml 已生成")

    print("🚫 生成 404 页面...")
    generate_404()
    print("   ✓ 404.html 已生成")

    print("\n✅ 全部生成完成！")

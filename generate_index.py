#!/usr/bin/env python3
"""
Leo Lee's Personal Site Generator
==================================
Generates:
  - FTP-style resource directory indexes
  - Blog posts from Markdown (with tag support)
  - Tag archive pages
  - RSS feed for blog posts
  - Sitemap.xml for SEO
  - 404 page
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

FONT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

:root {
    --color-black: #34322D;
    --color-gray: #F8F8F8;
    --color-white: #FFFFFF;
    --color-accent: #1793d1;
    --color-accent-light: rgba(23, 147, 209, 0.08);
    --color-border: rgba(52, 50, 45, 0.1);
    --font-serif: 'Libre Baskerville', 'Noto Serif SC', serif;
    --font-sans: 'DM Sans', 'Noto Sans SC', sans-serif;
    --max-width: 1200px;
}
"""

COMMON_CSS = FONT_CSS + """
* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
    font-family: var(--font-sans);
    background: var(--color-white);
    color: var(--color-black);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.container {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 2rem;
    width: 100%;
}

/* Navigation */
nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 1000;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--color-border);
}

.nav-container {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0.8rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-black);
    text-decoration: none;
    letter-spacing: -0.02em;
}

.nav-links {
    display: flex;
    gap: 1.8rem;
    list-style: none;
    align-items: center;
}

.nav-links a {
    color: var(--color-black);
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
    background: var(--color-accent);
    transition: width 0.3s ease;
}

.nav-links a:hover { color: var(--color-accent); }
.nav-links a:hover::after { width: 100%; }

/* Main content */
main {
    flex: 1;
    margin-top: 80px;
}

h1 {
    font-family: var(--font-serif);
    font-size: 2.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem;
    color: var(--color-black);
    letter-spacing: -0.02em;
    padding-bottom: 1rem;
    border-bottom: 3px solid var(--color-accent);
}

h2, h3, h4, h5, h6 {
    font-family: var(--font-serif);
    color: var(--color-black);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

a {
    color: var(--color-accent);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover { color: var(--color-black); text-decoration: underline; }

/* Breadcrumb */
.breadcrumb {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--color-accent-light);
    border-radius: 8px;
    border-left: 4px solid var(--color-accent);
}

.breadcrumb a { margin-right: 0.5rem; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: rgba(248,248,248,0.6);
    border-radius: 8px;
    overflow: hidden;
}

thead { background: var(--color-black); color: var(--color-white); }

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
    border-bottom: 1px solid var(--color-border);
    vertical-align: middle;
}

tbody tr:hover { background: rgba(248,248,248,1); }
tbody tr:last-child td { border-bottom: none; }

/* Tags */
.tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    margin: 0.15rem;
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
    text-decoration: none;
}

.tag:hover {
    background: var(--color-accent);
    color: var(--color-white);
    text-decoration: none;
}

.table-info {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--color-accent-light);
    border-radius: 8px;
    border-left: 4px solid var(--color-accent);
}

.table-info p { margin: 0; color: #666; }
.table-info .count { font-weight: 700; color: var(--color-accent); }

/* Footer */
footer {
    margin-top: 4rem;
    padding: 2rem;
    background: var(--color-black);
    color: var(--color-gray);
    text-align: center;
}

footer p { font-size: 0.9rem; }
footer a { color: var(--color-accent); }
footer a:hover { color: var(--color-gray); }

/* Post content */
.post-content {
    background: rgba(248,248,248,0.6);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid var(--color-border);
    margin: 2rem 0;
}

.post-content h1, .post-content h2, .post-content h3 {
    color: var(--color-black);
    margin-top: 1.5em;
    border-bottom: 2px solid var(--color-accent);
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
    box-shadow: 0 10px 30px rgba(52,50,45,0.1);
}

.post-content code {
    background: var(--color-black);
    color: var(--color-accent);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.9em;
}

.post-content pre {
    background: var(--color-black);
    color: var(--color-gray);
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1.5rem 0;
    border-left: 4px solid var(--color-accent);
}

.post-content pre code {
    background: transparent;
    color: inherit;
    padding: 0;
}

.post-content blockquote {
    border-left: 4px solid var(--color-accent);
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    font-style: italic;
    color: #666;
}

.post-content table { margin: 1.5rem 0; }
.post-content ul, .post-content ol { margin: 1.5rem 0 1.5rem 2rem; }
.post-content li { margin-bottom: 0.5rem; }

.post-meta {
    font-size: 0.9rem;
    color: #999;
    margin-bottom: 1rem;
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
    background: rgba(248,248,248,0.6);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    text-decoration: none;
    color: var(--color-black);
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.resource-card:hover {
    border-color: var(--color-accent);
    background: rgba(248,248,248,1);
    transform: translateY(-4px);
    box-shadow: 0 15px 30px rgba(52,50,45,0.08);
    text-decoration: none;
}

.resource-card .resource-icon {
    font-size: 2rem;
    color: var(--color-accent);
}

.resource-card .resource-name {
    font-size: 1.2rem;
    font-weight: 700;
}

.resource-card .resource-desc {
    font-size: 0.9rem;
    color: #666;
    flex: 1;
}

.resource-card .resource-meta {
    font-size: 0.8rem;
    color: #999;
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
    color: var(--color-accent);
    margin-bottom: 0;
}

.error-page p {
    font-size: 1.2rem;
    color: #666;
    margin: 1.5rem 0;
}

/* Archive timeline */
.archive-list {
    list-style: none;
}

.archive-list li {
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--color-border);
    display: flex;
    gap: 1.5rem;
    align-items: baseline;
}

.archive-list li:last-child { border-bottom: none; }

.archive-date {
    font-size: 0.85rem;
    color: #999;
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
    .nav-container { padding: 0.8rem 1rem; }
    .logo { font-size: 1.2rem; }
}
"""

# ── Helper Functions ──────────────────────────────────────────────────────

def get_size_format(b, factor=1024, suffix="B"):
    """Convert bytes to human-readable format."""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.1f}{unit}{suffix}"
        b /= factor
    return f"{b:.1f}Y{suffix}"


def read_meta_json(dir_path):
    """Read .meta.json from a directory, return dict or None."""
    meta_path = os.path.join(dir_path, ".meta.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def parse_markdown_frontmatter(text):
    """Parse YAML-like frontmatter from markdown text. Returns (meta, content)."""
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
                        # Parse tags as [tag1, tag2, ...]
                        val = [t.strip().strip('"').strip("'") for t in val.strip("[]").split(",") if t.strip()]
                    elif key == "date":
                        try:
                            val = str(datetime.datetime.strptime(val, "%Y-%m-%d").date())
                        except ValueError:
                            pass
                    meta[key] = val
    return meta, rest


def make_breadcrumb_html(path_parts, base_url=BASE_URL):
    """Generate breadcrumb HTML from path parts list."""
    crumbs = [f'<a href="{base_url}">🏠 首页</a>']
    current = base_url
    for name, rel_url in path_parts:
        current = f"{current}/{rel_url}" if current != base_url else f"{base_url}/{rel_url}"
        crumbs.append(f' / <a href="{current}">{name}</a>')
    # Last one as bold
    if len(path_parts) > 0:
        last_name = path_parts[-1][0]
        crumbs[-1] = f' / <strong>{last_name}</strong>'
    return "".join(crumbs)


def nav_html(extra_links=None):
    """Generate navigation bar HTML with dropdown support."""
    links_html = """
        <li><a href="https://lqy306.github.io">首页</a></li>
        <li><a href="https://lqy306.github.io/#about">关于</a></li>
        <li><a href="https://lqy306.github.io/post/">博客</a></li>
        <li><a href="https://lqy306.github.io/resources/">资源</a></li>
"""
    if extra_links:
        for link in extra_links:
            links_html += f'        <li><a href="{link["url"]}">{link["label"]}</a></li>\n'
    return f"""
    <nav>
        <div class="nav-container">
            <a href="{BASE_URL}" class="logo">Leo Lee</a>
            <ul class="nav-links">
{links_html}
            </ul>
        </div>
    </nav>"""


def footer_html(custom_text=None):
    text = custom_text or "使用 Arch Linux 精神构建"
    return f"""
    <footer>
        <p>&copy; {YEAR} Leo Lee | {text}</p>
    </footer>"""


# ── Resource Directory Generator ──────────────────────────────────────────

def generate_ftp_index(target_dir, root_repo_dir):
    """Generate an enhanced FTP-style directory index with metadata support."""
    rel_path = os.path.relpath(target_dir, root_repo_dir)
    display_path = "/" if rel_path == "." else "/" + rel_path

    meta = read_meta_json(target_dir)

    rows = []
    if rel_path != ".":
        rows.append(f'<tr><td><a href="../">📁 .. (上级目录)</a></td><td>-</td><td>-</td></tr>')

    items = os.listdir(target_dir)
    skip_items = {'index.html', 'generate_index.py', '.github', '.git', 'fonts', '.meta.json'}
    items = [i for i in items if i not in skip_items]

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

    # Page title
    if meta and "name" in meta:
        page_title = meta["name"]
    else:
        page_title = f"Index of {display_path}"

    # Description
    description_html = ""
    if meta and "description" in meta:
        description_html = f'<p>{xml_escape(meta["description"])}</p>'

    count = len(rows)
    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | {SITE_TITLE}</title>
    <meta name="description" content="{xml_escape(meta['description']) if meta and 'description' in meta else page_title}">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("📂 " + display_path, rel_path)]) if rel_path == "." else make_breadcrumb_html([("资源", "resources"), (page_title, rel_path)])}
            </div>

            <h1>📂 {page_title}</h1>

            {description_html}

            <div class="table-info">
                <p>此目录包含 <span class="count">{count}</span> 项。</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>名称</th>
                        <th>修改时间</th>
                        <th>大小</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(template)


def generate_resource_overview(root_repo_dir):
    """Generate the main resources page with card-based layout."""
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
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "dir": d,
            "name": meta.get("name", d.replace("_", " ").replace("-", " ").title()),
            "description": meta.get("description", ""),
            "icon": meta.get("icon", "📁"),
            "size": sum(
                os.path.getsize(os.path.join(d_path, f))
                for f in os.listdir(d_path)
                if os.path.isfile(os.path.join(d_path, f))
            ),
        })

    total_items = sum(len(items) for items in categories.values())

    cat_html = ""
    for cat_name, items in sorted(categories.items()):
        card_html = ""
        for item in items:
            size_str = get_size_format(item["size"]) if item["size"] > 0 else ""
            card_html += f"""                <a href="{item["dir"]}/" class="resource-card">
                    <div class="resource-icon">{item["icon"]}</div>
                    <div class="resource-name">{item["name"]}</div>
                    <div class="resource-desc">{xml_escape(item["description"])}</div>
                    <div class="resource-meta">
                        {f'<span>📦 {size_str}</span>' if size_str else ''}
                        <span>📂 {item["dir"]}/</span>
                    </div>
                </a>
"""
        cat_html += f"""        <h2>📁 {cat_name}</h2>
        <div class="resource-grid">
{card_html}        </div>
"""

    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>资源分享 | {SITE_TITLE}</title>
    <meta name="description" content="Leo Lee 的资源分享页面 - 包含 LUT 工具、配置文件等">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("资源", "resources")])}
            </div>

            <h1>📦 资源分享</h1>

            <div class="table-info">
                <p>共有 <span class="count">{total_items}</span> 个资源分类。</p>
            </div>

{cat_html}        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open(os.path.join(res_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(template)


# ── Blog Post Generator ────────────────────────────────────────────────────

def convert_md_to_html(md_path, html_path, title, tags=None, date_str=None):
    """Convert Markdown to HTML post."""
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
        html_content = markdown.markdown(text, extensions=["fenced_code", "tables", "toc"])

    mtime = date_str or datetime.datetime.fromtimestamp(os.path.getmtime(md_path)).strftime('%Y-%m-%d')

    # Tags HTML
    tags_html = ""
    if tags:
        tag_links = "".join(f'<a href="{BASE_URL}/tags/{t}/" class="tag">#{t}</a> ' for t in tags)
        tags_html = f'<div class="post-tags">{tag_links}</div>'

    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {SITE_TITLE}</title>
    <meta name="description" content="{title} - {SITE_TITLE} 的博客文章">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("博客", "post"), (title, os.path.basename(os.path.dirname(html_path)))])}
            </div>

            <article>
                <h1>{title}</h1>
                <div class="post-meta">📅 发布于 {mtime}</div>
                {tags_html}
                <div class="post-content">
                    {html_content}
                </div>
            </article>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(template)


def process_posts(post_dir, root_repo_dir):
    """Process blog posts directory. Returns list of post metadata dicts."""
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

        md_file = md_files[0]
        md_full_path = os.path.join(d_path, md_file)
        html_full_path = os.path.join(d_path, "index.html")

        # Parse frontmatter
        with open(md_full_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        front_meta, _ = parse_markdown_frontmatter(raw_text)
        title = front_meta.get("title", d.replace("_", " ").replace("-", " ").title())
        tags = front_meta.get("tags", [])
        post_date = front_meta.get("date")
        description = front_meta.get("description", "")

        convert_md_to_html(md_full_path, html_full_path, title, tags, post_date)

        mtime = post_date or datetime.datetime.fromtimestamp(os.path.getmtime(md_full_path)).strftime('%Y-%m-%d')

        post_info = {
            "title": title,
            "url": f"{d}/",
            "date": mtime,
            "tags": tags,
            "description": description,
        }
        all_posts.append(post_info)

        for tag in tags:
            if tag not in all_tags:
                all_tags[tag] = []
            all_tags[tag].append(post_info)

    # Sort posts by date descending
    all_posts.sort(key=lambda x: x["date"], reverse=True)

    # Generate post listing page
    generate_post_listing(post_dir, all_posts)

    # Generate tag archive pages
    generate_tag_pages(post_dir, all_tags, root_repo_dir)

    # Generate RSS feed
    generate_rss(post_dir, all_posts)

    return all_posts, all_tags


def generate_post_listing(post_dir, all_posts):
    """Generate the blog post listing page."""
    count = len(all_posts)
    rows = ""
    for p in all_posts:
        tags_html = " ".join(f'<a href="{BASE_URL}/tags/{t}/" class="tag">#{t}</a>' for t in p["tags"])
        rows += f'<tr><td><a href="{p["url"]}">📝 {p["title"]}</a><br><span style="font-size:0.8rem;color:#999;">{tags_html}</span></td><td>{p["date"]}</td></tr>\n'

    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客 | {SITE_TITLE}</title>
    <meta name="description" content="{SITE_TITLE} 的个人博客 - 技术、摄影与生活">
    <link rel="alternate" type="application/rss+xml" title="RSS" href="{BASE_URL}/post/rss.xml">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("博客", "post")])}
            </div>

            <h1>📝 博客文章</h1>

            <div class="table-info">
                <p>共有 <span class="count">{count}</span> 篇文章。<a href="rss.xml">📡 RSS 订阅</a></p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>标题</th>
                        <th>发布日期</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(template)


def generate_tag_pages(post_dir, all_tags, root_repo_dir):
    """Generate tag archive pages (e.g., /tags/unix/)."""
    tags_dir = os.path.join(root_repo_dir, "tags")
    os.makedirs(tags_dir, exist_ok=True)

    tag_list_html = ""
    for tag_name in sorted(all_tags.keys()):
        posts = all_tags[tag_name]
        tag_list_html += f'<a href="{tag_name}/" class="tag" style="font-size:1rem;padding:0.4rem 1rem;">#{tag_name} ({len(posts)})</a> '

    for tag_name, posts in sorted(all_tags.items()):
        tag_dir = os.path.join(tags_dir, tag_name)
        os.makedirs(tag_dir, exist_ok=True)

        rows = ""
        for p in sorted(posts, key=lambda x: x["date"], reverse=True):
            rows += f'<tr><td><a href="{BASE_URL}/post/{p["url"]}">📝 {p["title"]}</a></td><td>{p["date"]}</td></tr>\n'

        count = len(posts)
        template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标签: {tag_name} | {SITE_TITLE}</title>
    <meta name="description" content="标签 #{tag_name} 下的文章">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("标签", "tags"), (f"#{tag_name}", tag_name)])}
            </div>

            <h1>🏷️ #{tag_name}</h1>

            <div class="table-info">
                <p>共有 <span class="count">{count}</span> 篇带有此标签的文章。</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>标题</th>
                        <th>发布日期</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
        with open(os.path.join(tag_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(template)

    # Generate tag overview page
    count = len(all_tags)
    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标签 | {SITE_TITLE}</title>
    <meta name="description" content="博客标签索引">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container">
            <div class="breadcrumb">
                {make_breadcrumb_html([("标签", "tags")])}
            </div>

            <h1>🏷️ 标签</h1>

            <div class="table-info">
                <p>共有 <span class="count">{count}</span> 个标签。</p>
            </div>

            <div style="margin: 2rem 0; line-height: 2.5;">
                {tag_list_html}
            </div>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open(os.path.join(tags_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(template)


def generate_rss(post_dir, all_posts):
    """Generate RSS 2.0 feed for blog posts."""
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{SITE_TITLE} 的博客</title>
        <link>{BASE_URL}/post/</link>
        <description>{SITE_DESCRIPTION}</description>
        <language>{LANG}</language>
        <lastBuildDate>{NOW.strftime("%a, %d %b %Y %H:%M:%S +0800")}</lastBuildDate>
        <atom:link href="{BASE_URL}/post/rss.xml" rel="self" type="application/rss+xml"/>
"""
    for p in all_posts[:20]:  # Last 20 posts
        pub_date = datetime.datetime.strptime(p["date"], "%Y-%m-%d")
        rss_xml += f"""        <item>
            <title>{xml_escape(p["title"])}</title>
            <link>{BASE_URL}/post/{p["url"]}</link>
            <guid>{BASE_URL}/post/{p["url"]}</guid>
            <pubDate>{pub_date.strftime("%a, %d %b %Y %H:%M:%S +0800")}</pubDate>
            <description>{xml_escape(p.get("description", p["title"]))}</description>
        </item>
"""
    rss_xml += """    </channel>
</rss>"""
    with open(os.path.join(post_dir, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss_xml)


# ── Sitemap Generator ──────────────────────────────────────────────────────

def generate_sitemap(root_repo_dir, all_posts):
    """Generate sitemap.xml for SEO."""
    urls = [
        (BASE_URL + "/", "2026-06-05", "daily", "1.0"),
        (BASE_URL + "/resources/", "2026-06-05", "weekly", "0.8"),
        (BASE_URL + "/post/", "2026-06-05", "daily", "0.9"),
        (BASE_URL + "/tags/", "2026-06-05", "weekly", "0.5"),
    ]

    for p in all_posts:
        urls.append((
            f'{BASE_URL}/post/{p["url"]}',
            p["date"],
            "monthly",
            "0.7",
        ))

    if all_posts:
        all_tags = set()
        for p in all_posts:
            all_tags.update(p["tags"])
        for tag in sorted(all_tags):
            urls.append((
                f'{BASE_URL}/tags/{tag}/',
                "2026-06-05",
                "weekly",
                "0.6",
            ))

    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc, lastmod, changefreq, priority in urls:
        url_el = ET.SubElement(root, "url")
        ET.SubElement(url_el, "loc").text = loc
        ET.SubElement(url_el, "lastmod").text = lastmod
        ET.SubElement(url_el, "changefreq").text = changefreq
        ET.SubElement(url_el, "priority").text = priority

    tree = ET.ElementTree(root)
    tree.write(os.path.join(root_repo_dir, "sitemap.xml"), encoding="utf-8", xml_declaration=True)


def generate_404():
    """Generate a custom 404 page."""
    template = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 | {SITE_TITLE}</title>
    <meta name="description" content="页面未找到">
    <style>{COMMON_CSS}</style>
</head>
<body>
{nav_html()}

    <main>
        <div class="container error-page">
            <h1>404</h1>
            <p>🌙 页面在星空中迷失了方向……</p>
            <p>你寻找的页面不存在，或已被移动到其他地方。</p>
            <p>
                <a href="{BASE_URL}/" class="tag" style="font-size:1rem;padding:0.6rem 1.5rem;">🏠 返回首页</a>
                <a href="{BASE_URL}/post/" class="tag" style="font-size:1rem;padding:0.6rem 1.5rem;">📝 浏览博客</a>
            </p>
        </div>
    </main>

{footer_html()}
</body>
</html>"""
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(template)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = os.getcwd()

    # 1. Generate resource indexes (FTP style)
    print("📁 生成资源目录索引...")
    res_dir = os.path.join(root, "resources")
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    for r, dirs, files in os.walk(res_dir):
        generate_ftp_index(r, root)
    # Resource overview page (card layout)
    generate_resource_overview(root)
    print("   ✓ 资源目录索引已生成")

    # 2. Generate blog posts
    print("📝 处理博客文章...")
    all_posts, all_tags = process_posts(os.path.join(root, "post"), root)
    print(f"   ✓ 已处理 {len(all_posts)} 篇文章")
    print(f"   ✓ 已生成 {len(all_tags)} 个标签归档")

    # 3. Generate sitemap
    print("🗺️  生成站点地图...")
    generate_sitemap(root, all_posts)
    print("   ✓ sitemap.xml 已生成")

    # 4. Generate 404 page
    print("🚫 生成 404 页面...")
    generate_404()
    print("   ✓ 404.html 已生成")

    print("\n✅ 全部生成完成！")

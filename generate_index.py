import os
import datetime
import markdown

# 基础配置
BASE_URL = "https://lqy306.github.io"

# Manus 风格的 CSS
MANUS_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Fragment+Mono&display=swap');

:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #141414;
    --bg-tertiary: #1c1c1c;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --text-tertiary: #666666;
    --accent: #d4a574;
    --border: rgba(255, 255, 255, 0.08);
}

body {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    padding: 40px 24px;
    line-height: 1.6;
    margin: 0;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
}

h1 {
    font-size: 28px;
    font-weight: 500;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
    color: var(--text-primary);
}

.path-info {
    font-family: 'Fragment Mono', monospace;
    font-size: 13px;
    color: var(--text-tertiary);
    margin-bottom: 32px;
}

a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s ease;
}

a:hover {
    color: var(--accent);
}

.nav-links {
    margin-bottom: 40px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}

.nav-links a {
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.table-container {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    text-align: left;
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
}

th {
    font-weight: 500;
    color: var(--text-tertiary);
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.05em;
    background: var(--bg-tertiary);
}

tr:last-child td {
    border-bottom: none;
}

tr:hover {
    background-color: var(--bg-tertiary);
}

.file-name {
    display: flex;
    align-items: center;
    gap: 12px;
}

.file-icon {
    font-size: 16px;
}

.footer {
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    font-size: 12px;
    color: var(--text-tertiary);
    text-align: center;
    font-family: 'Fragment Mono', monospace;
}
"""

POST_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Fragment+Mono&display=swap');

:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #141414;
    --bg-tertiary: #1c1c1c;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --text-tertiary: #666666;
    --accent: #d4a574;
    --border: rgba(255, 255, 255, 0.08);
}

body {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    padding: 40px 24px;
    line-height: 1.7;
    margin: 0;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

.nav-links {
    margin-bottom: 40px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}

.nav-links a {
    font-size: 14px;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.nav-links a:hover {
    color: var(--accent);
}

.post-content {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px;
}

.post-content h1 {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-top: 0;
    margin-bottom: 24px;
    color: var(--text-primary);
}

.post-content h2, .post-content h3 {
    color: var(--text-primary);
    margin-top: 32px;
    margin-bottom: 16px;
}

.post-content p {
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.post-content img {
    max-width: 100%;
    border-radius: 8px;
    margin: 24px 0;
}

.post-content code {
    background: var(--bg-tertiary);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Fragment Mono', monospace;
    font-size: 0.9em;
    color: var(--accent);
}

.post-content pre {
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 24px 0;
}

.post-content pre code {
    background: transparent;
    padding: 0;
    color: var(--text-secondary);
}

.post-content blockquote {
    border-left: 3px solid var(--accent);
    padding-left: 20px;
    font-style: italic;
    color: var(--text-tertiary);
    margin: 24px 0;
}

.footer {
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    font-size: 12px;
    color: var(--text-tertiary);
    text-align: center;
    font-family: 'Fragment Mono', monospace;
}
"""

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.1f}{unit}{suffix}"
        b /= factor
    return f"{b:.1f}Y{suffix}"

def generate_ftp_index(target_dir, root_repo_dir):
    rel_path = os.path.relpath(target_dir, root_repo_dir)
    display_path = "/" if rel_path == "." else "/" + rel_path
    
    rows = []
    # 添加 "Parent Directory"
    if rel_path != ".":
        rows.append(f'''<tr><td><a href="../"><span class="file-icon">📁</span> .. <span style="color: var(--text-tertiary); margin-left: 4px;">(Parent Directory)</span></a></td><td>-</td><td>-</td></tr>''')
    
    items = os.listdir(target_dir)
    # 过滤掉系统文件和 index.html
    items = [i for i in items if i not in ['index.html', 'generate_index.py', '.github', '.git', 'fonts']]
    
    # 先文件夹后文件
    dirs = sorted([i for i in items if os.path.isdir(os.path.join(target_dir, i))])
    files = sorted([i for i in items if os.path.isfile(os.path.join(target_dir, i))])
    
    for d in dirs:
        d_path = os.path.join(target_dir, d)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(d_path)).strftime('%Y-%m-%d %H:%M:%S')
        rows.append(f'<tr><td><a href="{d}/"><span class="file-icon">📁</span> {d}/</a></td><td>{mtime}</td><td>-</td></tr>')
        
    for f in files:
        f_path = os.path.join(target_dir, f)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f_path)).strftime('%Y-%m-%d %H:%M:%S')
        size = get_size_format(os.path.getsize(f_path))
        rows.append(f'<tr><td><a href="{f}"><span class="file-icon">📄</span> {f}</a></td><td>{mtime}</td><td>{size}</td></tr>')

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of {display_path}</title>
    <style>{MANUS_STYLE}</style>
</head>
<body>
    <div class="container">
        <div class="nav-links">
            <a href="{BASE_URL}">🏠 Back to Home</a>
        </div>
        <h1>Index of {display_path}</h1>
        <p class="path-info">FTP-style Archive</p>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Last Modified</th>
                        <th>Size</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        <div class="footer">
            Generated by Auto-FTP Script | Arch Linux Spirit
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(target_dir, "index.html"), "w", encoding='utf-8') as f_out:
        f_out.write(template)

def convert_md_to_html(md_path, html_path, title):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        html_content = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc'])
        
    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Leo Lee's Blog</title>
    <style>{POST_STYLE}</style>
</head>
<body>
    <div class="container">
        <div class="nav-links">
            <a href="{BASE_URL}">🏠 Home</a> &nbsp;|&nbsp; <a href="../">📂 Back to Posts</a>
        </div>
        <article class="post-content">
            {html_content}
        </article>
        <div class="footer">
            © 2026 Leo Lee | Built with Arch Linux spirit
        </div>
    </div>
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(template)

def process_posts(post_dir):
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
        
    post_list = []
    # 遍历 post 下的每个文件夹
    for d in os.listdir(post_dir):
        d_path = os.path.join(post_dir, d)
        if os.path.isdir(d_path):
            # 查找 md 文件
            md_files = [f for f in os.listdir(d_path) if f.endswith('.md')]
            if md_files:
                md_file = md_files[0]
                md_full_path = os.path.join(d_path, md_file)
                html_full_path = os.path.join(d_path, "index.html")
                title = d.replace('_', ' ').replace('-', ' ').title()
                convert_md_to_html(md_full_path, html_full_path, title)
                
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(md_full_path)).strftime('%Y-%m-%d')
                post_list.append({'title': title, 'url': f"{d}/", 'date': mtime})
    
    # 生成 post 目录的 index.html (列表页)
    post_list.sort(key=lambda x: x['date'], reverse=True)
    rows = "".join([f'<tr><td><a href="{p["url"]}"><span class="file-icon">📝</span> {p["title"]}</a></td><td>{p["date"]}</td><td>-</td></tr>' for p in post_list])
    
    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts | Leo Lee</title>
    <style>{MANUS_STYLE}</style>
</head>
<body>
    <div class="container">
        <div class="nav-links">
            <a href="{BASE_URL}">🏠 Back to Home</a>
        </div>
        <h1>Blog Posts</h1>
        <p class="path-info">Writing & Thoughts</p>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Date</th>
                        <th>Size</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        <div class="footer">
            Generated by Auto-Blog Script | Arch Linux Spirit
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(post_dir, "index.html"), "w", encoding='utf-8') as f_out:
        f_out.write(template)

if __name__ == "__main__":
    root = os.getcwd()
    
    # 1. 处理资源目录 (FTP 风格)
    res_dir = os.path.join(root, "resources")
    if not os.path.exists(res_dir): os.makedirs(res_dir)
    for r, dirs, files in os.walk(res_dir):
        generate_ftp_index(r, root)
        
    # 2. 处理贴子目录 (Markdown 转换)
    process_posts(os.path.join(root, "post"))


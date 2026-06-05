import os
import datetime
import markdown

# 基础配置
BASE_URL = "https://lqy306.github.io"

# Manus 风格的字体和颜色配置
FONT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

:root {
    --color-black: #34322D;
    --color-gray: #F8F8F8;
    --color-white: #FFFFFF;
    --color-accent: #1793d1;
    --font-serif: 'Libre Baskerville', 'Noto Serif SC', serif;
    --font-sans: 'DM Sans', 'Noto Sans SC', sans-serif;
}
"""

COMMON_STYLE = f"""
{FONT_CSS}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: var(--font-sans);
    background-color: var(--color-white);
    color: var(--color-black);
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}}

/* Navigation */
nav {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(52, 50, 45, 0.1);
}}

.nav-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-black);
    text-decoration: none;
    letter-spacing: -0.02em;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--color-black);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--color-accent);
}}

/* Main Content */
main {{
    margin-top: 80px;
}}

h1 {{
    font-family: var(--font-serif);
    font-size: 2.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    color: var(--color-black);
    letter-spacing: -0.02em;
    padding-bottom: 1rem;
    border-bottom: 3px solid var(--color-accent);
}}

h2, h3, h4, h5, h6 {{
    font-family: var(--font-serif);
    color: var(--color-black);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}}

a {{
    color: var(--color-accent);
    text-decoration: none;
    transition: color 0.3s ease;
}}

a:hover {{
    color: var(--color-black);
    text-decoration: underline;
}}

/* Table Styles */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: rgba(248, 248, 248, 0.6);
    border-radius: 8px;
    overflow: hidden;
}}

thead {{
    background: var(--color-black);
    color: var(--color-white);
}}

th {{
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

td {{
    padding: 1rem;
    border-bottom: 1px solid rgba(52, 50, 45, 0.1);
}}

tbody tr:hover {{
    background: rgba(248, 248, 248, 1);
}}

tbody tr:last-child td {{
    border-bottom: none;
}}

/* Footer */
footer {{
    margin-top: 4rem;
    padding: 2rem;
    background: var(--color-black);
    color: var(--color-gray);
    text-align: center;
    border-top: 1px solid rgba(248, 248, 248, 0.1);
}}

footer p {{
    font-size: 0.9rem;
    margin: 0;
}}

footer a {{
    color: var(--color-accent);
}}

footer a:hover {{
    color: var(--color-gray);
}}

/* Breadcrumb Navigation */
.breadcrumb {{
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(248, 248, 248, 0.6);
    border-radius: 8px;
    border-left: 4px solid var(--color-accent);
}}

.breadcrumb a {{
    margin-right: 0.5rem;
}}

/* Responsive */
@media (max-width: 768px) {{
    .container {{
        padding: 1rem;
    }}

    h1 {{
        font-size: 1.8rem;
    }}

    .nav-links {{
        display: none;
    }}

    table {{
        font-size: 0.9rem;
    }}

    th, td {{
        padding: 0.75rem;
    }}
}}
"""

FTP_STYLE = COMMON_STYLE + """
.table-info {{
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(23, 147, 209, 0.05);
    border-radius: 8px;
    border-left: 4px solid var(--color-accent);
}}

.table-info p {{
    margin: 0;
    color: #666;
}}

.icon {{
    margin-right: 0.5rem;
    color: var(--color-accent);
}}
"""

POST_STYLE = COMMON_STYLE + """
.post-content {{
    background: rgba(248, 248, 248, 0.6);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid rgba(52, 50, 45, 0.1);
    margin: 2rem 0;
}}

.post-content h1, .post-content h2, .post-content h3 {{
    color: var(--color-black);
    margin-top: 1.5em;
    border-bottom: 2px solid var(--color-accent);
    padding-bottom: 0.5rem;
}}

.post-content h1 {{
    font-size: 2rem;
}}

.post-content h2 {{
    font-size: 1.5rem;
}}

.post-content h3 {{
    font-size: 1.2rem;
}}

.post-content img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(52, 50, 45, 0.1);
}}

.post-content code {{
    background: var(--color-black);
    color: var(--color-accent);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.9em;
}}

.post-content pre {{
    background: var(--color-black);
    color: var(--color-gray);
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1.5rem 0;
    border-left: 4px solid var(--color-accent);
}}

.post-content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
}}

.post-content blockquote {{
    border-left: 4px solid var(--color-accent);
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    font-style: italic;
    color: #666;
}}

.post-content table {{
    margin: 1.5rem 0;
}}

.post-content ul, .post-content ol {{
    margin: 1.5rem 0 1.5rem 2rem;
}}

.post-content li {{
    margin-bottom: 0.5rem;
}}

.post-meta {{
    font-size: 0.9rem;
    color: #999;
    margin-bottom: 2rem;
}}
"""

def get_size_format(b, factor=1024, suffix="B"):
    """将字节转换为可读格式"""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.1f}{unit}{suffix}"
        b /= factor
    return f"{b:.1f}Y{suffix}"

def generate_ftp_index(target_dir, root_repo_dir):
    """生成 FTP 风格的目录索引"""
    rel_path = os.path.relpath(target_dir, root_repo_dir)
    display_path = "/" if rel_path == "." else "/" + rel_path
    
    rows = []
    # 添加 "Parent Directory"
    if rel_path != ".":
        rows.append('<tr><td><a href="../">📁 .. (上级目录)</a></td><td>-</td><td>-</td></tr>')
    
    items = os.listdir(target_dir)
    # 过滤掉系统文件和 index.html
    items = [i for i in items if i not in ['index.html', 'generate_index.py', '.github', '.git', 'fonts']]
    
    # 先文件夹后文件
    dirs = sorted([i for i in items if os.path.isdir(os.path.join(target_dir, i))])
    files = sorted([i for i in items if os.path.isfile(os.path.join(target_dir, i))])
    
    for d in dirs:
        d_path = os.path.join(target_dir, d)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(d_path)).strftime('%Y-%m-%d %H:%M:%S')
        rows.append(f'<tr><td><a href="{d}/">📁 {d}/</a></td><td>{mtime}</td><td>-</td></tr>')
        
    for f in files:
        f_path = os.path.join(target_dir, f)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f_path)).strftime('%Y-%m-%d %H:%M:%S')
        size = get_size_format(os.path.getsize(f_path))
        rows.append(f'<tr><td><a href="{f}">📄 {f}</a></td><td>{mtime}</td><td>{size}</td></tr>')

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of {display_path}</title>
    <style>{FTP_STYLE}</style>
</head>
<body>
    <nav>
        <div class="nav-container">
            <a href="{BASE_URL}" class="logo">Leo Lee</a>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="breadcrumb">
                <a href="{BASE_URL}">🏠 首页</a> / <strong>{display_path}</strong>
            </div>

            <h1>📂 {display_path}</h1>

            <div class="table-info">
                <p>此目录包含 {{len(rows)}} 项。</p>
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

    <footer>
        <p>&copy; 2026 Leo Lee | 由 Manus 风格的自动生成脚本生成</p>
    </footer>
</body>
</html>
"""
    with open(os.path.join(target_dir, "index.html"), "w", encoding='utf-8') as f_out:
        f_out.write(template)

def convert_md_to_html(md_path, html_path, title):
    """将 Markdown 转换为 HTML"""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        html_content = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc'])
    
    # 获取文件修改时间
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(md_path)).strftime('%Y-%m-%d')
        
    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Leo Lee 的博客</title>
    <style>{POST_STYLE}</style>
</head>
<body>
    <nav>
        <div class="nav-container">
            <a href="{BASE_URL}" class="logo">Leo Lee</a>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="breadcrumb">
                <a href="{BASE_URL}">🏠 首页</a> / <a href="../">📂 博客</a> / <strong>{title}</strong>
            </div>

            <article>
                <h1>{title}</h1>
                <div class="post-meta">📅 发布于 {mtime}</div>
                <div class="post-content">
                    {html_content}
                </div>
            </article>
        </div>
    </main>

    <footer>
        <p>&copy; 2026 Leo Lee | 使用 Arch Linux 精神构建</p>
    </footer>
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(template)

def process_posts(post_dir):
    """处理博客文章目录"""
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
    rows = "".join([f'<tr><td><a href="{p["url"]}">📝 {p["title"]}</a></td><td>{p["date"]}</td></tr>' for p in post_list])
    
    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客 | Leo Lee</title>
    <style>{FTP_STYLE}</style>
</head>
<body>
    <nav>
        <div class="nav-container">
            <a href="{BASE_URL}" class="logo">Leo Lee</a>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="breadcrumb">
                <a href="{BASE_URL}">🏠 首页</a> / <strong>📂 博客</strong>
            </div>

            <h1>📝 博客文章</h1>

            <div class="table-info">
                <p>共有 {{len(post_list)}} 篇文章。</p>
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

    <footer>
        <p>&copy; 2026 Leo Lee | 由自动博客生成脚本生成</p>
    </footer>
</body>
</html>
"""
    with open(os.path.join(post_dir, "index.html"), "w", encoding='utf-8') as f_out:
        f_out.write(template)

if __name__ == "__main__":
    root = os.getcwd()
    
    # 1. 处理资源目录 (FTP 风格)
    res_dir = os.path.join(root, "resources")
    if not os.path.exists(res_dir): 
        os.makedirs(res_dir)
    for r, dirs, files in os.walk(res_dir):
        generate_ftp_index(r, root)
        
    # 2. 处理贴子目录 (Markdown 转换)
    process_posts(os.path.join(root, "post"))
    
    print("✓ 网页生成完成！")
    print("✓ 资源目录已更新")
    print("✓ 博客文章已处理")

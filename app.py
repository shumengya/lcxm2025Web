#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵创新媒实验室招新官网网站 - Python Flask版本
"""

import os
import re
from urllib.parse import unquote
from flask import Flask, render_template, send_from_directory, abort, request
from markdown import markdown
from markdown.extensions import codehilite, toc, tables, fenced_code, nl2br, sane_lists, smarty, admonition
import yaml
from pathlib import Path
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lcxm-docs-2024'

# 配置目录
DOCS_DIR = Path(__file__).parent
STATIC_DIR = DOCS_DIR / '.vuepress' / 'public'
IMG_DIR = DOCS_DIR / '.vuepress' / 'public' / 'img'

# 网站配置（从原VuePress配置转换）
SITE_CONFIG = {
    'title': '灵创新媒', 
    'description': '灵创新媒 数字媒体技术实验室',
    'lang': 'zh-CN',
    'navbar': [
        {'text': '指引', 'link': '/guide2023/'},
        {
            'text': '公告',
            'children': [
                {'text': '关于经费', 'link': '/notice/fund'}
            ]
        },
        {'text': '新闻与文章', 'link': '/essay/'},
        {'text': '数媒WIKI', 'link': '/wiki/wiki2023'},
        {
            'text': '关于',
            'children': [
                {'text': '友情链接', 'link': '/about/friends'},
                {'text': '参与贡献', 'link': '/about/contribution'}
            ]
        }
    ],
    'sidebar': {
        '/guide2023/': [
            '如何加入实验室',
            "灵创实验室问与答",
            '灵创新媒实验室简介',
            '灵创新媒实验室组成', 
            '灵创新媒实验室就业方向',

        ],
        '/essay/': [
            '灵创新媒实验室开展互联网产业就业实践',
            '云极客团队携手灵创新媒实验室：远程办公成果揭示科技的力量',
            'ZB中一些需要注意的地方',
            '建模学习问题'
        ]
    }
}

def read_markdown_file(file_path):
    """读取Markdown文件并解析frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析frontmatter
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    content = parts[2].strip()
                except yaml.YAMLError:
                    pass
        
        # 转换Markdown为HTML
        html_content = markdown(
            content,
            extensions=[
                'codehilite',
                'toc',
                'tables',
                'fenced_code',
                'attr_list',
                'nl2br',
                'sane_lists',
                'smarty',
                'admonition',
                'def_list',
                'abbr',
                'footnotes'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True,
                    'linenums': False
                },
                'toc': {
                    'permalink': True,
                    'permalink_class': 'header-anchor',
                    'permalink_title': '永久链接到此标题'
                },
                'smarty': {
                    'smart_angled_quotes': True,
                    'smart_dashes': True,
                    'smart_ellipses': True,
                    'smart_quotes': True
                }
            }
        )
        
        return frontmatter, html_content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}, f"<p>Error loading content: {e}</p>"

def get_page_title(frontmatter, file_path):
    """获取页面标题"""
    if 'title' in frontmatter:
        return frontmatter['title']
    
    # 从文件名推断标题
    filename = Path(file_path).stem
    if filename == 'readme' or filename == 'index':
        return SITE_CONFIG['title']
    return filename.replace('-', ' ').replace('_', ' ').title()

def parse_member_list():
    """解析灵创名单文件"""
    members = []
    founder_qq = "1213014433"  # 创始人QQ号
    founder_member = None
    
    try:
        with open(DOCS_DIR / '灵创名单.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 2 and parts[0] and parts[1]:
                        qq_number = parts[0]
                        nickname = parts[1]
                        
                        member = {
                            'qq': qq_number,
                            'nickname': nickname,
                            'avatar_url': f"http://q1.qlogo.cn/g?b=qq&nk={qq_number}&s=100"
                        }
                        
                        if qq_number == founder_qq:
                            founder_member = member
                        else:
                            members.append(member)
    except Exception as e:
        print(f"Error reading member list: {e}")
    
    # 将创始人放在第一位
    if founder_member:
        members.insert(0, founder_member)
    
    return members

@app.route('/hall-of-fame')
def hall_of_fame():
    """灵创英灵殿页面"""
    members = parse_member_list()
    return render_template('hall_of_fame.html',
                         config=SITE_CONFIG,
                         title='灵创英灵殿',
                         members=members)

@app.route('/')
def index():
    """首页"""
    index_file = DOCS_DIR / 'index.md'
    if index_file.exists():
        frontmatter, content = read_markdown_file(index_file)
        
        # 处理首页特殊配置
        if frontmatter.get('home'):
            return render_template('home.html', 
                                 config=SITE_CONFIG,
                                 frontmatter=frontmatter,
                                 content=content)
    
    return render_template('page.html',
                         config=SITE_CONFIG,
                         title=SITE_CONFIG['title'],
                         content=content or '<h1>欢迎来到灵创新媒</h1>')

@app.route('/<path:path>')
def serve_page(path):
    """服务Markdown页面"""
    # URL解码，处理中文文件名
    path = unquote(path)
    
    # 移除.html和.md后缀
    if path.endswith('.html'):
        path = path[:-5]
    elif path.endswith('.md'):
        path = path[:-3]
    
    # 尝试不同的文件路径
    possible_paths = [
        DOCS_DIR / f"{path}.md",
        DOCS_DIR / path / "readme.md",
        DOCS_DIR / path / "index.md"
    ]
    
    for file_path in possible_paths:
        if file_path.exists():
            frontmatter, content = read_markdown_file(file_path)
            title = get_page_title(frontmatter, file_path)
            
            # 获取侧边栏配置
            sidebar_key = f"/{path.split('/')[0]}/" if '/' in path else '/'
            sidebar = SITE_CONFIG['sidebar'].get(sidebar_key, [])
            
            return render_template('page.html',
                                 config=SITE_CONFIG,
                                 title=title,
                                 content=content,
                                 sidebar=sidebar,
                                 current_path=f"/{path}")
    
    abort(404)

@app.route('/img/<path:filename>')
def serve_image(filename):
    """服务图片文件"""
    return send_from_directory(IMG_DIR, filename)

@app.route('/video/<path:filename>')
def serve_video(filename):
    """服务视频文件"""
    video_dir = STATIC_DIR / 'video'
    return send_from_directory(video_dir, filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """服务静态资源"""
    return send_from_directory(STATIC_DIR, filename)

@app.errorhandler(404)
def not_found(error):
    """404错误页面"""
    return render_template('404.html', config=SITE_CONFIG), 404

if __name__ == '__main__':
    # 确保模板目录存在
    templates_dir = DOCS_DIR / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    
    app.run(host='0.0.0.0', port=5001, debug=True)
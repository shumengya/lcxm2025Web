# 灵创新媒实验室文档网站 - Python 版本

这是灵创新媒实验室文档网站的 Python Flask 版本，用于替代原有的 Node.js VuePress 部署方案。

## 项目特点

- ✅ **Python 3.13.2 兼容** - 使用最新的 Python 版本
- ✅ **Flask 框架** - 轻量级、高性能的 Web 框架
- ✅ **Markdown 支持** - 完整支持 Markdown 文档渲染
- ✅ **响应式设计** - 基于 Bootstrap 5 的现代化界面
- ✅ **代码高亮** - 使用 Prism.js 提供语法高亮
- ✅ **导航系统** - 自动生成导航栏和侧边栏
- ✅ **搜索友好** - SEO 优化的 HTML 结构
- ✅ **易于部署** - 简单的 Python 环境即可运行

## 系统要求

- Python 3.8+ (推荐 Python 3.13.2)
- pip (Python 包管理器)
- 现代浏览器支持

## 快速开始

### 1. 环境准备

确保已安装 Python 3.13.2：

```bash
python --version
# 应该显示 Python 3.13.2 或更高版本
```

### 2. 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt
```

### 3. 启动服务器

#### 方式一：使用启动脚本（推荐）

```bash
# 基本启动
python run.py

# 自定义端口
python run.py --port 8080

# 启用调试模式
python run.py --debug

# 自定义主机和端口
python run.py --host 127.0.0.1 --port 3000
```

#### 方式二：直接运行 Flask 应用

```bash
python app.py
```

### 4. 访问网站

打开浏览器访问：http://localhost:5000

## 项目结构

```
docs/
├── app.py                 # Flask 主应用
├── run.py                 # 启动脚本
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── templates/            # HTML 模板
│   ├── base.html         # 基础模板
│   ├── home.html         # 首页模板
│   ├── page.html         # 文档页面模板
│   └── 404.html          # 404 错误页面
├── index.md              # 网站首页
├── guide2023/            # 指引文档
├── essay/                # 新闻文章
├── wiki/                 # WIKI 文档
├── notice/               # 公告
├── about/                # 关于页面
├── history/              # 历史文档
├── extra/                # 额外内容
└── .vuepress/            # 原 VuePress 配置（保留静态资源）
    └── public/           # 静态文件（图片、图标等）
```

## 功能特性

### 1. Markdown 渲染

- 支持标准 Markdown 语法
- 代码块语法高亮
- 表格支持
- 目录自动生成
- 数学公式支持（可扩展）

### 2. 导航系统

- 自动生成顶部导航栏
- 智能侧边栏（基于目录结构）
- 面包屑导航
- 上一页/下一页导航

### 3. 响应式设计

- 移动端友好
- 自适应布局
- 现代化 UI 设计
- 暗色模式支持（可扩展）

### 4. 性能优化

- 静态资源 CDN 加速
- 图片懒加载（可扩展）
- 缓存优化
- 压缩输出

## 配置说明

### 网站配置

在 `app.py` 中的 `SITE_CONFIG` 字典可以配置：

- 网站标题和描述
- 导航栏菜单
- 侧边栏结构
- 语言设置

### 自定义样式

可以通过修改 `templates/base.html` 中的 CSS 来自定义网站样式。

### 添加新页面

1. 在相应目录下创建 `.md` 文件
2. 添加 frontmatter（可选）
3. 编写 Markdown 内容
4. 更新导航配置（如需要）

## 部署指南

### 开发环境

```bash
# 启用调试模式
python run.py --debug
```

### 生产环境

#### 使用 Gunicorn（推荐）

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 使用 uWSGI

```bash
# 安装 uWSGI
pip install uwsgi

# 启动服务
uwsgi --http :5000 --wsgi-file app.py --callable app
```

#### Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.13.2-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /path/to/your/static/files;
        expires 1y;
    }
}
```

## 从 VuePress 迁移

本项目已经完成了从 VuePress 到 Python Flask 的迁移：

1. ✅ **配置转换** - VuePress 配置已转换为 Python 配置
2. ✅ **模板适配** - 保持了原有的页面结构和样式
3. ✅ **静态资源** - 复用了原有的图片和静态文件
4. ✅ **路由映射** - 保持了原有的 URL 结构
5. ✅ **功能对等** - 实现了 VuePress 的主要功能

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 使用不同端口
   python run.py --port 8080
   ```

2. **依赖安装失败**
   ```bash
   # 升级 pip
   python -m pip install --upgrade pip
   
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **模板文件未找到**
   ```bash
   # 确保在正确的目录下运行
   cd /path/to/docs
   python run.py
   ```

4. **静态文件 404**
   - 检查 `.vuepress/public/` 目录是否存在
   - 确保图片路径正确

### 日志调试

启用调试模式查看详细日志：

```bash
python run.py --debug
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用与原项目相同的许可证。

## 联系方式

- 实验室官网：[灵创新媒实验室](https://lcxm.site)
- 问题反馈：请在 GitHub 上提交 Issue

---

**灵创新媒实验室** | Copyright © 2018-present LCXM
# Reference — 月报发布 Skill

## 输入格式：MD 与 PDF

- **支持的输入**：`.md`（Markdown）与 `.pdf` 均可。
- **MD**：直接解析，按标题/列表/段落生成对应 HTML 区块。
- **PDF**：先提取正文再生成 HTML。推荐方式：
  - **Python**：`pdfplumber`（`pdfplumber.open(path).pages` 逐页 `extract_text()`）或 `PyMuPDF`（`fitz.open(path)`），提取后按段落/换行整理为层级结构（标题、列表、正文），再套用与 MD 相同的 [HTML 生成规范](SKILL.md#html-生成规范) 与模板。
  - 提取时保留顺序与层级，不省略任何要点；若 PDF 含表格，可提取为 HTML `<table>` 或列表，样式与主题一致。

---

## 得物极光蓝色值

全站统一使用以下色值，保证视觉一致。

| 用途       | 色值 | 说明 |
|------------|------|------|
| 主色       | `#0066FF` | 标题强调、关键数字、按钮、边框、图表主色 |
| 主色 RGB   | `rgb(0, 102, 255)` | 用于 CSS 变量或 JS |
| 浅色/低透明 | `rgba(0, 102, 255, 0.15)` | 背景块、弱强调 |
| 中透明     | `rgba(0, 102, 255, 0.35)` | 分隔、装饰 |
| 高透明     | `rgba(0, 102, 255, 0.6)`  | 强调、线条 |
| 背景       | `#FFFFFF` | 页面背景 |

**注意**：仅用极光蓝一种高亮色做透明度渐变，禁止与其他高亮色做渐变。

---

## 滚动动效说明（Framer Motion vs 静态 HTML）

- **Framer Motion** 的 `whileInView` 为 React API，需在 React 环境中使用。若通过 CDN 引入 React + Framer Motion 并挂载组件，可直接使用 `motion.div` + `whileInView`、`viewport`。
- **纯静态 HTML 模板**（本 skill 提供的 `templates/`）：未使用 React，滚动动效使用 **Intersection Observer** 实现与 Apple 官网类似的「进入视口时淡入+位移」，视觉与 Framer Motion 的 `whileInView` 一致。模板中仍保留 Framer Motion CDN 链接，便于日后用 React 生成时复用。

---

## CDN 链接示例

在单页 HTML 的 `<head>` 中引入（版本可随需更新）：

```html
<!-- Tailwind CSS 3.x Play CDN -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Framer Motion -->
<script src="https://unpkg.com/framer-motion@11/dist/framer-motion.js" crossorigin="anonymous"></script>

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" />
```

若使用 Material Icons 替代 Font Awesome：

```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
```

图表（按需）：

```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
```

---

## 本机部署命令

站点目录约定：`dist/`（或项目根下的 `index.html` + `reports/`）。

在 `dist/` 目录下执行其一即可：

```bash
# Node（需已安装 Node）
npx serve .

# 或指定端口
npx serve . -l 8080
```

```bash
# Python 3
python3 -m http.server 8080
```

局域网访问：`http://<本机IP>:8080`（将 `8080` 换成实际端口）。

---

## 索引页结构说明

- **文件**：`dist/index.html`
- **内容**：单个 HTML 页面，列表展示历史月报。
- **每条条目**：
  - 月份（如 `2025-11`）
  - 标题（如 `多语言月报`）
  - 链接：指向 `reports/YYYY-MM/report.html`（或当期实际文件名）

可选用时间倒序；若有多类月报，可加标签（如「多语言」「前端」）。样式需与月报单页一致（Bento、极光蓝、Tailwind、Framer Motion）。

新增一期月报后，在索引页的列表容器中追加一条对应链接即可。

---

## 目录约定

```
dist/
├── index.html          # 索引页
└── reports/
    ├── 2025-11/
    │   └── report.html
    └── 2025-12/
        └── report.html
```

Skill 输出单页 HTML 时，路径格式：`dist/reports/YYYY-MM/report.html`（或与用户约定的文件名）。

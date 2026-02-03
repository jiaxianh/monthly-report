---
name: monthly-report-publish
description: Converts Markdown or PDF monthly reports to Bento Grid and Dewu aurora blue themed HTML, pushes code to a private GitHub repo, and maintains an index page for local/LAN access. Use when the user mentions publishing a monthly report, converting a report to HTML, uploading reports to GitHub, or viewing historical reports. Accepts .md and .pdf input.
---

# Monthly Report Publish

## Quick Start

When the user wants to publish a monthly report:

1. **Confirm input**: Source may be a `.md` or `.pdf` file. For **MD**: parse directly. For **PDF**: extract text (e.g. with pdfplumber, PyMuPDF, or similar), then structure the content into sections/titles/lists as needed and feed into the same HTML pipeline; do not omit any content from the PDF.
2. **Convert to HTML**: From the (parsed or extracted) content, produce a single HTML page that strictly follows the [HTML 生成规范](#html-生成规范) below. Output to the agreed directory (e.g. `dist/reports/YYYY-MM/`).
3. **Update index**: Add an entry to `index.html` with「month + title + link」to the new report.
4. **Deploy locally & push**: Start a static server for LAN access; run `git add`, `commit`, `push` to the private GitHub repository.

## Workflow

```
MD 或 PDF 月报 → 解析/提取正文 → 套用 HTML 规范 → 输出单页 HTML → 更新索引页 → 本机 serve / push 到 GitHub 私有仓库
```

- **Output layout**: Put each report under `dist/reports/YYYY-MM/` (e.g. `dist/reports/2025-11/report.html`). Index at `dist/index.html`.
- **Git**: Private repo, default branch `main`. Before push, ensure no tokens or secrets are committed.

---

## HTML 生成规范

生成月报 HTML 时**必须**严格遵循以下规范，并**不得省略月报中的任何内容要点**（标题、列表、数据、结论均需保留并合理呈现）。

### 视觉与版式

1. **Bento Grid + 得物极光蓝**
   - 使用 Bento Grid 布局：卡片式网格、大小块错落。
   - 纯白背景 `#ffffff`；高亮色使用**得物极光蓝**（色值见 [reference.md](reference.md)），用于标题强调、关键数字、按钮、边框等。

2. **超大字体/数字与比例反差**
   - 核心要点用超大字体或超大数字（如 Tailwind `text-7xl`、`text-8xl` 或更大）。
   - 画面中必须有**超大视觉元素**与小元素形成明显比例反差，避免整页均匀字号。

3. **中英文混排**
   - 中文：大号、粗体，作为主标题与核心信息。
   - 英文：小号，作为点缀（副标题、标签、装饰文案）。

4. **勾线图形化**
   - 数据可视化或配图使用**简洁勾线风格**（线框、线条图、简笔画式图表）。
   - 与极光蓝或灰色线条搭配，避免复杂填色。

5. **高亮色与科技感**
   - 仅用极光蓝的**自身透明度渐变**（如 `rgba(0,102,255,0.1)` → `rgba(0,102,255,0.6)`）营造科技感。
   - **禁止**不同高亮色之间互相渐变。

6. **Apple 风格滚动动效**
   - 向下滚动时，区块依次进入视口并配合淡入、位移或轻微缩放。
   - 使用 Framer Motion 的 `whileInView`、`viewport` 等实现，避免过于花哨。

### 数据与图表

- **在线图表**：若需图表，可引用 ECharts、Chart.js 等（CDN），**样式须与主题一致**：白底、极光蓝系、勾线或简洁风格。

### 技术栈（必须）

- **Framer Motion**：通过 CDN 引入，用于滚动与入场动效。
- **HTML5 + TailwindCSS 3.0+**：通过 CDN 引入（Play CDN 或指定版本）。
- **图标**：Font Awesome 或 Material Icons，通过 CDN 引入；**禁止用 emoji 作为主要图标**。
- **内容完整性**：转换时**不得省略**月报中的内容要点。

### 实现要点

- **单页结构**：一个 HTML 文件，`<head>` 中引入 Tailwind、Framer Motion、图标库的 CDN；`<body>` 为 Bento 网格容器 + 多个 section。
- **输入格式**：**MD** — 将 MD 转为 HTML 片段后嵌入模板，或按 MD 结构手写对应 HTML 区块。**PDF** — 先用工具（如 pdfplumber、PyMuPDF）提取全文与结构，再按章节/列表整理为内容，套用同一 HTML 模板；不得省略 PDF 中的要点。
- **色值**：得物极光蓝等色值在 [reference.md](reference.md) 中统一给出，全站一致。

模板可参考：[templates/report.html](templates/report.html)；索引页参考：[templates/index.html](templates/index.html)。

---

## 本机部署与 Git

- **本地/局域网访问**：在站点目录（如 `dist/`）执行 `npx serve .` 或 `python -m http.server 8080`，局域网通过 `http://<本机IP>:8080` 访问。
- **Git 推送**：代码推送到 GitHub **私有仓库**；不启用 GitHub Pages。推送前确认无 token、密钥等敏感信息。

详见 [reference.md](reference.md)。

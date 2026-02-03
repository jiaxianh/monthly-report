# 使用 Gemini 重新生成月报 HTML

## 依赖

- Python 3 + 项目虚拟环境 `.venv`（已含 PyMuPDF、google-generativeai）
- Google Gemini API Key

## 一键运行（Gemini 3）

在项目根目录执行：

```bash
# 使用 Gemini 3（若 API 已开放该模型）
export GEMINI_MODEL=gemini-3-flash   # 或 gemini-3.0-flash / gemini-3-pro
export GOOGLE_API_KEY=你的API密钥

.venv/bin/python3 scripts/generate_report_with_gemini.py
```

或使用默认模型（gemini-2.0-flash）：

```bash
export GOOGLE_API_KEY=你的API密钥
.venv/bin/python3 scripts/generate_report_with_gemini.py
```

生成结果会覆盖 `dist/reports/2025-11/report.html`。

## 获取 API Key

1. 打开 [Google AI Studio](https://aistudio.google.com/) 或 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建 API Key（Gemini API）
3. 将 Key 设为环境变量 `GOOGLE_API_KEY` 或 `GEMINI_API_KEY`（勿提交到 Git）

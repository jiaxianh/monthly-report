#!/usr/bin/env python3
"""
使用 Google Gemini API 将月报 PDF 正文生成符合 Bento + 得物极光蓝规范的 HTML。
需要环境变量 GOOGLE_API_KEY 或 GEMINI_API_KEY。可选 GEMINI_MODEL：默认 gemini-2.0-flash；若要用 Gemini 3，可设 GEMINI_MODEL=gemini-3-flash 或 gemini-3.0-flash（以 API 实际支持为准）。
"""
import os
import re
import sys

# 项目根目录
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# 若存在 .env 则加载（可用 pip install python-dotenv）
_env_path = os.path.join(ROOT, ".env")
if os.path.isfile(_env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass


def extract_pdf_text(pdf_path: str) -> str:
    """从 PDF 提取全文。优先使用项目 .venv 中的 PyMuPDF。"""
    try:
        import fitz
    except ImportError:
        raise SystemExit("请先安装 PyMuPDF: pip install pymupdf 或在项目下执行 .venv/bin/pip install pymupdf")
    pdf = fitz.open(pdf_path)
    parts = []
    for page in pdf:
        parts.append(page.get_text())
    pdf.close()
    return "\n".join(parts)


def load_spec() -> str:
    """返回 HTML 生成规范说明（给 Gemini 的 prompt 用）。"""
    return r"""
请根据下方「月报正文」生成**单页完整 HTML**，严格满足以下规范，且**不得省略任何内容要点**。

## 视觉与版式
1. **Bento Grid + 得物极光蓝**：卡片式网格、大小块错落；纯白背景 #ffffff；高亮色得物极光蓝 #0066FF（以及 rgba(0,102,255,0.15)、0.35、0.6 做透明度渐变）。
2. **超大字体/数字**：核心要点用 text-7xl / text-8xl 或更大，与小字形成明显反差。
3. **中英文混排**：中文大号粗体为主，英文小号点缀（副标题、标签）。
4. **勾线图形化**：数据可视化用简洁勾线风格（SVG 线框），极光蓝或灰色，避免复杂填色。
5. **高亮色**：仅极光蓝自身透明度渐变，禁止不同高亮色互相渐变。
6. **滚动动效**：区块进入视口时淡入+位移，用 Intersection Observer 或 Framer Motion；可给 section 加 class reveal-section，CSS: opacity 0→1, transform translateY(32px)→0。

## 技术栈（必须）
- HTML5，TailwindCSS 3.0+ 通过 CDN：https://cdn.tailwindcss.com（在 tailwind.config 中扩展 colors.aurora：DEFAULT #0066FF, light/mid/strong 为上述 rgba）。
- Framer Motion CDN、Font Awesome 或 Material Icons CDN。禁止用 emoji 作为主要图标。
- 单页结构：一个完整 HTML 文件，<body> 内为 Bento 网格容器与多个 section，保留月报所有标题、列表、数据、结论。

## 输出要求
只输出一个完整的 HTML 文档（从 <!DOCTYPE html> 到 </html>），不要输出 markdown 代码块包裹或多余解释。若被包在 ```html ... ``` 中，我会自动剥离。
"""


def call_gemini(content: str, model: str, api_key: str) -> str:
    """调用 Gemini API，返回生成的 HTML 文本。"""
    api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("请设置环境变量 GOOGLE_API_KEY 或 GEMINI_API_KEY")

    prompt = load_spec() + "\n\n## 月报正文\n\n" + content

    # 优先使用 google-generativeai（genai）
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        gemini = genai.GenerativeModel(model)
        response = gemini.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )
        if not response.text:
            raise RuntimeError(response.prompt_feedback or "Empty response")
        return response.text.strip()
    except ImportError:
        pass

    # 备选：google-genai 新 SDK
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )
        if response.text:
            return response.text.strip()
        raise RuntimeError("Empty response from Gemini")
    except ImportError as e:
        raise SystemExit(
            "请安装 Gemini SDK 之一： pip install google-generativeai  或  pip install google-genai"
        ) from e


def extract_html_from_response(text: str) -> str:
    """从模型输出中剥离 markdown 代码块，得到纯 HTML。"""
    text = text.strip()
    # 去掉 ```html ... ``` 或 ``` ... ```
    m = re.search(r"^```(?:html)?\s*\n?(.*?)```\s*$", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text


def main():
    pdf_path = os.path.join(ROOT, "2025.11 多语言月报.pdf")
    out_path = os.path.join(ROOT, "dist", "reports", "2025-11", "report.html")
    # Gemini 3: 可设为 gemini-3-flash / gemini-3.0-flash / gemini-3-pro 等（以 Google API 文档为准）
    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

    if not os.path.isfile(pdf_path):
        raise SystemExit(f"未找到 PDF: {pdf_path}")

    print("正在从 PDF 提取正文…")
    content = extract_pdf_text(pdf_path)
    print(f"已提取约 {len(content)} 字。")

    print(f"正在调用 Gemini ({model}) 生成 HTML…")
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    raw = call_gemini(content, model, api_key)
    html = extract_html_from_response(raw)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已写入: {out_path}")


if __name__ == "__main__":
    main()

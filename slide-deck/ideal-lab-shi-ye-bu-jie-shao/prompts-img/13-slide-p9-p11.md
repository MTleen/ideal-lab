Slide type: Content

Title: "P9 智能配图 → P11 文档渲染"

P9 智能配图 (illustration):
What it does: 分析章节内容，判断哪些地方需要配图，自动选择工具生成并插入
Input: sections/*.md（写作完成的各章节文件）
Output: 更新后的 sections/*.md + images/ 目录（生成的图片文件）
Tool selection logic:
  - 流程图 / 时序图 → Mermaid CLI 渲染为 PNG（mmdc）
  - 架构图 / 数据图 / 原型图 / 路线图 → baoyu-image-gen AI 图片生成
Principles:
  - 内容优先：图服务于文字，不是装饰
  - 统一风格：白底、学术配图规范、中文标注
  - 按需生成：不是每段都要配图，只在需要时生成

P11 文档渲染 (document-render):
What it does: 将 Markdown 中间产物组装渲染为最终交付格式
Input: sections/*.md + images/
Output: 最终交付物
Supported formats:
  - markdown: 无需渲染，直接使用
  - docx: Pandoc + python-docx，中文字体/字号/间距标准化（宋体/Times New Roman 正文，黑体/Arial 标题）
  - pptx: PptxGenJS 转换
Key principle: "Markdown 中间产物永久保留，渲染生成格式副本，可随时重新渲染为其他格式"

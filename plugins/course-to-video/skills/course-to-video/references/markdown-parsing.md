# Markdown 解析规则

将 Markdown 课程文件解析为结构化幻灯片数据（`slides.json`）的规则。

## 文件排序

按文件名前缀排序，支持以下模式：

- `01-xxx.md`、`02-xxx.md`（数字+连字符）
- `01_xxx.md`（数字+下划线）
- `00-before-start.md`（前导零+描述）
- `index.md`（课程目录首页，排在最前面）

如果存在 `index.md`，优先读取作为课程封面信息。

## 幻灯片切分规则

### H1（`#`）→ 分节页（slide-section）

H1 标题生成为全屏居中的分节页，用于课程的大章节分隔。

```
# 第一章：准备工作
```

→ 独立一页，类型 `section`。

### H2（`##`）→ 内容页（slide-content）

H2 是最常见的幻灯片类型。标题作为幻灯片标题，后续内容作为幻灯片正文。

```
## 安装 Node.js
正文内容...
```

### H3（`###`）→ 视密度决定

- 如果 H3 下的正文 < 80 字符：**合并到父 H2 页**
- 如果 H3 下的正文 >= 80 字符：**独立成页**

### 水平分割线（`---`）

强制开始新幻灯片，无论当前内容密度如何。

### 代码块

独立的围栏代码块（``` ... ```）生成 `code` 类型幻灯片。代码块前面的段落作为该页的说明文字。

```
这是说明文字：

```python
print("hello")
```
```

→ 一页 code slide，标题取自前文，代码块在 pre 标签内。

### 引用块（`> blockquote`）

引用块合并到当前幻灯片，渲染为带左边框的高亮区域。不独立成页。

### 图片（`![alt](url)`）

图片合并到前一张幻灯片。如果图片紧跟 H2 标题，则该页为图片页。

### 表格

- ≤ 3 行：内联在当前幻灯片中
- \> 3 行：拆分为两页，或改为要点列表

## 内容密度规则

- **理想幻灯片**：1 个标题 + 3-6 个要点，或 1 个标题 + 1 段说明 + 1 个代码块
- **列表 > 8 项**：拆分为两页（前 N 项一页，后 M 项一页）
- **代码块 > 15 行**：截断，添加注释 `// ... 更多内容见课程文档`
- **纯文本段落 > 200 字**：考虑拆分或提取要点

## slides.json 输出格式

```json
{
  "course_title": "课程标题（来自 index.md 的 H1 或 frontmatter.title）",
  "course_subtitle": "副标题（来自 index.md 的描述）",
  "course_tags": "标签行（如：零基础 · 纯实操 · 不用写代码）",
  "source_files": ["index.md", "01-intro.md", "02-setup.md"],
  "config": {
    "resolution": [1280, 720],
    "voice": "zh-CN-YunxiNeural",
    "theme": "dark"
  },
  "slides": [
    {
      "slide_number": 1,
      "type": "cover",
      "title": "课程标题",
      "body": "",
      "bullet_points": [],
      "code_block": null,
      "notes": "原始 markdown 上下文，用于旁白创作参考"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "安装工具",
      "body": "选择一个 AI 代码编辑器...",
      "bullet_points": ["Trae: 免费", "Cursor: 更成熟"],
      "code_block": null,
      "notes": "原始 markdown 上下文"
    },
    {
      "slide_number": 3,
      "type": "code",
      "title": "示例代码",
      "body": "",
      "bullet_points": [],
      "code_block": "console.log('hello')",
      "notes": "原始 markdown 上下文"
    }
  ]
}
```

## 特殊处理

### Frontmatter

课程文件可能有 YAML frontmatter。提取以下字段：
- `title` → 课程标题
- `description` → 课程副标题
- `order` → 文件排序辅助（但优先按文件名排序）

### 附录（appendix/）

`appendix/` 目录下的文件通常包含模板、参考资源等，不纳入幻灯片主体。可选择性生成 1 页"参考资源"幻灯片，指向附录。

### 嵌套列表

Markdown 嵌套列表（缩进的子列表）扁平化处理，用卡片组件展示层级关系。

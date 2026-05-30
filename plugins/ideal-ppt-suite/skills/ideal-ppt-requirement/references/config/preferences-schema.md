# Preferences Schema — 用户偏好加载规格

本文件定义 `EXTEND.md` 的 Schema 和加载优先级。EXTEND.md 用于存储用户的跨项目偏好，在 research 阶段自动加载。

---

## EXTEND.md 位置

```
{project-root}/EXTEND.md
```

当 ideal-ppt-requirement 启动时，检测项目根目录是否存在 `EXTEND.md`，如存在则读取用户偏好并合并到分析中。

---

## Schema 定义

```yaml
# EXTEND.md YAML frontmatter
---
preferences:
  # 默认画幅格式
  canvas_format: "1280x720"    # 可选: 1280x720, 1024x768, 1242x1660, 1080x1080, 1080x1920

  # 默认语言
  language: "zh"               # 可选: zh, en, ja

  # 默认受众类型
  audience: "practitioner"     # 可选: beginner, practitioner, expert, executive, mixed

  # 默认风格偏好
  style:
    preset: "china-telecom"    # 可选: china-telecom, scientific
    texture: "clean"
    mood: "professional"       # china-telecom=professional, scientific=cool
    typography: "geometric"    # china-telecom=geometric, scientific=technical
    density: "ultra-dense"     # 可选: dense, ultra-dense

  # 品牌色（如有）
  brand_colors:
    primary: "#C41E24"         # HEX 格式
    secondary: "#005BAC"
    accent: "#25364D"

  # 图片策略
  image_approach: "none"       # 可选: none, user-provided, ai-generated, placeholders

  # 评审偏好
  review:
    skip_outline: false
    skip_prompts: false
    skip_images: false

  # 图标偏好
  icon_style: "built-in"       # 可选: emoji, ai-generated, built-in, none

  # 字体偏好
  fonts:
    zh_title: "MiSans Bold"
    zh_body: "MiSans Regular"
    en_title: "Liter Bold"
    en_body: "HedvigLettersSans"
---
```

---

## 加载优先级

优先级从高到低：

```
1. 用户在 Step 3 苏格拉底提问中的回答      ← 最高优先级
2. 命令行参数 (--style, --audience, --lang)  ← 高优先级
3. EXTEND.md 中的偏好设置                   ← 中优先级
4. Step 2 自动分析结果                      ← 低优先级（默认值来源）
```

### 合并规则

- 高优先级的设置覆盖低优先级
- 未被覆盖的字段使用低优先级的值
- 所有层级都未设置的字段使用系统默认值

### 系统默认值

```yaml
canvas_format: "1280x720"
language: "zh"
audience: "practitioner"
style:
  preset: "china-telecom"
  texture: "clean"
  mood: "professional"
  typography: "geometric"
  density: "ultra-dense"
brand_colors: null
image_approach: "none"
review:
  skip_outline: false
  skip_prompts: false
  skip_images: false
icon_style: "built-in"
fonts:
  zh_title: "MiSans Bold"
  zh_body: "MiSans Regular"
  en_title: "Liter Bold"
  en_body: "HedvigLettersSans"
```

---

## 检测逻辑

```
1. 检查 {project-root}/EXTEND.md 是否存在
2. 如存在，解析 YAML frontmatter
3. 校验 Schema 字段合法性
4. 合并到 Step 2 分析结果中（作为中优先级覆盖）
5. 如 EXTEND.md 不存在，跳过，使用系统默认值
```

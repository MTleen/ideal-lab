# 预设 → 维度映射

将 18 种预设风格映射到其维度组合。每个风格的完整定义（含设计 token、色值、组件规范）见 `../styles/{预设}.md`，采用 DESIGN.md 格式。

## 映射表

| 预设 | 纹理 | 色调 | 字体 | 密度 | 质感 | 间距 |
|------|------|------|------|------|------|------|
| blueprint | grid | cool | technical | balanced | soft-shadow | standard |
| chalkboard | organic | warm | handwritten | balanced | flat | generous |
| corporate | clean | professional | geometric | balanced | soft-shadow | standard |
| minimal | clean | neutral | geometric | minimal | flat | editorial |
| sketch-notes | organic | warm | handwritten | balanced | flat | generous |
| watercolor | organic | warm | humanist | minimal | flat | editorial |
| dark-atmospheric | clean | dark | editorial | balanced | layered-depth | standard |
| notion | clean | neutral | geometric | dense | soft-shadow | standard |
| bold-editorial | clean | vibrant | editorial | balanced | layered-depth | editorial |
| editorial-infographic | clean | cool | editorial | dense | soft-shadow | compact |
| fantasy-animation | organic | vibrant | handwritten | minimal | flat | generous |
| intuition-machine | clean | cool | technical | dense | soft-shadow | compact |
| pixel-art | pixel | vibrant | technical | balanced | flat | standard |
| scientific | clean | cool | technical | dense | flat | compact |
| vector-illustration | clean | vibrant | humanist | balanced | flat | generous |
| vintage | paper | warm | editorial | balanced | flat | generous |
| high-density-infographic | clean | cool | technical | dense | flat | compact |
| china-telecom | clean | professional | geometric | dense | soft-shadow | standard |

## 预设详情

### blueprint（蓝图风格）
- **维度**: grid + cool + technical + balanced
- **感受**: 工程精确、分析清晰
- **自动触发**: 架构、系统、数据、分析、技术、blueprint

### chalkboard（黑板风格）
- **维度**: organic + warm + handwritten + balanced
- **感受**: 课堂温暖、教育感
- **自动触发**: 课堂、教学、学校、chalkboard

### corporate（商务风格）
- **维度**: clean + professional + geometric + balanced
- **感受**: 商业可信、机构信任
- **自动触发**: 投资者、季度、业务、企业、corporate

### minimal（极简风格）
- **维度**: clean + neutral + geometric + minimal
- **感受**: 极致高级感、高管聚焦
- **自动触发**: 管理层、简洁、干净、简单、minimal

### sketch-notes（手绘风格）
- **维度**: organic + warm + handwritten + balanced
- **感受**: 友好学习、亲和教育
- **自动触发**: 教程、学习、教育、指南、入门、sketch-notes

### watercolor（水彩风格）
- **维度**: organic + warm + humanist + minimal
- **感受**: 艺术感、自然、生活方式
- **自动触发**: 生活、健康、旅行、艺术、watercolor

### dark-atmospheric（暗色风格）
- **维度**: clean + dark + editorial + balanced
- **感受**: 电影感、娱乐
- **自动触发**: 娱乐、音乐、游戏、氛围、dark

### notion（块状风格）
- **维度**: clean + neutral + geometric + dense
- **感受**: SaaS 专业感、数据导向
- **自动触发**: SaaS、产品、仪表盘、指标、notion

### bold-editorial（杂志风格）
- **维度**: clean + vibrant + editorial + balanced
- **感受**: 杂志冲击力、keynote 戏剧感
- **自动触发**: 发布、营销、演讲、杂志、bold-editorial

### editorial-infographic（图表风格）
- **维度**: clean + cool + editorial + dense
- **感受**: 出版物品质、信息丰富
- **自动触发**: 解读、新闻、科学传播、editorial-infographic

### fantasy-animation（动画风格）
- **维度**: organic + vibrant + handwritten + minimal
- **感受**: 魔幻、讲故事
- **自动触发**: 故事、童话、动画、魔法、fantasy

### intuition-machine（架构图风格）
- **维度**: clean + cool + technical + dense
- **感受**: 技术简报、双语文档
- **自动触发**: 汇报、学术、研究、双语、架构图、intuition

### pixel-art（像素风格）
- **维度**: pixel + vibrant + technical + balanced
- **感受**: 复古游戏、开发者文化
- **自动触发**: 游戏、复古、像素、开发者、pixel

### scientific（论文风格）
- **维度**: clean + cool + technical + dense
- **感受**: 学术精确、研究品质
- **自动触发**: 生物、化学、医学、科学、scientific

### vector-illustration（插画风格）
- **维度**: clean + vibrant + humanist + balanced
- **感受**: 扁平设计、友好创意
- **自动触发**: 创意、儿童、可爱、vector

### vintage（复古报纸风）
- **维度**: paper + warm + editorial + balanced
- **感受**: 历史感、遗产叙事
- **自动触发**: 历史、遗产、复古、探险、vintage

### high-density-infographic（高密度信息图）
- **维度**: clean + cool + technical + dense
- **感受**: 最大信息密度、技术销售
- **自动触发**: 技术销售、企业产品、高密度信息、sales、enterprise、product deck

### china-telecom（中国电信风格）
- **维度**: clean + professional + geometric + dense + soft-shadow + standard
- **感受**: 央企稳重、科技精致、红蓝双色
- **自动触发**: 中国电信、政企、算力、云、AIDC、央企、chinamobile

## 构建自定义组合

当用户选择"自定义维度"时，可自由组合：

- **纹理** (5): clean、grid、organic、pixel、paper
- **色调** (6): professional、warm、cool、vibrant、dark、neutral
- **字体** (5): geometric、humanist、handwritten、editorial、technical
- **密度** (4): minimal、balanced、dense、ultra-dense
- **质感** (5): flat、soft-shadow、glassmorphism、neumorphism、layered-depth
- **间距** (4): compact、standard、generous、editorial

总可能组合数: 5 × 6 × 5 × 4 × 5 × 4 = **12,000 种独特风格**

18 种预设是精选的常用组合。完整风格定义见各预设的 DESIGN.md 文件。

## 推荐组合（超出预设）

| 自定义名称 | 纹理 | 色调 | 字体 | 密度 | 质感 | 间距 | 使用场景 |
|------------|------|------|------|------|------|------|----------|
| tech-minimal | clean | neutral | technical | minimal | flat | editorial | 开发者 keynote |
| warm-editorial | paper | warm | editorial | balanced | soft-shadow | generous | 遗产品牌 |
| dark-technical | grid | dark | technical | dense | layered-depth | compact | 安全、DevOps |
| playful-clean | clean | vibrant | humanist | balanced | soft-shadow | generous | 初创公司、应用 |
| glass-tech | clean | cool | technical | balanced | glassmorphism | standard | 前沿科技发布 |

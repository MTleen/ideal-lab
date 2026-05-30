# 预设 → 维度映射

本套件只保留两类企业常用风格，避免在 PPT 生成时让风格选择稀释质量。

## 映射表

| 预设 | 中文名 | 纹理 | 色调 | 字体 | 密度 | 质感 | 间距 | 风格文件 |
|------|--------|------|------|------|------|------|------|----------|
| scientific | 学术风格 | clean | cool | technical | dense | flat | compact | `../styles/scientific.md` |
| china-telecom | 电信高信息密度风格 | clean | professional | geometric | ultra-dense | soft-shadow | compact | `../styles/china-telecom.md` |

## 选择规则

### scientific（学术风格）

- **适用**：论文汇报、课题答辩、研究综述、实验结果、算法/方法论文、技术研究报告。
- **关键词**：学术、论文、研究、实验、方法、模型、假设、数据集、指标、消融、综述、答辩。
- **视觉目标**：像高质量 conference slide 或研究摘要页，强调论证链、数据、方法流程和可复核标注。

### china-telecom（电信高信息密度风格）

- **适用**：中国电信、央企、政企汇报、云网、算力、AI、安全、AIDC、行业解决方案、技术销售、综合报告。
- **关键词**：电信、政企、央企、云、网、算力、安全、AI、AIDC、解决方案、运营商、DICT、集成、标书。
- **视觉目标**：成熟咨询级 one-pager，红蓝品牌节奏，高信息密度，强区块组织，支持参考图片继承电信 PPT 背景气质。

## 默认规则

无法判断时默认使用 `china-telecom`。如果内容明显是论文/研究/实验/学术答辩，则使用 `scientific`。

不再支持任意维度自由组合。若用户确实提供自定义风格，以 `style_reference.description` 或 `style_reference.path` 作为局部覆盖，不新增长期预设。

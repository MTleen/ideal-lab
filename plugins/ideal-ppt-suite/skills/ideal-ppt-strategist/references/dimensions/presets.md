# 风格预设映射

本插件只保留两种长期风格预设。策略阶段必须从两者中选择其一，避免风格库过大导致后续 prompt 发散。

| 预设 | 中文名 | 纹理 | 色调 | 字体 | 密度 | 适用场景 |
|------|--------|------|------|------|------|----------|
| scientific | 学术风格 | clean | cool | technical | dense | 论文汇报、课题答辩、研究综述、实验结果、算法/方法报告 |
| china-telecom | 电信高信息密度风格 | clean | professional | geometric | ultra-dense | 中国电信、央企政企、云网算力、AI、安全、AIDC、DICT、行业解决方案 |

## 选择规则

```
是否明显是学术/论文/研究/实验/综述/答辩？
├─ 是 → scientific
└─ 否 → china-telecom
```

## scientific

- 视觉目标：像高质量 conference slide 或研究摘要页。
- 内容重心：研究问题、方法流程、实验设计、关键指标、结论和局限。
- 版式偏好：research summary、method pipeline、evidence matrix、paper comparison、mechanism diagram。
- 字体：标题可偏学术衬线感，正文和图表标签使用清晰无衬线。
- 禁止：用装饰插画替代研究内容，生成伪公式、伪图表或不可读标签。

## china-telecom

- 视觉目标：成熟咨询级 one-pager，高信息密度，红蓝品牌节奏。
- 内容重心：核心结论、KPI、方案架构、流程、对比矩阵、风险与行动项。
- 版式偏好：executive dashboard、consulting one-pager、architecture map、process map、comparison matrix、industry solution page。
- 字体：几何无衬线，小字号可读，标题区紧凑。
- 参考图：可使用电信 PPT 背景图、母版截图或品牌页作为风格锚点；只继承背景质感、红蓝比例、标题栏、装饰线和空间节奏，不复制旧文字、logo、水印、页码。

## 默认

无法判断时使用 `china-telecom`。

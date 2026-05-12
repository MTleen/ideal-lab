# HTML 幻灯片 CSS 模板 — 专业汇报风格

> 匹配技术汇报/咨询报告风格：颜色编码模块、数据表格、架构流程图、高信息密度。

## 1. CSS 变量系统

```css
:root {
  /* ── 模块颜色（颜色=含义） ── */
  --mod-red: #DC2626;         --mod-red-bg: #FEF2F2;     --mod-red-border: #FECACA;
  --mod-blue: #2563EB;        --mod-blue-bg: #EFF6FF;     --mod-blue-border: #BFDBFE;
  --mod-amber: #D97706;       --mod-amber-bg: #FFFBEB;    --mod-amber-border: #FDE68A;
  --mod-green: #059669;       --mod-green-bg: #ECFDF5;    --mod-green-border: #A7F3D0;
  --mod-purple: #7C3AED;      --mod-purple-bg: #F5F3FF;   --mod-purple-border: #C4B5FD;

  /* ── 中性色 ── */
  --text: #111827;
  --text-secondary: #4B5563;
  --text-muted: #9CA3AF;
  --bg: #FFFFFF;
  --bg-page: #F9FAFB;
  --border: #E5E7EB;
  --border-strong: #D1D5DB;

  /* ── 字体 ── */
  --font: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  --font-mono: "SF Mono", "Consolas", "Monaco", monospace;
  --font-number: "DIN Alternate", "Helvetica Neue", system-ui, sans-serif;

  /* ── 字号 ── */
  --fs-title: 28px;
  --fs-section: 18px;
  --fs-card-title: 15px;
  --fs-body: 14px;
  --fs-small: 12px;
  --fs-tiny: 11px;
  --fs-data-lg: 36px;
  --fs-data: 24px;
  --fs-table-head: 13px;
  --fs-table-cell: 12px;
}
```

## 2. 基础样式

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px; overflow: hidden;
  font-family: var(--font); font-size: var(--fs-body);
  line-height: 1.5; color: var(--text);
  background: var(--bg-page); padding: 32px 40px;
}
```

## 3. 页面标题

```css
.page-title {
  font-size: var(--fs-title); font-weight: 700;
  color: var(--text);
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 3px solid var(--mod-red);
  display: inline-block;
}
.page-title.blue { border-color: var(--mod-blue); }
.page-title.green { border-color: var(--mod-green); }
```

## 4. 架构层叠组件

```css
.arch-layer {
  padding: 10px 16px;
  border-radius: 4px;
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 4px;
}
.arch-layer.red   { background: var(--mod-red-bg);   border-left: 4px solid var(--mod-red); }
.arch-layer.blue  { background: var(--mod-blue-bg);  border-left: 4px solid var(--mod-blue); }
.arch-layer.amber { background: var(--mod-amber-bg); border-left: 4px solid var(--mod-amber); }
.arch-layer.green { background: var(--mod-green-bg); border-left: 4px solid var(--mod-green); }
.arch-layer.purple{ background: var(--mod-purple-bg);border-left: 4px solid var(--mod-purple);}

.layer-label {
  width: 90px; font-size: 13px; font-weight: 700;
  flex-shrink: 0;
}
.arch-layer.red   .layer-label { color: var(--mod-red); }
.arch-layer.blue  .layer-label { color: var(--mod-blue); }
.arch-layer.amber .layer-label { color: var(--mod-amber); }
.arch-layer.green .layer-label { color: var(--mod-green); }
.arch-layer.purple .layer-label { color: var(--mod-purple); }

.layer-tags {
  display: flex; gap: 6px; flex-wrap: wrap; flex: 1;
}
.arch-tag {
  padding: 3px 10px; border-radius: 3px;
  font-size: 11px; font-weight: 600; color: white;
}
.arch-layer.red   .arch-tag { background: var(--mod-red); }
.arch-layer.blue  .arch-tag { background: var(--mod-blue); }
.arch-layer.amber .arch-tag { background: var(--mod-amber); }
.arch-layer.green .arch-tag { background: var(--mod-green); }
.arch-layer.purple .arch-tag { background: var(--mod-purple); }

.arrow-row {
  display: flex; justify-content: center; gap: 120px;
  padding: 2px 0; color: var(--text-muted); font-size: 14px;
}
```

## 5. 数据表格

```css
.data-table {
  width: 100%; border-collapse: collapse;
  font-size: var(--fs-table-cell);
}
.data-table th {
  padding: 8px 12px; text-align: left;
  background: #F3F4F6; font-weight: 600;
  border: 1px solid var(--border);
  font-size: var(--fs-table-head); color: var(--text);
}
.data-table td {
  padding: 6px 12px;
  border: 1px solid var(--border);
  color: var(--text-secondary);
}
.data-table td.highlight {
  font-weight: 700; color: var(--mod-red);
}
.data-table td.success {
  font-weight: 700; color: var(--mod-green);
}
.data-table tr:hover td { background: #F9FAFB; }
```

## 6. KPI 数据行

```css
.kpi-row {
  display: flex; gap: 0;
}
.kpi-item {
  flex: 1; text-align: center;
  padding: 12px 8px;
  border-right: 1px solid var(--border);
}
.kpi-item:last-child { border-right: none; }
.kpi-value {
  font-family: var(--font-number);
  font-size: var(--fs-data-lg); font-weight: 700;
  line-height: 1.1;
}
.kpi-value.red    { color: var(--mod-red); }
.kpi-value.blue   { color: var(--mod-blue); }
.kpi-value.green  { color: var(--mod-green); }
.kpi-value.amber  { color: var(--mod-amber); }
.kpi-value.purple { color: var(--mod-purple); }
.kpi-label {
  font-size: var(--fs-small); color: var(--text-secondary);
  margin-top: 4px;
}
.kpi-change {
  font-size: var(--fs-tiny); margin-top: 2px;
}
.kpi-change.up { color: var(--mod-green); }
.kpi-change.down { color: var(--mod-red); }
```

## 7. 信息卡片

```css
.info-card {
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--bg);
}
.info-card.accent-red    { border-left: 4px solid var(--mod-red); }
.info-card.accent-blue   { border-left: 4px solid var(--mod-blue); }
.info-card.accent-green  { border-left: 4px solid var(--mod-green); }
.info-card.accent-amber  { border-left: 4px solid var(--mod-amber); }
.info-card.accent-purple { border-left: 4px solid var(--mod-purple); }

.info-card .card-title {
  font-size: var(--fs-card-title); font-weight: 700;
  margin-bottom: 8px;
}
.info-card.accent-red    .card-title { color: var(--mod-red); }
.info-card.accent-blue   .card-title { color: var(--mod-blue); }
.info-card.accent-green  .card-title { color: var(--mod-green); }
.info-card.accent-amber  .card-title { color: var(--mod-amber); }
.info-card.accent-purple .card-title { color: var(--mod-purple); }

.info-card .card-body {
  font-size: var(--fs-body); color: var(--text-secondary);
}
.info-card ul {
  list-style: none; display: flex; flex-direction: column; gap: 3px;
}
.info-card li::before { content: "• "; color: var(--text-muted); }
```

## 8. 对比布局

```css
.compare-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
}
.compare-side {
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 4px;
}
.compare-side.option-a {
  border-color: var(--mod-red-border);
  background: var(--mod-red-bg);
}
.compare-side.option-a .side-title { color: var(--mod-red); }
.compare-side.option-b {
  border: 2px solid var(--mod-blue);
  background: var(--mod-blue-bg);
}
.compare-side.option-b .side-title { color: var(--mod-blue); }
.side-title { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.side-list {
  list-style: none; font-size: 13px;
  display: flex; flex-direction: column; gap: 3px;
  color: var(--text-secondary);
}
```

## 9. 封面页

```css
body.cover {
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  color: white;
  display: flex; flex-direction: column; justify-content: center;
  padding: 80px;
}
.cover-badge {
  display: inline-block;
  padding: 4px 12px; border-radius: 3px;
  font-size: 12px; font-weight: 600;
  background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7);
  margin-bottom: 16px;
}
.cover-title {
  font-size: 48px; font-weight: 700; line-height: 1.2;
  margin-bottom: 20px;
}
.cover-subtitle {
  font-size: 20px; opacity: 0.8;
  line-height: 1.6; margin-bottom: 40px;
}
.cover-meta {
  display: flex; gap: 24px;
  font-size: 14px; opacity: 0.5;
}
```

## 10. 总结页

```css
body.summary {
  background: #1E293B; color: white;
  display: flex; flex-direction: column; justify-content: center;
  padding: 80px;
}
.summary-title { font-size: 32px; font-weight: 700; margin-bottom: 32px; }
.summary-item {
  display: flex; align-items: center; gap: 16px;
  font-size: 18px; margin-bottom: 16px;
}
.summary-item .num {
  font-family: var(--font-number);
  font-size: 24px; font-weight: 700;
  color: var(--mod-amber);
}
```

## 11. 布局 Grid 预设

```css
.grid-main-side { display: grid; grid-template-columns: 3fr 2fr; gap: 20px; }
.grid-side-main { display: grid; grid-template-columns: 2fr 3fr; gap: 20px; }
.grid-half      { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.grid-third     { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.grid-quarter   { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; }

/* 两行布局 */
.grid-2rows {
  display: grid; grid-template-rows: auto 1fr; gap: 16px;
  height: calc(720px - 64px - 50px); /* 减去 padding 和 title */
}
```

## 验收报告 (ppt-v5-no-overlap)

### C1: 背景图不含文字
- OCR: OCR unavailable; install attempt exit=1, tesseract=missing
- Slide 1: PASS - no OCR text and no text-like leakage in TextBox regions; textlike_boxes=0/10, max_components=0, bg_html_similarity=0.9789
- Slide 2: PASS - no OCR text and no text-like leakage in TextBox regions; textlike_boxes=0/29, max_components=1, bg_html_similarity=0.9839
- Slide 3: PASS - no OCR text and no text-like leakage in TextBox regions; textlike_boxes=0/53, max_components=0, bg_html_similarity=0.9830
- Slide 4: PASS - no OCR text and no text-like leakage in TextBox regions; textlike_boxes=0/44, max_components=0, bg_html_similarity=0.9819
- Slide 5: PASS - no OCR text and no text-like leakage in TextBox regions; textlike_boxes=0/25, max_components=1, bg_html_similarity=0.9779

### C2: 无文字重叠
- PASS - 背景图未检测到残留文字，TextBox 不会与背景文字重叠。

### C3: 整体视觉效果一致
- FAIL - PPTX render: soffice pdf export failed, exit=134 (render unavailable; used structural fallback)
- Slide 1: TextBox->HTML 10/10 (100%); HTML->TextBox 10/18 (56%); background-vs-HTML similarity 0.9789; missing HTML text: Harness 工程平台 | 技术架构与最佳实践 | AI 驱动的 CI/CD、云成本管理、安全测试与混沌工程 | 一体化 DevOps 平台 — 从代码提交到生产部署的全链路自动化 | CI/CD 智能流水线 | 云成本自动优化 (CCM)
- Slide 2: TextBox->HTML 29/29 (100%); HTML->TextBox 29/29 (100%); background-vs-HTML similarity 0.9839
- Slide 3: TextBox->HTML 45/53 (85%); HTML->TextBox 45/45 (100%); background-vs-HTML similarity 0.9830
- Slide 4: TextBox->HTML 44/44 (100%); HTML->TextBox 43/43 (100%); background-vs-HTML similarity 0.9819
- Slide 5: TextBox->HTML 25/25 (100%); HTML->TextBox 25/30 (83%); background-vs-HTML similarity 0.9779; missing HTML text: — Harness 覆盖 CI/CD/STO/CCM/FF 五大领域，无需自建 Jenkins+Spinnaker+ArgoCD 技术栈，部署周期从 6-9 个月缩短至 2-4 周。 | — AIDA 引擎自动推荐 Pipeline 步骤、根因分析部署异常、优化云资源配额，减少 70% 人工决策和排障时间。 | — 年度总成本从 ¥350 万降至 ¥140 万，节省 ¥210 万。CCM 模块持续优化云支出，Spot 实例调度节省 70%。 | — STO 编排 30+ 安全工具，漏洞自动阻断高风险部署，一键生成 SOC2/ISO27001 合规报告，审计零盲区。 | — 一套 Pipeline 适配 AWS/GCP/Azure/阿里云/本地 K8s，环境标准化，供应商切换零成本，避免锁定。

### 总结: 需要修复
- 中间产物: /Users/mathrippermacmini/Documents/Sync/Work/电信/理想/产品/0-最佳实践/slide-deck/harness-engineering/pptx_debug
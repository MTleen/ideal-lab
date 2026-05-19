---
name: image-to-svg
description: >
  将 AI 生成的图片（PNG/JPG/WebP）转换为结构化、ppt-master 兼容的可编辑 SVG 文件。
  通过 Claude Vision 分区精读图片内容（布局、文字、形状、颜色），逐字抄录后生成
  原生矢量 SVG（每个元素可独立编辑）。输出可直接送入 ppt-master 的 svg_to_pptx 管线导出 PPTX。
  Convert AI-generated images into structured, editable SVG compatible with ppt-master pipeline.
triggers:
  - 图片转SVG
  - PNG转SVG
  - image to SVG
  - convert image to editable SVG
  - 把这张图变成可编辑的
  - 从图片生成幻灯片
  - 图片解析
  - 图片还原
  - 复原这张幻灯片
  - 图片转矢量
  - image analysis for PPT
  - reproduce slide from image
  - reconstruct slide from screenshot
---

# Image to SVG

Convert AI-generated images into structured SVG files compatible with ppt-master's `svg_to_pptx` pipeline.

## 🚫 Red Lines (Non-Negotiable)

These rules exist because "looks plausible" is not "faithful reproduction". A pretty SVG that doesn't match the source is a regression, not output.

1. **No memory-based generation.** Every text element MUST be transcribed character-by-character from the source image while looking at it, not from inferred semantics. If a phrase is illegible, mark it `[UNREADABLE]` — never invent content.
2. **No delivery without Step 2.5.** An SVG that has not passed visual fidelity verification (rendered-back PNG vs source image diff) is a draft, not output. Do not present it to the user as "done".
3. **No skipping the per-region pass.** Even for "simple" slides, Step 1 must produce a region-by-region transcript with `(x, y, font_size)` per text element. One-shot whole-slide reads always miss text.
4. **No silent simplification.** If you decide to omit a visual element (e.g., a decorative icon you can't recreate), it must be logged in `analysis/<page>.json` under `omitted[]` with a reason. The user reviews omissions explicitly.
5. **No downgrading structural decoration.** Large brackets, frames, connector paths, arrows, separators, and section containers are layout-bearing elements, not optional decoration. Rebuild them as SVG paths before judging fidelity; do not replace a rounded frame with a generic line or curve.
6. **Skill-first iteration only.** For every new version after a failed judgment, first update this skill (or its references/scripts/analysis contract) to address the systematic failure, then regenerate the SVG under the new rule. Do not directly tune the SVG as the primary fix. If a one-off direct SVG patch is unavoidable, document why it is not a skill gap in the judgment file.
7. **No full-page source-image fallback for editable reconstruction.** Exact visual fidelity must not be achieved by embedding the whole source image. Text must remain editable text. Frames, circles, lines, arrows, dividers, and other simple diagram elements must remain native SVG. Only genuinely complex photos/icons/bitmap details may be embedded as source crops, and every crop must be recorded in `downgrades[]`.

## Core Pipeline

```
Image (PNG/JPG/WebP)
  -> Step 1: Per-region transcript (Claude Vision, zoom-in on each region)
  -> Step 2: SVG generation (faithful to transcript, not to memory)
  -> Step 2.5: Visual fidelity verification (render SVG -> PNG -> diff vs source)
  -> Step 3: SVG quality check (banned features, XML validity)
  -> Step 4: Output svg_output/<page>.svg
  Loop: if 2.5 fails, return to Step 1 on failing region (max 3 rounds)
```

For iterative improvement, every round must leave a trace:
- `diagnostics/<page>.vN.judgment.md`: source-vs-rendered findings.
- A skill/reference/script/analysis-contract change that explains how the next version prevents the same failure.
- `diagnostics/<page>.vN.generation.md`: which updated skill rule(s) were applied to generate this SVG.

When the target is first-shot acceptance on a new image, do not start from a minimal native reconstruction. Apply all accumulated hard gates in the first version:
- classify the layout family before generation;
- build regions, geometry anchors, text inventory, icon inventory, crop plan, and surface/shadow plan first;
- use selective transparent icon crops in v1 when native icon redrawing has repeatedly been the dominant failure mode on similar slides;
- render crop contact sheet before judging the page;
- render PNG, compare image, and same-canvas overlay before writing acceptance.
- run a text-fit preflight before judging: no visible text may be clipped, hidden behind another object, overflow a card/row boundary, or collide with an adjacent inline emphasis run.

## Input Requirements

- Format: PNG (preferred, lossless), JPG, WebP
- Resolution: minimum 1920x1080, Retina (2x/3x) preferred
- One slide per image
- No overlay artifacts (cursors, notifications, annotations)

## Step 1: Per-Region Transcript (NOT a one-shot summary)

A one-shot "look at the slide and summarize" pass always loses text. Force a per-region scan.

### 1.1 Divide the canvas into regions

Read the image once at full resolution to identify regions. A region is a visually grouped block (title bar, single card, chart, footer line, etc.). Typical counts:

| Layout type | Region count |
|-------------|--------------|
| title + body | 2–3 |
| 2/3-column cards | 4–6 |
| dashboard / 5-component | 6–10 |
| comparison / matrix | 5–8 |

Write the region map to `analysis/<page>.regions.json`:

```json
{
  "canvas": {"width": 1920, "height": 1080},
  "regions": [
    {"id": "R1", "role": "title",    "bbox": [0.04, 0.02, 0.92, 0.10]},
    {"id": "R2", "role": "card-1",   "bbox": [0.04, 0.15, 0.30, 0.65]},
    {"id": "R3", "role": "card-2",   "bbox": [0.35, 0.15, 0.30, 0.65]},
    {"id": "R4", "role": "card-3",   "bbox": [0.66, 0.15, 0.30, 0.65]},
    {"id": "R5", "role": "footer",   "bbox": [0.04, 0.93, 0.92, 0.05]}
  ]
}
```

`bbox` is `[x, y, w, h]` in 0–1 normalized canvas coords.

### 1.2 Zoom into each region and transcribe verbatim

For each region, look at that region only (mentally crop) and transcribe **every visible character**. Do not paraphrase, do not summarize, do not "complete" trailing ellipsis. If a glyph is illegible at the available resolution, write `[UNREADABLE:n_chars]`.

Write per-element entries to `analysis/<page>.elements.json`:

```json
{
  "elements": [
    {
      "region": "R1",
      "type": "text",
      "content": "精密支撑系统的三大支柱",
      "position": {"x": 80, "y": 100, "anchor": "start"},
      "style": {"font_size": 44, "font_weight": "bold", "fill": "#1A2A4A", "font_family": "Microsoft YaHei"}
    },
    {
      "region": "R2",
      "type": "text",
      "content": "10PB+",
      "position": {"x": 200, "y": 650, "anchor": "middle"},
      "style": {"font_size": 36, "font_weight": "bold", "fill": "#3A5BBF"}
    },
    {
      "region": "R2",
      "type": "shape",
      "shape": "rect",
      "position": {"x": 80, "y": 160, "w": 560, "h": 600},
      "style": {"fill": "#EAF2FB", "stroke": "#3A5BBF", "stroke_width": 2, "rx": 12}
    }
  ],
  "omitted": [
    {"region": "R3", "reason": "decorative icon — could not recreate as vector", "fallback": "<image>"}
  ]
}
```

Hard rules:
- Every visible text → one `{type: "text"}` entry. No exceptions, no "etc."
- `position` uses pixel coords in the viewBox space (e.g., 1920×1080), not normalized.
- `font_size` is a number in px. Anchor your scale: measure the title's height vs canvas height (e.g., title fills 8% of 1080 → font_size ≈ 48–56 px) and propagate the ratio.
- Anything you can't reproduce as a vector → goes into `omitted[]` with a fallback plan. Do not silently drop it.
- Structural frames/connectors must be represented as paths with approximate control points. Record their start/end, corner radii, arrowheads, and whether they pass behind or in front of content.

### 1.3 Geometry anchor table (MANDATORY before SVG generation)

Before authoring SVG, create a geometry anchor table in `analysis/<page>.elements.json` (or a sibling `analysis/<page>.geometry.json`). This is the "do not drift" contract for one-to-one reconstruction.

Required anchors:
- Canvas source size and target viewBox scale.
- Header title bbox.
- Text run bboxes for visually dominant titles/headings, not only baselines.
- Every major frame/container bbox.
- Every repeated card/column bbox and divider line.
- Every circle/ellipse center and radius.
- Every icon bbox, not just center.
- Every connector/arrow path bbox and endpoint.

Example:

```json
{
  "geometry_anchors": {
    "scale_to_viewbox": {"source_px": [1672, 941], "viewBox": [1920, 1080]},
    "main_red_frame": {"bbox": [92, 241, 1744, 341], "tolerance_px": 12},
    "node_1_circle": {"cx": 315, "cy": 582, "r": 173, "tolerance_px": 10},
    "insight_bar": {"bbox": [71, 815, 1765, 204], "tolerance_px": 12}
  }
}
```

Hard gate:
- Do not accept an SVG whose major anchors drift more than the listed tolerance.
- If the rendered SVG "looks redesigned", inspect anchor drift first; do not keep tuning icons or text while the layout frame is off.
- For repeated elements, preserve the source spacing rhythm. Do not distribute by intuition if the source provides centers/bounds.
- For dominant text, choose font size/weight/position to match the source text bbox. A correct string with the wrong visual bbox is still a fidelity failure.
- For icons, match the full bbox and visual weight. A semantically correct icon that is 20% too large, too heavy, or miscentered fails one-to-one reproduction.
- For text-heavy fidelity failures, run a source-vs-rendered text bbox calibration pass. Measure dominant dark-text bboxes on the scaled source and rendered output, then adjust SVG font size, weight, and baseline from those measurements before the next version.

### 1.3b Group-level anchor calibration (MANDATORY for one-to-one loops)

When the user asks for one-to-one reproduction, local element tuning is not enough. Before changing individual text sizes or icon details, calibrate whole visual groups against the scaled source image.

Required group anchors:
- Header badge shape bbox and slant direction.
- Header title chain bbox, subtitle bbox, and baseline rhythm.
- Main structural frame/callout bbox, including line y positions, curve endpoints, badge/cloud callout bbox, and arrow tips.
- Chain row circle centers/radii, badge centers, chevron centers, icon bboxes, title bboxes, and body text bboxes.
- Bottom insight bar bbox, vertical tag bbox, divider x positions, card icon bboxes, heading bboxes, and body bboxes.
- Background bands/vignettes/shadows if they are visible; sample the center/corner luminance and rebuild them as native gradients/shapes, never as a full-page image.

Calibration order:
1. Measure group bboxes on the scaled source and rendered SVG.
2. Fix any group drift that exceeds tolerance before touching text metrics.
3. Then run text bbox calibration inside the now-aligned group.
4. Then inspect icon bboxes and semantic fidelity.

Hard gate:
- Do not accept a version where a major group is visually shifted, stretched, or slanted differently from the source, even if every text string is correct.
- Do not compensate for group drift by moving only the nearest text; move the owning group or its structural anchor geometry.
- Header badges, frames, tags, dividers, circles, and chevrons are simple editable primitives. They must stay native SVG/PPT shapes.
- If text bboxes are aligned but the rendered text still looks too light/heavy, calibrate text ink density while keeping it editable: adjust decimal font sizes, `font-weight`, and only if necessary a small text `stroke-width` (for example `0.2`–`0.8`) with `paint-order="stroke fill"`. Do not convert text to paths or image crops.
- Avoid overcorrecting body text. If a body copy line is too narrow but not visibly too light, prefer a small decimal `font-size` or `letter-spacing` change; do not make normal body copy semi-bold just to increase width. After changing weight/stroke, re-check ink density against source so the fix does not become a new mismatch.
- For normal body copy, if decimal font-size still leaves the text visibly too light, use a micro-stroke (`0.15`–`0.3`) before trying any heavier `font-weight`. This preserves normal-weight editable text while matching rasterized ink density.
- Do not leave a flat white background when the source has a visible vignette, edge shadow, or soft gray band. Use simple SVG gradients or translucent native shapes for these background effects.

### 1.3c Multi-column analogy/comparison calibration

For slides built from repeated comparison columns (e.g., "A is to B as C is to D"), create anchors for the repeated rhythm before generating SVG.

Required anchors:
- Title number badge bbox, title text bbox, and underline start/end.
- Each column's upper card bbox, header strip bbox, icon circle bbox, primary label bbox, and secondary label bbox.
- Each column's lower explanation card bbox, heading bbox, bullet left edge, bullet baselines, and card border color.
- Inter-column connector/chevron bboxes. Chevrons are native editable paths/polygons, not text glyphs or images.
- Bottom insight/conclusion bars, including icon square/circle bbox, label bbox, vertical separator x position, body text bbox, and any faint decorative native line art.

Calibration order:
1. Align all column card bboxes and gutters as a group.
2. Align connector chevrons between cards.
3. Calibrate card header strip heights and color fills.
4. Calibrate text bboxes line by line, especially bullet left edges and baselines.
5. Only then tune icons or decorative background line art.

Text baseline calibration:
- `y` on SVG `<text>` is a baseline, not the top of the measured source text bbox.
- For Chinese bold headings, start with `baseline_y = bbox_top + 0.78 * font_size`; for Latin-heavy text, use `0.72 * font_size`; then adjust by overlay.
- If overlay shows most text in a group consistently high/low by the same amount, move all text baselines in that group together before changing individual font sizes.
- Do not thicken text to compensate for vertical drift. Fix baseline first, then adjust font weight/stroke for ink density.

Horizontal text/ink calibration:
- After baseline alignment, compare each repeated text group's dark/colored ink bbox on source vs rendered.
- If rendered body copy is wider and darker than the source, reduce stroke first, then weight, then decimal font size; do not keep heavy strokes because the text "looks sharper".
- If a long summary line is too narrow while its height is correct, prefer small positive `letter-spacing` over increasing font size, so height/baseline remain stable.
- Adjust column text left edges independently if the source columns are not perfectly symmetric. Do not force equal text insets when measured source bboxes differ.
- Low-opacity decorative line art still needs a bbox anchor. Measure its full visible bbox and match position/scale natively instead of leaving a tiny symbolic approximation.

Hard gate:
- Do not accept a comparison slide where repeated columns have uneven widths/gutters unless the source itself is uneven.
- Do not crop text or card structures. Only complex decorative icons may be cropped, and only after native redrawing fails.
- Preserve bottom summary bars as native editable shapes and text; they are usually the semantic conclusion of the slide.

### 1.3d Layered architecture calibration

For slides that explain stacked architecture layers (for example IaaS/MaaS/SaaS), create anchors for both the vertical layer rhythm and the horizontal architecture/detail rhythm.

Required anchors:
- Header title bbox, red/blue underline segment endpoints, and page-number badge bbox.
- Left layer label tiles: each tile bbox, icon bbox, layer name bbox, subtitle bbox, and body line bboxes.
- Main layer containers: outer bbox, stroke color, section title bbox, inner feature-card bboxes, component/pill row bboxes, and upward/downward connector arrow endpoints.
- Repeated feature cards inside each layer: icon bbox, heading bbox, body line bboxes, and card border/fill.
- Right insight panel: header bbox, each insight card bbox, red number badge bbox, icon bbox, heading bbox, and body line bboxes.
- Bottom mini flow: each stage pill bbox, arrow bbox, and text bbox.

Calibration order:
1. Align the left layer tiles and the three main layer containers as one stacked group.
2. Align the right insight panel as a separate column, preserving its top/bottom relationship to the main group.
3. Align connector arrows between layers and the bottom mini-flow arrows.
4. Calibrate repeated feature-card positions and pill spacing inside each layer.
5. Calibrate text baselines/ink density only after the layer/container rhythm is stable.
6. Tune or crop icon-only details last.

Global scale and density calibration:
- If the overlay shows most of a stacked architecture page is "plausible but redesigned", measure group bboxes before any local edits: header/title/underline, left tile column, main three-layer stack, right insight column, and bottom mini-flow.
- For each group, record source bbox, rendered bbox, and drift in `diagnostics/<page>.vN.judgment.md`. Fix row heights, gutters, card insets, and group translations first.
- Then measure repeated text density: heading bbox height, body-line baseline gap, pill text bbox, and right-card body bbox. Architecture dashboards often require smaller body type and lighter ink than a generated SVG's default bold look.
- Do not treat icon mismatches as the primary failure while cards, pills, or text density are still visibly oversized/undersized.

Soft surface/shadow calibration:
- Layered architecture screenshots often use subtle shadows, edge vignettes, and faint card elevation. These are visual primitives, not bitmap excuses. Rebuild them with native SVG radial/linear gradients and low-opacity offset rectangles before accepting the page.
- Add soft underlay rectangles behind left layer tiles, major layer containers, inner feature cards, insight cards, bottom-flow pills, and page badges when the source shows card lift or gray edge halos. Keep these underlays separate from the editable foreground shapes.
- Do not use SVG filters for shadows because the ppt-master path may not preserve them. Use 1-3 translucent native rectangles or gradients with calibrated offsets instead.
- If a rendered page looks too "clean" or "flat" while anchors and icon semantics pass, reject it and add a surface calibration pass before changing text or using more crops.

Hard gate:
- Do not accept a layered-architecture slide where the three layers have different vertical rhythm from the source or where the right insight column drifts relative to the main group.
- Left layer tiles, layer containers, cards, arrows, insight cards, and pills are simple editable structures and must remain native SVG/PPT shapes.
- Icon-only crops are allowed only for compact glyphs after native redraw is no longer the main value; never crop the layer label text or the feature-card text.

### 1.3e Component-architecture and workflow calibration

For slides that combine a radial component architecture diagram with a numbered execution workflow and lower explanation cards, create anchors for each subsystem before generating SVG.

Required anchors:
- Header: left chevron/brand mark bbox, title text bbox, top-right page-corner badge bbox, and any red section bars.
- Radial architecture panel: outer panel bbox, section header bar bbox, central hub circle center/radius, central hub icon bbox, hub label bbox, background circular guide bbox, every surrounding component card bbox, header strip bbox, icon bbox, body text bboxes, and colored/dashed arrow endpoints.
- Workflow panel: outer panel bbox, section header bar bbox, each numbered row bbox, number badge bbox, row icon bbox, title bbox, description bbox, vertical arrow x positions, and right-side loop-back bracket/arrow endpoints.
- Detail cards: bottom section header bbox, each card bbox, card header strip bbox, heading bbox, bullet left edge, bullet baselines, and card border/fill.
- Insight panel: section header bbox, icon circle bboxes, icon glyph bboxes, insight text bboxes, separator/column rhythm if present, and emphasized inline text bbox.

Calibration order:
1. Align the four macro panels (architecture, workflow, details, insight) plus title/page badge.
2. Align section bars and panel borders.
3. Align the radial hub, circular guide, component card bboxes, and arrows as a single architecture group.
4. Align workflow rows as a repeated-row group, including number badges and right loop bracket.
5. Align bottom detail cards as equal-width repeated cards, then calibrate bullets.
6. Calibrate text bboxes/ink density.
7. Apply icon crops last and inspect the crop contact sheet before judging.

Hard gate:
- Do not accept if the architecture diagram looks like a redesigned radial layout, even if the text is correct.
- Workflow rows must preserve the source row rhythm and number-color mapping.
- Component cards, workflow rows, bottom cards, red section bars, arrows, circles, and brackets are editable primitives and must remain native SVG/PPT shapes.
- For compact glyphs inside cards/rows/circles, source crops are allowed in the first version if they are transparent, text-free, and recorded in `downgrades[]`.
- If a card header contains a long bilingual title, split editable text into separate lines only when the source itself wraps; do not compress a two-line source into one line just to fit.
- Before acceptance, perform a text-fit/overflow pass on every bilingual header, workflow row, detail-card header, and inline-emphasis sentence. If any rendered text is clipped by its card, overlaps body text, or collides with an emphasized red phrase, reject the page and adjust font size, wrapping, or x positions while keeping the text editable.
- For workflow rows with a long title and a right-side description, reserve separate horizontal lanes for title and description. Do not let the title extend into the description lane; reduce font size or split the source-wrapped title instead.
- For bottom detail cards, prefer source-like two-line wrapping for long titles such as `Agentic Loop 自主循环` and `Context Management 上下文管理`. A long single-line bilingual title that clips inside a card is a fidelity failure.
- For inline emphasis inside insight text, measure the preceding black run and place the red run after its rendered bbox with a small source-like gap. Do not position the red run by guesswork.

### 1.4 Icon semantic identification (MANDATORY for every icon)

Icons are the #1 source of fidelity failures. A "looks like a list" vs "server stack" confusion is invisible to text/layout checks but immediately visible to any viewer. Before generating SVG, every icon must have a **semantic label** locked down.

For each icon element in `analysis/<page>.elements.json`, add these fields:

```json
{
  "region": "R4",
  "type": "icon",
  "icon_semantic": "server_stack",
  "icon_description": "3 stacked horizontal bars with indicator dots on left, each bar has a small vertical line on right side. Represents compute infrastructure / server hardware.",
  "icon_visual_form": "3 rounded rects stacked vertically, white dot on left of each, thin white horizontal line across middle",
  "position": {"cx": 234, "cy": 498, "size": 58},
  "style": {"fill": "#3A5BBF"}
}
```

Required fields:
- `icon_semantic`: one of the standard labels below, or a free-form kebab-case name if no label fits
- `icon_description`: what the icon depicts in plain language (2-3 sentences). This is the **contract** — the SVG generation step must produce something matching this description
- `icon_visual_form`: describe the actual geometric shapes you see (not what it "means"). e.g., "circle with two dots and a curved line below" not "smiley face"

Icon fidelity rules:
- Separate the **container** from the **glyph**. Record whether the icon sits in a filled circle, outlined circle, rounded square, badge, or no container. Do not invert foreground/background colors unless the source does.
- Transcribe visible icon text exactly. If a coin says `TOKEN`, `icon_visual_form` must say `TOKEN`, and the SVG must render the full word, not a generic `T`.
- For ambiguous glyphs, describe discriminating features: a robot/AI head has a head silhouette or chip, not a smile; a lightbulb has a bulb outline, rays, and a base; a server stack has stacked chassis and ports.
- Before accepting SVG output, compare each rendered icon against its `icon_visual_form`. Any semantic swap or missing visible lettering is a Step 2.5 failure.
- If text, card geometry, and layout anchors pass but native icon redraw remains the dominant fidelity gap after repeated attempts, downgrade only the tight icon bbox to a source crop. Keep surrounding text and simple frames native. Do not include adjacent editable text in the crop, and log the crop in `analysis/<page>.crops.json` plus `accept.json` `downgrades[]`.

Icon crop contract:
- Crop from the source scaled to the target viewBox whenever possible, so the crop's bitmap pixel size is at least the display size and does not trigger blurry-image warnings.
- Every crop record must include `source_bbox_viewbox`, `display_bbox`, `contains_text: false`, `native_replaced`, and a one-line reason.
- The crop bbox may include a few pixels of the original icon background to cover antialiased edges, but it must not include editable labels, card borders, arrows, or large structural shapes.
- Place the crop exactly over the native icon bbox after the card/text geometry has passed. Do not move text or resize containers to make a crop look better.
- If the crop contains a visible word or numeral that belongs to the icon itself, record it under `icon_text`; otherwise set `icon_text` to `null`.
- A crop must not introduce a visible rectangular background patch. If the crop background differs from the SVG-native background, create an alpha-matted transparent crop that preserves only the icon pixels and antialiased edge pixels. For white glyphs on colored tiles, matte by white/low-saturation brightness; for colored glyphs on light cards, matte by the icon hue and exclude black/body text pixels.
- After adding transparent crops, run a post-crop artifact pass. Reject any crop that leaves stray card-border lines, partial neighboring heading glyphs, duplicated text, or clipped icon strokes. Tighten the crop bbox or hue mask and rerender before judging other regions.
- For dominant title text where height/ink matches but width differs because the source font is not available, calibrate the rendered text bbox explicitly while preserving editable text. Prefer a small horizontal text transform on the title run over changing font size if changing font size would break the vertical bbox.
- When a hue-based transparent crop cannot separate an icon from same-colored neighboring heading text, use connected-component filtering inside the crop. Keep the components whose bbox/centroid belongs to the icon area, and discard components that are thin border lines, text-like fragments, or outside the icon's expected bbox.
- `contains_text: false` is an assertion, not proof. Before accepting a crop-based SVG, render a crop contact sheet on a checkerboard background and inspect every crop as its own artifact. Reject the version if any crop contains neighboring heading/body glyphs, numerals that are not intrinsic icon text, card-border fragments, or clipped icon strokes.
- For icons beside same-color labels, prefer preserving the intended icon display bbox while setting non-icon connected components to zero alpha. Do not widen an icon crop to include neighboring label pixels, and do not move editable text to hide crop contamination.

Standard icon semantic labels (use these when applicable):

| Label | Depicts | Typical visual form |
|-------|---------|-------------------|
| `server_stack` | Compute/servers | 2-3 stacked rounded rects |
| `cloud` | Cloud computing | Cloud shape outline |
| `network_mesh` | Connected nodes | Hub with radiating spokes |
| `shield` | Security | Shield/badge outline |
| `lock` | Access control | Padlock shape |
| `lightbulb` | Ideas/insight | Bulb outline + base lines; often rays around bulb |
| `ai_robot` | AI/ML | Robot/chip/head silhouette with AI text or circuit dots |
| `chart_bar` | Data/analytics | Vertical bars of varying height |
| `chart_line` | Trends | Polyline with dots |
| `coin_token` | Currency/token | Coin circle or stacked coins; preserve visible label such as `TOKEN` exactly |
| `grid_apps` | Applications | 2×2 or 3×3 square grid |
| `arrow_right` | Flow/progress | Right-pointing chevron/triangle |
| `user_person` | People/users | Head + shoulders silhouette |
| `gear_settings` | Configuration | Gear/cog outline |
| `document` | Files/docs | Rectangle with folded corner |

**Why this matters**: Without this step, the model will "guess" an icon shape based on the surrounding text context. "算力承载模型" → model draws something abstract. With `icon_semantic: "server_stack"` + `icon_visual_form`, the generation step has an explicit target to match. ZAI ui_diff_check will catch if the rendered icon doesn't match the semantic label.

Prompt template (for VLM-only flows): see [references/vlm-prompts.md](references/vlm-prompts.md)

## Step 2: SVG Generation

Generate SVG from the structured analysis. Follow these rules:

### Canvas Setup

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1920 1080"
     width="1920" height="1080">
```

Use pixel-based viewBox matching the image dimensions. Do NOT use EMU.

### Element Mapping

| Image Element | SVG Element |
|---------------|-------------|
| Text block | `<text>` with explicit `x`, `y`, `font-size`, `fill` |
| Rectangle | `<rect>` with `x`, `y`, `width`, `height`, optional `rx` |
| Circle/Ellipse | `<circle>` or `<ellipse>` |
| Line/Arrow | `<line>` or `<path>` with marker |
| Group of elements | `<g id="descriptive-name">` |
| Photo/Complex illustration | `<image href="...">` |
| Chart | Rebuild with SVG shapes (bars = rects, pie = paths) |
| Icon | Rebuild with simple shapes or `<use>` for icon references |

### Critical Constraints (from ppt-master)

Read [references/svg-constraints.md](references/svg-constraints.md) for the full list. Summary:

**Banned** (DrawingML has no equivalent):
- `mask` — use gradient overlays or clipPath instead
- `<style>`, `class` — use inline attributes only
- `@font-face`, `foreignObject` — no external font loading
- `textPath`, `animate*`, `<script>`, `<iframe>`
- HTML named entities (`&mdash;`) — use raw Unicode (`—`)
- `symbol` + `use` (for non-icon purposes)
- group-level opacity on `<g>` — set `fill-opacity`, `stroke-opacity`, or `opacity` on each child element instead

**Conditional** (allowed with restrictions):
- `marker-start`/`marker-end` — arrows only
- `clip-path` — image cropping only, not on shapes
- `<use>` — icon references only, must be expanded by `embed_icons.py`

**Always**:
- Use raw Unicode for special chars: `—` `→` `©` `&` must be `&amp;`
- Use `<g id="...">` for logical content blocks (enables animation)
- Use PPT-safe fonts: `Microsoft YaHei`, `SimHei`, `Arial`, `Segoe UI`
- Position text with explicit `x`, `y` (y = baseline), `text-anchor`
- Split long paragraphs into separate `<text>` elements per line

## Step 2.5: Visual Fidelity Verification (MANDATORY)

The SVG quality checker only validates *technical* conformance (banned features, XML validity). It does NOT tell you whether your SVG looks like the source image. This step does.

**Division of labor.** Scripts only *prepare* the comparison — render the SVG, optionally lay it next to the source. **The judgment is the model's, performed by Vision-inspecting the images.** Do not write or use scripts that try to algorithmically score fidelity (pixel diff, SSIM, OCR-of-rendered). Those metrics either miss the point (a layout shift that looks fine scores badly; semantic icon mismatch scores fine) or hide failures behind a number.

**Two-layer judgment.** After the model's own Vision check (§2.5.3), run an independent third-party visual comparison tool if available in the current environment (e.g., `mcp__zai-mcp-server__ui_diff_check` or any image diff MCP). The model's self-check catches obvious issues; an independent tool catches what the model missed (especially icon semantic mismatches where the model "sees what it expects"). If no external diff tool is available, skip this layer but note it in the judgment file.

### 2.5.1 Render SVG back to PNG at source resolution

Use `scripts/render_svg.py` (Playwright headless Chromium):

```bash
python3 "${SKILL_DIR}/scripts/render_svg.py" \
  --svg svg_output/<page>.svg \
  --out diagnostics/<page>.rendered.png \
  --width 1920 --height 1080
```

If the script's renderer is unavailable, any equivalent works (Playwright MCP screenshot, `npx playwright screenshot`, Chrome headless). The output must be a PNG at the source image's resolution.

Renderer path requirement:
- If the SVG contains relative `<image href="...">` crop references, those paths must resolve relative to the SVG file directory. The bundled `scripts/render_svg.py` sets an HTML `<base>` tag for this when wrapping SVG in temporary HTML. If crops appear as browser broken-image placeholders, fix renderer/path resolution before judging visual fidelity.

### 2.5.2 (Optional) Build side-by-side helper image

For quick visual scanning, `compare_images.py` lays source and rendered next to each other with an alignment grid:

```bash
python3 "${SKILL_DIR}/scripts/compare_images.py" \
  --source source_images/<page>.png \
  --rendered diagnostics/<page>.rendered.png \
  --out diagnostics/<page>.compare.png
```

This is a convenience — the model could equally well Read both images separately. The script makes **no judgment**; it only formats.

### 2.5.2b Build same-canvas overlay for alignment-sensitive pages

For one-to-one reproduction work, side-by-side comparison is not enough. Also create a same-size overlay where the source is scaled to the SVG canvas and the rendered PNG is composited over it:

```bash
python3 "${SKILL_DIR}/scripts/overlay_images.py" \
  --source source_images/<page>.png \
  --rendered diagnostics/<page>.rendered.png \
  --out diagnostics/<page>.overlay.png
```

Use the overlay to inspect drift in:
- text baselines and left edges
- circle centers/radii
- frame corners and arrow endpoints
- icon bboxes
- divider lines and card boundaries

Hard gate for "one-to-one" tasks:
- If the user requests exact reproduction or says the result is still far off, the next judgment MUST include this overlay artifact.
- If the overlay shows major anchors drifting, update the geometry contract before regenerating the SVG.
- After repeated native reconstruction failures, stop blind native tuning. Identify which remaining differences are simple editable primitives vs. complex bitmap details. Keep primitives native and use source crops only for the complex bitmap/icon details. Never use a full-page source image as a substitute for editable reconstruction unless the user explicitly requests a screenshot-like output.

### 2.5.2c Selective crop downgrades

Allowed crop downgrades:
- Photos or raster illustrations.
- Complex icons whose geometry cannot be reliably reproduced with native SVG within the current loop.
- Texture/noise/shadow details that are not meaningful editable objects.

Forbidden crop downgrades unless explicitly requested by the user:
- Full-slide source image.
- Text blocks.
- Simple boxes, circles, lines, arrows, dividers, and rounded frames.

Every `<image>` crop must have:
- a crop source path in `analysis/<page>.crops.json`
- a reason
- a target bbox in SVG coordinates
- an entry in `diagnostics/<page>.accept.json` `downgrades[]`

### 2.5.3 Model judgment (the only check that matters)

Open the rendered PNG and the source PNG in the model's vision. Answer each question explicitly. **A "yes" without a specific reason is not a pass.**

1. **Text completeness.** Walk through every visible text block in the source and locate its counterpart in the rendered. Are all main titles, card headings, numeric data, and footer text present and identical character-by-character? List any text that's missing, paraphrased, truncated, or invented.
2. **Layout alignment.** Are the major regions (header, columns, cards, footer) positioned and sized within ~5% of the source? Use the grid in the compare image, or eyeball the proportions. Call out any region that drifted noticeably.
3. **Color palette match.** Are the dominant colors (background, primary brand, accent) recognizably the same? Would a viewer call it "the same slide" or "a redesign"?
4. **Semantic icon match.** For every iconic element in the source, is the rendered version the right *type* — a lock is a lock, an arrow points the same way, three lines is three lines? Pixel-perfect not required, but category mismatches are failures.

Write the answers to `diagnostics/<page>.judgment.md`. Be specific (`"title '...' missing"`, not `"some text issues"`). If any answer surfaces a real problem, return to Step 1 for the failing region. Max 3 rounds; on the 4th attempt, downgrade that region to an embedded `<image href="...crop.png">` of the source crop and log it in `analysis/<page>.json` under `downgrades[]`.

### 2.5.4 Independent visual verification (SECOND PASS, if tool available)

After the model's own judgment passes, run an independent image diff tool (e.g., `ui_diff_check` MCP) to catch issues the model's self-review missed:

```
image_diff_tool(
  expected = source image,
  actual = rendered SVG,
  prompt = "逐区域对比：1.文字是否逐字忠实还原 2.布局位置是否对齐 3.颜色是否一致 4.图标语义是否匹配。按区域列出所有差异。"
)
```

Record results in `diagnostics/<page>.zai-judgment.md` (or similar).

**Gate**: If the tool reports any HIGH-severity icon semantic mismatch, the page is NOT accepted — return to Step 1.3 for the failing icon(s), re-identify, regenerate, and re-verify. Max 3 rounds total (model self-check + tool combined).

### 2.5.5 Acceptance

After judgment, write `diagnostics/<page>.accept.json`:

```json
{"page": "<page>", "accepted": true, "rounds": 1, "downgrades": [], "omitted": [], "judgment_ref": "diagnostics/<page>.judgment.md", "independent_judgment_ref": "diagnostics/<page>.zai-judgment.md"}
```

Without this acceptance record, downstream steps (PPTX export, user delivery) must not run.

## Step 3: SVG Quality Check

Run ppt-master's quality checker:

```bash
PPT_MASTER="${SKILL_DIR}/scripts/ppt-master"
python3 "$PPT_MASTER/svg_quality_checker.py" svg_output/
```

Fix any errors before proceeding. No auto-fix — re-author the page in context.

## Step 4: Export to PPTX (Optional)

If the user wants PPTX output:

```bash
PPT_MASTER="${SKILL_DIR}/scripts/ppt-master"
python3 "$PPT_MASTER/finalize_svg.py" <project_path>
python3 "$PPT_MASTER/svg_to_pptx.py" <project_path> --only native -t none -o output.pptx
```

## Fidelity Rules

1. The source image is the layout contract. Match its visual structure, not just content.
2. Every visible text must be editable SVG `<text>`, not a path or image.
3. Shapes must be native SVG elements (`<rect>`, `<circle>`, `<path>`), not embedded images.
4. Colors must be sampled from the source image precisely (use hex values).
5. Layout proportions must match the source. Use the same coordinate system.
6. Do not redesign, simplify, or create a new layout from the content alone.

## Project Layout

```
projects/YYYYMMDD_slug/
  source_images/       <- input images
  analysis/            <- VLM analysis JSON
  svg_output/          <- generated SVG files
  diagnostics/         <- quality check results
```

## Multi-Page Workflow

1. Analyze and convert ONE representative page first
2. Run quality check + visual comparison against source
3. Only after passing, apply the same style/coordinate conventions to remaining pages
4. For each page: create a brief blueprint before SVG generation

## Usage

```
/image-to-svg path/to/image.png
/image-to-svg path/to/image.png --format 4:3
/image-to-svg path/to/images/ --batch
/image-to-svg path/to/image.png --ocr paddleocr
/image-to-svg path/to/image.png --no-export
```

| Option | Description |
|--------|-------------|
| `--format <ratio>` | Canvas ratio: 16:9 (default), 4:3, 1:1, 9:16, 3:4 |
| `--batch` | Process multiple images in a folder |
| `--ocr <engine>` | Cross-validate text with OCR: paddleocr, tesseract, none (default: none) |
| `--no-export` | Stop at SVG, skip PPTX export |
| `--output <path>` | Custom output directory |

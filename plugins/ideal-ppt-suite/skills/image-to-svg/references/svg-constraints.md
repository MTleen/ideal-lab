# SVG Constraints for ppt-master Compatibility

Source: ppt-master technical design + empirically-grown blacklist.

## Banned Features

DrawingML has no equivalent for these. Presence triggers `svg_quality_checker.py` error.

### Structural

| Feature | Reason | Substitute |
|---------|--------|-----------|
| `<mask>` | DrawingML cannot represent SVG masks | Gradient overlay, clipPath, filter shadow, or bake into source image |
| `<style>` / `class` attribute | DrawingML has no CSS cascade | Inline all attributes on each element |
| `@font-face` | No font embedding in DrawingML | Use system/PPT-safe fonts |
| `<foreignObject>` | No HTML embedding in DrawingML | Rebuild as native SVG |
| `<symbol>` + `<use>` (non-icon) | Unsupported conversion path | Inline the content directly |
| `<textPath>` | Text on a path not supported | Straight-line text only |
| `animate*` (any animation) | PPTX uses its own animation model | Remove; PPTX animations added via `animations.json` |
| `<script>`, `<iframe>` | Security and compatibility | Never use |

### Encoding

| Issue | Fix |
|-------|-----|
| HTML named entities (`&mdash;`, `&rarr;`) | Use raw Unicode: `—`, `→`, `©` |
| Unescaped XML reserved chars | `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` |
| NBSP in text | Use ` ` or actual non-breaking space character |

## Conditional Features

Allowed with specific restrictions.

| Feature | Restriction |
|---------|------------|
| `marker-start` / `marker-end` | Arrows only. Must be simple triangular markers. |
| `clip-path` | Image cropping only. Not allowed on shapes or text. |
| `<use>` | Icon references only (`<use data-icon="...">`). Expanded by `embed_icons.py` in post-processing. |
| `<image>` | Photos, complex illustrations, genuinely non-editable regions only. Not for text or simple shapes. |
| `<filter>` | Only `drop-shadow` equivalent. Complex filters (blur, turbulence) not supported. |
| Gradient (`linearGradient`, `radialGradient`) | Supported. Use `<defs>` block. Keep simple (2-3 stops). |
| `<pattern>` | Not supported. Use solid/gradient fill instead. |

## Required Patterns

### Logical Grouping

Every slide must use top-level `<g>` groups for logical content blocks:

```xml
<g id="background">...</g>
<g id="header">...</g>
<g id="content-main">
  <g id="title-text">...</g>
  <g id="body-columns">...</g>
</g>
<g id="footer">...</g>
```

Auto-skipped animation groups (by id token): `background`, `header`, `footer`, `decoration`, `watermark`, `page_number`.

### Text

- Use `<text>` elements. Never convert text to `<path>`.
- Position with `x`, `y` (y = baseline position), `text-anchor`.
- For multi-line text, use separate `<text>` elements (not `<tspan dy="...">` when possible).
- PPT-safe fonts: `Microsoft YaHei`, `SimHei`, `Arial`, `Segoe UI`, `Helvetica Neue`.
- Font sizes in pixels (matching viewBox coordinate space).

### Coordinates

- ViewBox uses pixel units (e.g., `viewBox="0 0 1920 1080"`).
- All coordinates in pixels relative to viewBox.
- EMU conversion happens only at export time in `svg_to_pptx.py`.

### Images

- External references during development (`<image href="photo.png"/>`).
- `finalize_svg.py` handles Base64 inlining for `svg_final/`.
- `svg_to_pptx.py` copies bitmaps into PPTX media folder.

## Quality Gate

`svg_quality_checker.py` enforces these rules on `svg_output/`. It runs BEFORE post-processing.

Severity model:
- **Error**: Must fix. Re-author the page. No auto-fix.
- **Warning**: Informational. Does not block.

Why no auto-fix: A banned `<style>` element exists because the Executor used it for a reason. Auto-fixing to inline attributes would silently lose the design intent.

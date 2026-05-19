# VLM Prompt Templates

## Slide Analysis Prompt (Primary)

Use this prompt with Claude Vision to analyze a slide image:

```
Analyze this slide/image. Extract ALL visible content as structured JSON.

Output format:
{
  "canvas": {"width": <pixel_width>, "height": <pixel_height>, "ratio": "<16:9|4:3|1:1|9:16|3:4>"},
  "layout_type": "<title_content|two_column|three_column|comparison|data_dashboard|image_focus|timeline|process|quote|blank>",
  "background": {
    "type": "<solid|gradient|image|pattern>",
    "color": "<hex>",
    "gradient": {"direction": "<vertical|horizontal|diagonal>", "colors": ["<hex>", "<hex>"]}
  },
  "elements": [
    {
      "id": "<descriptive_id>",
      "type": "<text|shape|image|chart|icon|line|divider|group>",
      "content": "<visible text or description>",
      "position": {"x": <0-1>, "y": <0-1>, "w": <0-1>, "h": <0-1>},
      "style": {
        "font_family": "<guess or null>",
        "font_size": "<large|medium|small|tiny or px estimate>",
        "font_weight": "<bold|semibold|normal|light>",
        "color": "<hex>",
        "background": "<hex or null>",
        "alignment": "<left|center|right>",
        "border_radius": "<none|small|medium|large|pill>",
        "border": {"color": "<hex>", "width": "<thin|medium|thick>"}
      },
      "shape_type": "<rect|circle|triangle|arrow|star|hexagon|custom>",
      "chart_data": {
        "type": "<bar|line|pie|donut|area>",
        "categories": ["<cat1>", ...],
        "series": [{"name": "<name>", "values": [<v1>, ...]}]
      },
      "children": [<nested elements>]
    }
  ],
  "color_palette": ["<hex1>", "<hex2>", ...],
  "typography": {
    "title_size": "<relative>",
    "body_size": "<relative>",
    "font_families": ["<family1>", ...]
  },
  "hierarchy": {
    "title": "<element_id>",
    "subtitle": "<element_id or null>",
    "body": ["<element_id>", ...],
    "emphasis": ["<element_id>", ...],
    "decoration": ["<element_id>", ...]
  }
}

Rules:
- Extract EVERY visible text character. No paraphrasing or summarizing.
- Position values are relative (0.0 to 1.0) of canvas dimensions.
- Colors must be precise hex values sampled from the image.
- Identify the visual hierarchy: what is the title, what is body, what is decoration.
- For charts, estimate the data values from visual proportions.
- For icons, describe what the icon represents.
- Group related elements (e.g., a card with title + body + icon).
```

## Text-Heavy Slide Prompt

For slides dominated by text content:

```
Analyze this text-heavy slide. Focus on precise text extraction and hierarchy.

For each text block, provide:
1. Exact text content (character-for-character)
2. Font size relative to other text (title > heading > body > caption)
3. Color (hex)
4. Position (relative 0-1)
5. Weight (bold/normal)
6. Alignment

Also identify:
- Bullet or numbered list structures
- Column divisions
- Text hierarchy levels
- Emphasized or highlighted text
- Links or references
```

## Chart/Data Slide Prompt

For slides containing charts or data visualizations:

```
Analyze this data visualization slide. Extract:

1. Chart type (bar, line, pie, donut, scatter, area, table)
2. All axis labels and tick values
3. Data series names
4. Approximate data values (estimate from visual proportions)
5. Colors mapped to each series
6. Legend content
7. Grid lines or reference lines
8. Title and annotations
9. Any summary statistics shown (totals, averages, percentages)

Output as structured JSON with chart_data field.
```

## Icon/Shape Reconstruction Prompt

When analyzing icons and simple shapes for vector reconstruction:

```
Analyze the icons and shapes in this image. For each icon/shape:

1. Basic geometric description (circle, square, triangle, arrow, etc.)
2. Fill color (hex)
3. Stroke color and width
4. Size relative to canvas
5. Position (relative 0-1)
6. Can it be rebuilt from basic SVG shapes? (yes/no)
7. If yes, suggest SVG elements: rect, circle, path, polygon, line
8. If no, mark as "needs image embedding"

For complex icons that cannot be vectorized easily, note:
- "image-embed: true" — will be embedded as <image> in SVG
```

## OCR Cross-Validation Template

When using PaddleOCR to verify VLM text extraction:

```python
import json
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr('image.png', cls=True)

# Extract text with positions
ocr_text = []
for line in result[0]:
    bbox, (text, confidence) = line
    x1, y1 = bbox[0]
    x2, y2 = bbox[2]
    ocr_text.append({
        "text": text,
        "confidence": confidence,
        "bbox": {"x": x1, "y": y1, "w": x2-x1, "h": y2-y1}
    })

# Compare with VLM extraction
with open('analysis/vlm_result.json') as f:
    vlm_result = json.load(f)

# Cross-validate: flag discrepancies
for ocr_item in ocr_text:
    if ocr_item["confidence"] < 0.85:
        print(f"LOW CONF: {ocr_item['text']} ({ocr_item['confidence']:.2f})")
```

#!/bin/bash
# 通用 Markdown 转 Word 脚本
# 用于技术标书/投标文档的格式转换
#
# 使用方法:
#   ./markdown_to_word.sh [选项] <输入目录> [输出文件]
#
# 选项:
#   -o, --output FILE    输出文件名 (默认: 技术方案_完整版.docx)
#   -f, --files PATTERN  文件匹配模式 (默认: *_风格改写版.md)
#   -h, --help           显示帮助信息
#
# 示例:
#   ./markdown_to_word.sh 章节拆分/
#   ./markdown_to_word.sh -o 投标文件.docx 章节拆分/

set -e

# 默认参数
OUTPUT_FILE="技术方案_完整版.docx"
FILE_PATTERN="*.md"
INPUT_DIR=""
TEMP_MERGED="_temp_merged.md"
TEMP_CLEANED="_temp_cleaned.md"

# 帮助信息
show_help() {
    echo "Markdown 转 Word 转换脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 [选项] <输入目录> [输出文件]"
    echo ""
    echo "选项:"
    echo "  -o, --output FILE    输出文件名 (默认: 技术方案_完整版.docx)"
    echo "  -f, --files PATTERN  文件匹配模式 (默认: *.md)"
    echo "  -h, --help           显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 章节拆分/"
    echo "  $0 -o 投标文件.docx 章节拆分/"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -f|--files)
            FILE_PATTERN="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            if [ -z "$INPUT_DIR" ]; then
                INPUT_DIR="$1"
            else
                OUTPUT_FILE="$1"
            fi
            shift
            ;;
    esac
done

# 检查输入目录
if [ -z "$INPUT_DIR" ]; then
    echo "错误: 请指定输入目录"
    show_help
    exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "错误: 目录不存在: $INPUT_DIR"
    exit 1
fi

# 检查依赖
if ! command -v pandoc &> /dev/null; then
    echo "错误: pandoc 未安装"
    echo "请运行: brew install pandoc"
    exit 1
fi

# 查找文件
FILES=()
while IFS= read -r -d '' file; do
    FILES+=("$file")
done < <(find "$INPUT_DIR" -name "$FILE_PATTERN" -type f -print0 | sort -z)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "错误: 未找到匹配的文件: $INPUT_DIR/$FILE_PATTERN"
    exit 1
fi

echo "=== Markdown 转 Word ==="
echo "输入目录: $INPUT_DIR"
echo "文件数量: ${#FILES[@]}"
echo "输出文件: $OUTPUT_FILE"
echo ""

# 步骤1: 合并所有文件
echo "=== 步骤1: 合并文件 ==="
> "$TEMP_MERGED"
for file in "${FILES[@]}"; do
    echo "  合并: $(basename "$file")"
    echo -e "\n\n" >> "$TEMP_MERGED"
    cat "$file" >> "$TEMP_MERGED"
done

# 步骤2: 预处理 Markdown
echo "=== 步骤2: 预处理格式 ==="
python3 << 'PYTHON_SCRIPT'
import re

with open('_temp_merged.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 清理 \newpage 指令
content = re.sub(r'\\newpage', '', content)

# 2. 清理水平分割线
content = re.sub(r'\n---+\n', '\n\n', content)

# 3. 确保标题前后有空行
content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
content = re.sub(r'(#{1,6} .+)\n([^\n])', r'\1\n\n\2', content)

# 4. 清理多余的连续空行
content = re.sub(r'\n{4,}', '\n\n', content)

# 5. 确保公式块前后有空行
content = re.sub(r'([^\n])\n(\$\$)', r'\1\n\n\2', content)
content = re.sub(r'(\$\$[^\$]+\$\$)\n([^\n])', r'\1\n\n\2', content)

# 6. 清理行尾空格
content = re.sub(r' +\n', '\n', content)

# 7. 修复表格格式（表头与分隔行之间不能有空行）
content = re.sub(r'(\|[^\n]+\|)\n\n(\|[-:| ]+\|)', r'\1\n\2', content)

# 8. 确保表格前后有空行
content = re.sub(r'([^\n])\n(\|[^\n]+\|\n\|[-:| ]+\|)', r'\1\n\n\2', content)

with open('_temp_cleaned.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("  格式清理完成")
PYTHON_SCRIPT

# 步骤3: Pandoc 转换
echo "=== 步骤3: Pandoc 转换 ==="
pandoc "$TEMP_CLEANED" \
    -o "$OUTPUT_FILE" \
    --from=markdown+pipe_tables+tex_math_dollars \
    --to=docx \
    --mathml \
    --wrap=none \
    --standalone \
    --metadata title="技术方案"

# 步骤4: 后处理 Word 格式
echo "=== 步骤4: Word 格式后处理 ==="
python3 << 'PYTHON_SCRIPT'
try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Twips
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    import sys
    output_file = sys.argv[1] if len(sys.argv) > 1 else '技术方案_完整版.docx'
    doc = Document(output_file)

    def set_run_font(run, font_name='宋体', font_size=12, color_rgb=RGBColor(0, 0, 0)):
        """设置文字格式：字体、大小、颜色"""
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.color.rgb = color_rgb
        r = run._element
        rPr = r.get_or_add_rPr()
        for child in list(rPr):
            if child.tag == qn('w:rFonts'):
                rPr.remove(child)
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        rFonts.set(qn('w:eastAsia'), font_name)
        rPr.insert(0, rFonts)

    # 处理段落
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        is_heading = para.style.name.startswith('Heading')

        if not is_heading and text:
            # 正文格式
            para.paragraph_format.first_line_indent = Twips(420)
            para.paragraph_format.line_spacing = 1.5
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after = Pt(0)

        for run in para.runs:
            if is_heading:
                if 'Heading 1' in para.style.name:
                    set_run_font(run, '黑体', 16)
                elif 'Heading 2' in para.style.name:
                    set_run_font(run, '黑体', 14)
                else:
                    set_run_font(run, '黑体', 12)
                run.italic = False
            else:
                set_run_font(run, '宋体', 12)

        if text:
            para.paragraph_format.line_spacing = 1.5
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after = Pt(0)

        # 一级标题自动分页
        if para.style.name == 'Heading 1' and i > 0:
            pPr = para._p.get_or_add_pPr()
            pageBreak = OxmlElement('w:pageBreakBefore')
            pPr.append(pageBreak)

    # 处理表格
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    for run in para.runs:
                        set_run_font(run, '宋体', 10.5)

    doc.save(output_file)
    print("  Word 格式后处理完成")

except ImportError:
    print("  警告: python-docx 未安装，跳过后处理")
except Exception as e:
    print(f"  后处理出错: {e}")
PYTHON_SCRIPT "$OUTPUT_FILE"

# 步骤5: 清理临时文件
echo "=== 步骤5: 清理临时文件 ==="
rm -f "$TEMP_MERGED" "$TEMP_CLEANED"

echo ""
echo "=== 完成 ==="
echo "输出文件: $OUTPUT_FILE"
